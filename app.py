from flask import Flask, jsonify,request
from db import get_tasks_by_user, add_task
from db import update_task_status
from db import delete_task
from db import create_user
from db import login_user

app=Flask(__name__)

@app.route('/')
def home():
    return "student task manager API running"

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    data=request.get_json()
    user_id=data.get("user_id")

    if not user_id:
        return jsonify({
            "error":"User id required"
        }),400

    if request.method == 'GET':
        return jsonify(get_tasks_by_user(user_id))

    if request.method == 'POST':
        data = request.get_json()

        title = data.get("title")

        if not title or title.strip() == "":
            return jsonify({
                "error": "Task title is required"
            }), 400

        new_task = add_task(title,user_id)
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

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()

    username=data.get('username')
    password=data.get('password')

    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }),400
    
    user_id=create_user(username,password)

    if user_id is None:
        return jsonify({
            "error":"username already exist"
        }),409
    
    return jsonify({
        "message":"registration successful",
        "user_id":user_id
    }),201

@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()

    username=data.get('username')
    password=data.get('password')

    if not username or not password:
        return jsonify({
            "error":"username and password are required"
        }),400
    
    user=login_user(username)

    if user is None:
        return jsonify({
            "error":"user not exist"
        }),404
    
    if user[2]!=password:
        return jsonify({
            "error":"password incorrect"
        })
    
    return jsonify({
        "message":"Login Successful",
        "user_id":user[0]
    }),200
    

if __name__=='__main__':
    app.run(debug=True)