from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    new_task = request.form['new_task']
    tasks = load_tasks()
    tasks.append({'task': new_task, 'done': False})
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/done/<int:task_index>')
def mark_done(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        tasks[task_index - 1]['done'] = True
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
