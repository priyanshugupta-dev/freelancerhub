from flask import Flask, render_template, request, redirect, session, jsonify
import smtplib
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

# In-memory storage for users and jobs
users = []
jobs = []

# Load users (from memory)
def load_users():
    return users

# Save users (to memory)
def save_user(new_user):
    users.append(new_user)

# Load jobs (from memory)
def load_jobs():
    return jobs

# Save jobs (to memory)
def save_job(new_job):
    jobs.append(new_job)

# Home Route
@app.route("/", methods=['GET', 'POST', 'PUT']) # decorator
def home(): # route handler function
    # returning a response
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        myEmail = 'sahpriyanshu2012@gmail.com'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Warm regards from Aman"
        msg['From'] = myEmail
        msg['To'] = email
        
       # Create the body of the message (a plain-text and an HTML version).

        with open("templates/contact.html", encoding='utf-8-sig') as myfile:
            outerdata=myfile.read()
            template = Template(outerdata)
            mainpage=template.render(firstName = name,body = message)
        # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = mainpage

       # Record the MIME types of both parts - text/plain and text/html.
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

       # Attach parts into message container.
       # According to RFC 2046, the last part of a multipart message, in this case
       # the HTML message, is best and preferred.
        # msg.attach(part1)
        msg.attach(part2)

       # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(myEmail, 'egew wyph oigl xgsm')
        mail.sendmail(myEmail, email, msg.as_string())
        mail.quit()
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/get-jobs')
def get_jobs():
    return jsonify(load_jobs())  # Return in-memory jobs

@app.route('/post-job', methods=["GET", "POST"])
def post_job():
    if "user" not in session:
        return redirect("/login")  # Redirect if not logged in

    # Get logged-in user details
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
            "poster": poster_name  # Store logged-in user's full name
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

    # Check if user already exists
    if any(user["email"] == email for user in users):
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

    # Validate user credentials
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
