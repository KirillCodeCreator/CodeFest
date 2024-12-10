import { Reactive } from "./reactive";

/** Базовый компонент */
abstract class Component {
    private root: HTMLElement;
    private reactiveDependencies: Reactive<any>[] = [];

    constructor(root: HTMLElement) {
        this.root = root;
    }

    protected observe(reactive: Reactive<any>) {
        reactive.subscribe(() => this.render());
        this.reactiveDependencies.push(reactive);
    }

    abstract template(): string;

    render() {
        this.root.innerHTML = this.template();
        this.afterRender();
    }

    protected afterRender() {
        // Для обработки событий (переопределяется в наследниках)
    }
}

export { Component };
