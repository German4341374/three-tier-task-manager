import assert from 'node:assert/strict';
import test from 'node:test';

import { countOpenTasks, taskCountLabel } from '../src/task-utils.js';

test('counts only incomplete tasks', () => {
  const tasks = [{ completed: false }, { completed: true }, { completed: false }];
  assert.equal(countOpenTasks(tasks), 2);
});

test('formats the open task label', () => {
  assert.equal(taskCountLabel([]), '0 open');
});
