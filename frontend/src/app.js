import { taskCountLabel } from './task-utils.js';

const apiUrl = '/api/v1/tasks';
const form = document.querySelector('#task-form');
const list = document.querySelector('#task-list');
const status = document.querySelector('#status');
const count = document.querySelector('#task-count');

async function request(url = apiUrl, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
  return response.status === 204 ? null : response.json();
}

function render(tasks) {
  list.replaceChildren(...tasks.map((task) => {
    const item = document.createElement('li');
    item.className = `task${task.completed ? ' completed' : ''}`;
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = task.completed;
    checkbox.setAttribute('aria-label', `Complete ${task.title}`);
    checkbox.addEventListener('change', () => updateTask(task.id, { completed: checkbox.checked }));
    const title = document.createElement('span');
    title.textContent = task.title;
    const remove = document.createElement('button');
    remove.textContent = 'Delete';
    remove.addEventListener('click', () => deleteTask(task.id));
    item.append(checkbox, title, remove);
    return item;
  }));
  count.textContent = taskCountLabel(tasks);
}

async function loadTasks() {
  try { status.textContent = ''; render(await request()); }
  catch (error) { status.textContent = `Unable to load tasks: ${error.message}`; }
}

async function updateTask(id, data) {
  await request(`${apiUrl}/${id}`, { method: 'PATCH', body: JSON.stringify(data) });
  await loadTasks();
}

async function deleteTask(id) {
  await request(`${apiUrl}/${id}`, { method: 'DELETE' });
  await loadTasks();
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const title = new FormData(form).get('title').trim();
  if (!title) return;
  await request(apiUrl, { method: 'POST', body: JSON.stringify({ title }) });
  form.reset();
  await loadTasks();
});

loadTasks();
