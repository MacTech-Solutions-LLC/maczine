import { serve } from '@hono/node-server';
import { context, createServer, getServerPort, reddit, redis, settings } from '@devvit/web/server';
import type { TaskRequest, TaskResponse } from '@devvit/web/server';
import type { UiResponse } from '@devvit/web/shared';
import { Hono } from 'hono';

import { FEED_URL } from './maczine/feed.ts';
import { isSuccess, liveFetchText, runPoster, type Outcome, type PosterDeps } from './maczine/poster.ts';
import { runWeekly, type WeeklyDeps, type WeeklyOutcome } from './maczine/weekly.ts';

const RECENT_POSTS_TO_SCAN = 100;

type Config = { feedUrl: string; flairId: string; dryRun: boolean; weeklyThread: boolean };

/** Moderator settings, each falling back to a safe default. */
const config = async (): Promise<Config> => {
  const defaults: Config = { feedUrl: FEED_URL, flairId: '', dryRun: false, weeklyThread: true };
  try {
    const all = await settings.getAll<Record<string, unknown>>();
    const feedUrl = typeof all['feedUrl'] === 'string' ? all['feedUrl'].trim() : '';
    const flairId = typeof all['flairId'] === 'string' ? all['flairId'].trim() : '';
    return {
      feedUrl: feedUrl.startsWith('https://') ? feedUrl : FEED_URL,
      flairId,
      dryRun: all['dryRun'] === true,
      weeklyThread: all['weeklyThread'] !== false,
    };
  } catch (error) {
    console.warn(`could not read settings, using defaults: ${error instanceof Error ? error.message : error}`);
    return defaults;
  }
};

const store = {
  remember: async (key: string, value: string, ttlSeconds: number): Promise<void> => {
    await redis.set(key, value);
    await redis.expire(key, ttlSeconds);
  },
  recall: (key: string): Promise<string | undefined> => redis.get(key),
};

const weeklyDeps = (cfg: Config): WeeklyDeps => {
  const subredditName = context.subredditName;
  if (!subredditName) throw new Error('no subreddit in context');
  return {
    subredditName,
    dryRun: cfg.dryRun,
    submitText: async (opts) => {
      const post = await reddit.submitPost(opts);
      return { id: post.id, permalink: post.permalink };
    },
    sticky: async (postId) => {
      const post = await reddit.getPostById(postId as `t3_${string}`);
      await post.sticky();
    },
    unsticky: async (postId) => {
      const post = await reddit.getPostById(postId as `t3_${string}`);
      await post.unsticky();
    },
    ...store,
  };
};

const runWeeklyThread = async (trigger: string): Promise<WeeklyOutcome> => {
  console.log(`MacZine weekly thread: ${trigger} at ${new Date().toISOString()}`);
  const cfg = await config();
  if (!cfg.weeklyThread) {
    return { status: 'ALREADY_POSTED', message: 'the weekly thread is turned off in settings' };
  }
  const outcome = await runWeekly(weeklyDeps(cfg));
  const line = `RESULT=WEEKLY_${outcome.status} ${outcome.message}${outcome.permalink ? ` ${outcome.permalink}` : ''}`;
  if (outcome.status === 'REJECTED') console.error(line);
  else console.log(line);
  return outcome;
};

const deps = (options: Config): PosterDeps => {
  const subredditName = context.subredditName;
  if (!subredditName) throw new Error('no subreddit in context');
  return {
    subredditName,
    dryRun: options.dryRun,
    ...(options.flairId ? { flairId: options.flairId } : {}),
    fetchText: () => liveFetchText(options.feedUrl),
    recentPosts: async () => {
      const posts = await reddit
        .getNewPosts({ subredditName, limit: RECENT_POSTS_TO_SCAN, pageSize: RECENT_POSTS_TO_SCAN })
        .all();
      return posts.map((post) => ({ id: post.id, url: post.url, permalink: post.permalink }));
    },
    submitLink: async (opts) => {
      const post = await reddit.submitPost(opts);
      return { id: post.id, url: post.url, permalink: post.permalink };
    },
    ...store,
  };
};

const describe = (outcome: Outcome): string =>
  `RESULT=${outcome.status} ${outcome.message}${outcome.permalink ? ` ${outcome.permalink}` : ''}`;

const run = async (trigger: string): Promise<Outcome> => {
  // The fired-at stamp is deliberate: Devvit does not document the timezone
  // its cron runs in, so the logs are how we confirm when the job actually
  // fires and adjust the crons in devvit.json if it is not UTC.
  console.log(`MacZine poster: ${trigger} at ${new Date().toISOString()}`);
  const outcome = await runPoster(deps(await config()));
  const line = describe(outcome);
  if (isSuccess(outcome)) console.log(line);
  else console.error(line);
  return outcome;
};

const app = new Hono();

/**
 * The weekday schedule. Several runs a morning: the first posts, the rest find
 * the post already there and do nothing. The crons are in devvit.json.
 */
app.post('/internal/scheduler/post-latest-issue', async (c) => {
  await c.req.json<TaskRequest>().catch(() => undefined);
  try {
    await run('scheduled run');
  } catch (error) {
    // Never throw out of a scheduled task: a failed task may be retried, and a
    // retry that reposts is worse than a missed run. The next cron picks it up.
    console.error(`RESULT=UNEXPECTED ${error instanceof Error ? error.message : String(error)}`);
  }
  return c.json<TaskResponse>({ status: 'ok' }, 200);
});

/** Moderator menu item, for posting by hand if a morning is missed. */
app.post('/internal/menu/post-latest-issue', async (c) => {
  try {
    const outcome = await run('moderator menu action');
    if (outcome.status === 'POSTED' && outcome.permalink) {
      return c.json<UiResponse>({ navigateTo: outcome.permalink }, 200);
    }
    return c.json<UiResponse>({ showToast: outcome.message }, 200);
  } catch (error) {
    console.error(error);
    return c.json<UiResponse>({ showToast: 'MacZine poster failed; see the app logs' }, 400);
  }
});

app.post('/internal/scheduler/weekly-thread', async (c) => {
  await c.req.json<TaskRequest>().catch(() => undefined);
  try {
    await runWeeklyThread('scheduled run');
  } catch (error) {
    console.error(`RESULT=WEEKLY_UNEXPECTED ${error instanceof Error ? error.message : String(error)}`);
  }
  return c.json<TaskResponse>({ status: 'ok' }, 200);
});

app.post('/internal/menu/weekly-thread', async (c) => {
  try {
    const outcome = await runWeeklyThread('moderator menu action');
    if (outcome.status === 'POSTED' && outcome.permalink) {
      return c.json<UiResponse>({ navigateTo: outcome.permalink }, 200);
    }
    return c.json<UiResponse>({ showToast: outcome.message }, 200);
  } catch (error) {
    console.error(error);
    return c.json<UiResponse>({ showToast: 'Weekly thread failed; see the app logs' }, 400);
  }
});

serve({
  fetch: app.fetch,
  createServer,
  port: getServerPort(),
});
