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

ALLOWED_STATUSES = ["pending", "in-progress", "done"] 
ALLOWED_PRIORITIES = ["low", "medium", "high"]
ALLOWED_SORT_FIELDS = ["created_at", "due_date", "priority"]

def validate_date(due_date): 
    if not due_date:
        return None
    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format (YYYY-MM-DD)"
    return None
    
def validate_priority(priority): 
    if priority not in ALLOWED_PRIORITIES: 
        return "Invalid priority"
    return None 

def validate_status(status): 
    if status and status not in ALLOWED_STATUSES:
         return "Invalid status" 
    return None
    
def validate_json(data): 
    if not data:
         return "Invalid JSON body" 
    return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header: 
            return jsonify({'error': 'Token is missing'}), 401

        try: token = auth_header.split(" ")[1] 
        except IndexError: 
            return jsonify({'error': 'Invalid token format'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id'] 
        except jwt.ExpiredSignatureError: 
            return jsonify({'error': 'Token expired'}), 401 
        except jwt.InvalidTokenError: 
            return jsonify({'error': 'Invalid token'}), 401 
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
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 10, type=int)
            sort = request.args.get("sort")
            tag = request.args.get("tag")
            error = validate_status(status) 
            if error: 
                return jsonify({"error": error}), 400
            
            if page < 1 or limit < 1:
                return jsonify({"error": "Page and limit must be positive"}), 400
            
            if limit > 100: 
                limit = 100
            
            if sort not in ALLOWED_SORT_FIELDS:
                sort = "created_at"

            offset = (page - 1) * limit
            
            tasks = get_tasks_by_user(user_id, status, limit, offset, sort, tag)
            return jsonify({ 
                "page": page,
                "limit": limit, 
                "tasks": tasks 
                }), 200

        if request.method == 'POST':
            data = request.get_json(silent=True)
            error = validate_json(data) 
            if error: 
                return jsonify({"error": error}), 400
            
            title = data.get("title")
            due_date = data.get("due_date")
            priority = data.get("priority", "medium")
            subject=data.get("subject")
            tag = data.get("tag")

            if not title or title.strip() == "":
                return jsonify({
                    "error": "Task title is required"
                }), 400
            
            if subject is not None and subject.strip() == "":
                return jsonify({"error": "Subject cannot be empty"}), 400
            
            if tag is not None and not isinstance(tag, list):
                return jsonify({"error": "Tag must be a list"}), 400
            
            error = validate_priority(priority) 
            if error:
                 return jsonify({"error": error}), 400 
            
            error = validate_date(due_date) 
            if error:
                return jsonify({"error": error}), 400

            new_task = add_task(title,user_id,due_date, priority,subject,tag)
            return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT','PATCH'])
@token_required
def update_task_route(user_id,task_id):
    data = request.get_json(silent=True)
    error = validate_json(data)
    if error:
        return jsonify({"error": error}), 400
    
    title = data.get("title")
    status = data.get("status")
    due_date = data.get("due_date")
    priority = data.get("priority")
    subject=data.get("subject")
    tag = data.get("tag")

    if subject is not None and subject.strip() == "":
        return jsonify({"error": "Subject cannot be empty"}), 400

    if all(v is None for v in [title, status, due_date, priority, subject,tag]):
        return jsonify({
            "error": "Nothing to update"
        }), 400

    error = validate_status(status)
    if error:
        return jsonify({"error": error}), 400 
    
    error = validate_priority(priority) if priority else None 
    if error: 
        return jsonify({"error": error}), 400 
    
    error = validate_date(due_date) 
    if error:
        return jsonify({"error": error}), 400
    
    if tag is not None and not isinstance(tag, list):
        return jsonify({"error": "Tag must be a list"}), 400
    
    updated = update_task(task_id, user_id, title, status, due_date, priority, subject, tag)

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
    data=request.get_json(silent=True)
    error = validate_json(data) 
    if error: 
        return jsonify({"error": error}), 400

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
    data=request.get_json(silent=True)
    error = validate_json(data) 
    if error:
        return jsonify({"error": error}), 400

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