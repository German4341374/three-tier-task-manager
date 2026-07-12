export function countOpenTasks(tasks) {
  return tasks.filter((task) => !task.completed).length;
}

export function taskCountLabel(tasks) {
  const count = countOpenTasks(tasks);
  return `${count} open`;
}
