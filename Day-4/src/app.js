import { debounce } from "./utils/debounce.js";
import { loadTodos, saveTodos } from "./storage/todosStorage.js";
import { addErrorLog } from "./errors/logger.js";

let todos = loadTodos();
let editIndex = null;

function renderTodos(list = todos) {
    const ul = document.getElementById("todoList");
    ul.innerHTML = "";

    list.forEach((todo, index) => {
        ul.innerHTML += `
            <li>
                <span onclick="toggle(${index})">${todo.text}</span>

                <div class="actions">
                    <button class="edit-btn" onclick="startEdit(${index})">✏️</button>
                    <button class="delete-btn" onclick="removeTodo(${index})">🗑️</button>
                </div>
            </li>
        `;
    });
}

window.startEdit = function (index) {
    document.getElementById("todoInput").value = todos[index].text;
    editIndex = index;
};

window.toggle = function (index) {
    try {
        todos[index].completed = !todos[index].completed;
        saveTodos(todos);
        renderTodos();
    } catch (e) {
        addErrorLog("Toggle Error", { index, message: e.message });
    }
};

window.removeTodo = function (index) {
    try {
        todos.splice(index, 1);
        saveTodos(todos);
        renderTodos();
    } catch (e) {
        addErrorLog("Delete Error", { index, message: e.message });
    }
};

document.getElementById("addBtn").onclick = function () {
    const input = document.getElementById("todoInput");
    let text = input.value.trim();

    if (!text) return;

    try {
        if (editIndex !== null) {
            todos[editIndex].text = text;
            editIndex = null;
        } else {
            todos.push({ text, completed: false });
        }

        saveTodos(todos);
        input.value = "";
        renderTodos();
    } catch (e) {
        addErrorLog("Add Error", { message: e.message });
    }
};

document.getElementById("searchInput").addEventListener(
    "input",
    debounce((e) => {
        let q = e.target.value.toLowerCase();
        let filtered = todos.filter(t => t.text.toLowerCase().includes(q));
        renderTodos(filtered);
    }, 300)
);

renderTodos();
