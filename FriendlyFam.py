# To activate environment use: .\.venv\Scripts\activate
# To deactivate environment use: deactivate
# To run: run in terminal and don't use the play button.
# Run command:  python .\FriendlyFam.py
# What does this command mean: .\.venv\Scripts\activate
#                               in the current folder, go into the .venv folder, then go to Scripts folder, then run the activate program.
from flask import Flask, render_template, request, session, flash, redirect, url_for
import os
from db import init_db, Login, Event, User

app = Flask(__name__)
app.secret_key = 'yay'

init_db()

@app.route('/')
def home():
    events = Event.get_all()
    print(events)
    return render_template('home.html', list=events, user=session.get('user'))

@app.route('/myevents')
def myevents():
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

    host = session['user']
    events = Event.get_by_host(host)
    return render_template('myevents.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        result = add_event_to_db(session['user'], request.form)
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for('home'))
        else:
            flash(result["message"], "danger")
            return render_template('add.html')
    
    return render_template('add.html')

def add_event_to_db(host, form_data):
    try:
        description = form_data['description']
        day = form_data['day']
        time = form_data['time']
        Event.add(host, description, day, time) 
        return {"success": True, "message": "Event added successfully!"}
    except Exception as e:
        print(f"Error adding event: {e}")
        return {"success": False, "message": f"Error adding event: {e}"}
    
@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

    event = Event.get_by_id(event_id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        description = request.form['description']
        day = request.form['day']
        time = request.form['time']
        Event.update(event_id, description, day, time)
        flash("Event updated successfully!", "success")
        return redirect(url_for('myevents')) 

    return render_template('edit.html', event=event)

@app.route('/delete/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

    try:
        Event.delete(event_id)
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the event.', 'danger')
        print(f"Error deleting event: {e}")

    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Login.get_by_username(username)
        
        if user and user['password'] == password: 
            session['user'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        flash("Invalid username or password.", "danger")
    return render_template('index.html', username=session.get('user'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash("Passwords don't match!", "danger")
            return render_template("signup.html")

        existing_user = User.get_by_username(username)
        if existing_user:
            flash("Username already taken.", "danger")
            return render_template("signup.html")

        User.add(username, password)
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)