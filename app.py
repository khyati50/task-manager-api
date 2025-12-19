from flask import Flask, jsonify,request
from db import get_all_tasks, add_task
from db import update_task_status,delete_task

app=Flask(__name__)

@app.route('/')
def home():
    return "student task manager API running"

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return jsonify(get_all_tasks())

    if request.method == 'POST':
        data = request.get_json()

        title = data.get("title")

        if not title or title.strip() == "":
            return jsonify({
                "error": "Task title is required"
            }), 400

        new_task = add_task(title)
        return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    status = data.get("status")

    if not status:
        return jsonify({
            "error": "Status is required"
        }), 400

    updated = update_task_status(task_id, status)

    if updated == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task updated successfully"
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    deleted = delete_task(task_id)

    if deleted == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


if __name__=='__main__':
    app.run(debug=True)