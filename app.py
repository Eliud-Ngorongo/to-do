from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__, static_url_path='/static')

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
    tasks.insert(0, {'task': new_task, 'done': False})
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/done/<int:task_index>')
# Update the 'mark_done' route to move completed tasks to the dropdown
@app.route('/done/<int:task_index>')
def mark_done(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        completed_task = tasks.pop(task_index - 1)
        completed_task['done'] = True
        tasks.append(completed_task)
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/remove/<int:task_index>')
def remove(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        del tasks[task_index - 1]
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/hide/<int:task_index>')
def hide(task_index):
    tasks = load_tasks()
    if 1 <= task_index <= len(tasks):
        tasks[task_index - 1]['hidden'] = True
        save_tasks(tasks)
    return redirect(url_for('index'))
# New route to handle undo completion
@app.route('/undo_completion', methods=['POST'])
def undo_completion():
    completed_task = request.form.get('completed_task')
    tasks = load_tasks()
    
    for task in tasks:
        if task['task'] == completed_task and task['done']:
            task['done'] = False
            save_tasks(tasks)
            return redirect(url_for('index'))
    
    return 'Task not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
