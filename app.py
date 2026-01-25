from flask import Flask, jsonify,request
from db import get_tasks_by_user, add_task
from db import update_task 
from db import delete_task
from db import create_user
from db import get_user_by_username
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps
from config import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
        except:
            return jsonify({'error': 'Invalid or expired token'}), 401

        return f(user_id, *args, **kwargs)

    return decorated

@app.route('/')
def home():
    return "student task manager API running"

@app.route('/tasks', methods=['GET', 'POST'])
@token_required
def handle_tasks(user_id):

        if request.method=='GET':
            status = request.args.get("status")  
            tasks = get_tasks_by_user(user_id, status)

            return jsonify(tasks), 200

        if request.method == 'POST':
            data = request.get_json()
            title = data.get("title")
            due_date = data.get("due_date")
            priority = data.get("priority", "medium")
            subject=data.get("subject")

            if priority not in ["low", "medium", "high"]:
                return jsonify({"error": "Invalid priority"}), 400

            if not title or title.strip() == "":
                return jsonify({
                    "error": "Task title is required"
                }), 400

            new_task = add_task(title,user_id,due_date, priority,subject)
            return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task_route(user_id,task_id):
    data = request.get_json()
    ALLOWED_STATUSES = ["pending", "in-progress", "done"]
    ALLOWED_PRIORITIES = ["low", "medium", "high"]
    title = data.get("title")
    status = data.get("status")
    due_date = data.get("due_date")
    priority = data.get("priority")
    subject=data.get("subject")

    if not title and not status and not due_date and not priority and not subject:
        return jsonify({
            "error": "Nothing to update"
        }), 400

    if status and status not in ALLOWED_STATUSES:
        return jsonify({
            "error": "Status is required"
        }), 400
    
    if priority and priority not in ALLOWED_PRIORITIES:
        return jsonify({
            "error": "Invalid priority. Allowed: low, medium, high"
        }), 400

    updated = update_task(task_id, user_id, title, status, due_date, priority,subject)

    if updated == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task updated successfully"
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task_route(user_id,task_id):
    deleted = delete_task(task_id,user_id)

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
    

    user=get_user_by_username(username)

    if user is None:
        return jsonify({
            "error":"user not exist"
        }),404
    
    if not check_password_hash(user[2],password):
        return jsonify({
            "error":"password incorrect"
        }),401
    
    token=jwt.encode({
        "user_id":user[0],
        "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=1)
    },app.config['SECRET_KEY'],algorithm="HS256"
    )
    
    return jsonify({
        "token":token
    })
    

if __name__=='__main__':
    app.run(debug=True)