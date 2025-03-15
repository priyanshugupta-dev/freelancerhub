from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

USER_FILE = "static/user.json"
DASHBOARD_FILE = "static/dashboard.json"

# Load users from user.json
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            content = file.read()
            return json.loads(content) if content else []
    return []

# Save users to user.json
def save_user(new_user):
    users = load_users()
    users.append(new_user)
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

def load_jobs():
    if os.path.exists("dashboard.json"):
        with open(DASHBOARD_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save jobs to dashboard.json
def save_job(new_job):
    jobs = load_jobs()
    jobs.append(new_job)
    with open(DASHBOARD_FILE, "w") as file:
        json.dump(jobs, file, indent=4)


# Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-jobs')
def get_jobs():
    try:
        with open(DASHBOARD_FILE, "r") as file:
            jobs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        jobs = []  # Return empty list if file not found or corrupt

    return jsonify(jobs)

@app.route('/post-job', methods=["GET", "POST"])
def post_job():
    if "user" not in session:
        return redirect("/login")  # Redirect if not logged in
    
    users = load_users()
    current_user_email = session["user"]
    current_user = next((u for u in users if u["email"] == current_user_email), None)
    poster_name = current_user["name"] if current_user else "Unknown"

    if request.method == "GET":
        return render_template('postjob.html')

    elif request.method == "POST":
        data = request.json
        if not data or "title" not in data or "description" not in data or "budget" not in data:
            return jsonify({"success": False, "message": "Invalid job data"}), 400

        new_job = {
            "title": data["title"],
            "description": data["description"],
            "budget": data["budget"],
            "poster": poster_name # Store logged-in user as the poster
        }

        save_job(new_job)
        return jsonify({"success": True, "message": "Job posted successfully!"})

# Signup Route
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'GET':
        return render_template('signup.html')
    
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    
    # Check if user already exists
    for user in users:
        if user["email"] == email:
            return jsonify({"success": False, "message": "Email already registered!"})
    
    new_user = {"name": name, "email": email, "password": password}
    save_user(new_user)

    return jsonify({"success": True, "message": "User registered successfully!"})

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.json
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    for user in users:
        if user["email"] == email and user["password"] == password:
            session["user"] = user["email"]  # Store user session
            return jsonify({"success": True, "message": "Login successful!", "redirect": "/dashboard"})
    
    return jsonify({"success": False, "message": "Invalid credentials! Please try again."})

# Dashboard Route (Restricted to Logged-in Users)
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect("/login")  # Redirect if not logged in
    
    return render_template('dashboard.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop("user", None)  # Remove session
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
