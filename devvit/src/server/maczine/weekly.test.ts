import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { runWeekly, threadTitle, weekKey, type WeeklyDeps } from './weekly.ts';

const MONDAY = new Date('2026-09-21T16:00:00Z');

type Harness = { deps: WeeklyDeps; posted: string[]; memory: Map<string, string>; stickied: string[] };

const harness = (overrides: Partial<WeeklyDeps> = {}): Harness => {
  const posted: string[] = [];
  const stickied: string[] = [];
  const memory = new Map<string, string>();
  const deps: WeeklyDeps = {
    subredditName: 'MacTechSolutions',
    now: MONDAY,
    submitText: async (opts) => {
      posted.push(opts.title);
      return { id: `t3_w${posted.length}`, permalink: `/r/MacTechSolutions/comments/w${posted.length}/x/` };
    },
    sticky: async (id) => void stickied.push(id),
    unsticky: async (id) => void stickied.splice(stickied.indexOf(id), 1),
    remember: async (key, value) => void memory.set(key, value),
    recall: async (key) => memory.get(key),
    ...overrides,
  };
  return { deps, posted, memory, stickied };
};

describe('weekKey', () => {
  it('is stable across a week and changes at the week boundary', () => {
    assert.equal(weekKey(new Date('2026-09-21T00:00:00Z')), weekKey(new Date('2026-09-27T23:59:00Z')));
    assert.notEqual(weekKey(new Date('2026-09-27T23:59:00Z')), weekKey(new Date('2026-09-28T00:01:00Z')));
  });

  it('formats as an ISO week', () => {
    assert.match(weekKey(MONDAY), /^\d{4}-W\d{2}$/);
  });
});

describe('threadTitle', () => {
  it('carries the date so two weeks never collide', () => {
    assert.equal(
      threadTitle(MONDAY),
      'Weekly thread: what are you working through? (September 21, 2026)'
    );
  });
});

describe('runWeekly', () => {
  it('posts and pins the thread', async () => {
    const { deps, posted, stickied } = harness();
    const outcome = await runWeekly(deps);

    assert.equal(outcome.status, 'POSTED');
    assert.equal(outcome.permalink, 'https://www.reddit.com/r/MacTechSolutions/comments/w1/x/');
    assert.equal(posted.length, 1);
    assert.deepEqual(stickied, ['t3_w1']);
  });

  it('posts only once a week however often it runs', async () => {
    const { deps, posted } = harness();
    await runWeekly(deps);
    const second = await runWeekly({ ...deps, now: new Date('2026-09-24T16:00:00Z') });

    assert.equal(second.status, 'ALREADY_POSTED');
    assert.equal(posted.length, 1);
  });

  it('posts again the following week, and unpins the old one', async () => {
    const { deps, posted, stickied } = harness();
    await runWeekly(deps);
    const next = await runWeekly({ ...deps, now: new Date('2026-09-28T16:00:00Z') });

    assert.equal(next.status, 'POSTED');
    assert.equal(posted.length, 2);
    assert.deepEqual(stickied, ['t3_w2']);
  });

  it('still counts as posted when pinning fails', async () => {
    const { deps, posted } = harness({
      sticky: async () => {
        throw new Error('not a moderator');
      },
    });
    const outcome = await runWeekly(deps);

    assert.equal(outcome.status, 'POSTED');
    assert.equal(posted.length, 1);
  });

  it('dry run posts nothing', async () => {
    const { deps, posted } = harness({ dryRun: true });
    assert.equal((await runWeekly(deps)).status, 'DRY_RUN');
    assert.equal(posted.length, 0);
  });

  it('reports a rejection without remembering the week', async () => {
    const { deps, memory } = harness({
      submitText: async () => {
        throw new Error('SUBREDDIT_NOTALLOWED');
      },
    });
    const outcome = await runWeekly(deps);

    assert.equal(outcome.status, 'REJECTED');
    assert.equal(memory.size, 0); // so the next run tries again
  });
});
