import { Reactive, Component } from "./core";

/** Реактивное состояние для счётчика */
const count = new Reactive<number>(0);

/** Реактивное состояние для списка задач */
const tasks = new Reactive<string[]>([]);

/** Компонент счётчика */
class Counter extends Component {
    template(): string {
        return `
            <div style="margin-bottom: 20px;">
                <h1>Счётчик: ${count.value}</h1>
                <button id="increment">Увеличить</button>
                <button id="decrement">Уменьшить</button>
            </div>
        `;
    }

    protected afterRender() {
        document.getElementById("increment")?.addEventListener("click", () => {
            count.value += 1;
        });

        document.getElementById("decrement")?.addEventListener("click", () => {
            count.value -= 1;
        });
    }
}

/** Компонент списка задач */
class TaskList extends Component {
    template(): string {
        return `
            <div>
                <h2>Список задач</h2>
                <ul>
                    ${tasks.value.map(task => `<li>${task}</li>`).join("")}
                </ul>
                <input type="text" id="taskInput" placeholder="Новая задача" />
                <button id="addTask">Добавить задачу</button>
            </div>
        `;
    }

    protected afterRender() {
        const taskInput = document.getElementById("taskInput") as HTMLInputElement;
        const addTaskButton = document.getElementById("addTask");

        addTaskButton?.addEventListener("click", () => {
            if (taskInput.value.trim() !== "") {
                tasks.value = [...tasks.value, taskInput.value];
                taskInput.value = ""; // Очищаем поле ввода
            }
        });
    }
}

/** Главный компонент приложения */
class App extends Component {
    template(): string {
        return `
            <div>
                <h1>Добро пожаловать в K-Fork App</h1>
                <div id="counter"></div>
                <div id="taskList"></div>
            </div>
        `;
    }

    protected afterRender() {
        // Инициализируем дочерние компоненты
        const counterRoot = document.getElementById("counter")!;
        const taskListRoot = document.getElementById("taskList")!;

        const counter = new Counter(counterRoot);
        const taskList = new TaskList(taskListRoot);

        // Подписываем компоненты на изменения состояния
        counter.observe(count);
        taskList.observe(tasks);

        // Рендерим дочерние компоненты
        counter.render();
        taskList.render();
    }
}

// Инициализация приложения
const appRoot = document.getElementById("app")!;
const app = new App(appRoot);
app.render();
