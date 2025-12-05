const KEY = "todos_v1";

export function loadTodos() {
    return JSON.parse(localStorage.getItem(KEY)) || [];
}

export function saveTodos(todos) {
    localStorage.setItem(KEY, JSON.stringify(todos));
}
