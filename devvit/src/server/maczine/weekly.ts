/**
 * The weekly discussion thread.
 *
 * A community that only ever receives link posts has nowhere for anyone to
 * talk, so the feed reads as a broadcast. This posts one open thread a week
 * and pins it. Like the article poster, every Reddit call is injected, so the
 * decision path is testable.
 */

export type WeeklyDeps = {
  readonly subredditName: string;
  readonly submitText: (opts: {
    subredditName: string;
    title: string;
    text: string;
  }) => Promise<{ id: string; permalink?: string }>;
  readonly sticky?: (postId: string) => Promise<void>;
  readonly unsticky?: (postId: string) => Promise<void>;
  readonly remember: (key: string, value: string, ttlSeconds: number) => Promise<void>;
  readonly recall: (key: string) => Promise<string | undefined>;
  readonly now?: Date;
  readonly dryRun?: boolean;
};

export type WeeklyOutcome = {
  readonly status: 'POSTED' | 'ALREADY_POSTED' | 'DRY_RUN' | 'REJECTED';
  readonly message: string;
  readonly permalink?: string;
};

const MEMORY_SECONDS = 60 * 60 * 24 * 60; // two months, well past one week

/** ISO week key, e.g. 2026-W39. Stable across timezones because it uses UTC. */
export const weekKey = (now: Date): string => {
  const date = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  // ISO weeks run Monday to Sunday and week 1 contains the first Thursday.
  const day = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - day);
  const yearStart = Date.UTC(date.getUTCFullYear(), 0, 1);
  const week = Math.ceil(((date.getTime() - yearStart) / 86400000 + 1) / 7);
  return `${date.getUTCFullYear()}-W${String(week).padStart(2, '0')}`;
};

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

export const threadTitle = (now: Date): string =>
  `Weekly thread: what are you working through? (${MONTHS[now.getUTCMonth()]} ${now.getUTCDate()}, ${now.getUTCFullYear()})`;

export const threadBody = (): string =>
  [
    'The open thread for the week. Anything goes as long as it is on topic:',
    '',
    '- A control you cannot work out how to evidence',
    '- An assessment coming up, or one you have just been through',
    '- A DFARS or CMMC clause you were handed and would rather understand than guess at',
    '- Tooling questions, and what has actually worked for you',
    '',
    'No question is too basic here. Most people in the defense industrial base',
    'inherited this work without asking for it.',
  ].join('\n');

export const runWeekly = async (deps: WeeklyDeps): Promise<WeeklyOutcome> => {
  const now = deps.now ?? new Date();
  const key = `weekly:${weekKey(now)}`;

  const existing = await deps.recall(key);
  if (existing) {
    return { status: 'ALREADY_POSTED', message: `this week's thread is already up`, permalink: existing };
  }

  const title = threadTitle(now);
  if (deps.dryRun) {
    return { status: 'DRY_RUN', message: `Would post "${title}" to r/${deps.subredditName}` };
  }

  let post: { id: string; permalink?: string };
  try {
    post = await deps.submitText({ subredditName: deps.subredditName, title, text: threadBody() });
  } catch (error) {
    return { status: 'REJECTED', message: error instanceof Error ? error.message : String(error) };
  }

  const permalink = post.permalink?.startsWith('/')
    ? `https://www.reddit.com${post.permalink}`
    : (post.permalink ?? post.id);
  await deps.remember(key, permalink, MEMORY_SECONDS);

  // Pinning is a nicety: a failure to pin must not make the run look failed,
  // and must not cause a retry that posts a second thread.
  const previous = await deps.recall('weekly:sticky');
  try {
    if (previous && deps.unsticky) await deps.unsticky(previous);
    if (deps.sticky) await deps.sticky(post.id);
    await deps.remember('weekly:sticky', post.id, MEMORY_SECONDS);
  } catch (error) {
    console.warn(`could not pin the weekly thread: ${error instanceof Error ? error.message : error}`);
  }

  return { status: 'POSTED', message: 'weekly thread posted', permalink };
};
