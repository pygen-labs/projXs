# from flask import Flask, render_template, request, jsonify, session, redirect, url_for
# import requests
# import pandas as pd

# app = Flask(__name__)
# app.secret_key = 'pygen-and-co-8113261-2024-projXs'

# # Google Apps Script URL
# GSHEET_URL = "https://script.google.com/macros/s/AKfycbyvtHc34HgLZ7IKCUT-57cuXrAlp53RhDM4pOCAyjm8Z17iJ6Rrgw1lvBVRxlnqTbs/exec"

# # Helper function for sending POST requests
# def send_post_request(action, params):
#     data = {'action': action, **params}
#     response = requests.post(GSHEET_URL, json=data)
#     return response.json()

# @app.route('/')
# def index():
#     if 'username' not in session:
#         return render_template('index.html', logged_in=False)
#     return redirect(url_for('main_page'))

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['email']
#     password = request.form['password']
#     params = {'email': email, 'password': password}
#     result = send_post_request('login', params)

#     if 'Login successful!' in result['result']:
#         session['username'] = email
#         return redirect(url_for('main_page'))

#     return jsonify(result)

# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     params = {'username': username, 'email': email, 'password': password}
#     result = send_post_request('signup', params)

#     if 'Signup successful!' in result['result']:
#         session['username'] = email
#         return redirect(url_for('main_page'))

#     return jsonify(result)

# @app.route('/main', methods=['GET', 'POST'])
# def main_page():
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     username = session['username']
#     params = {'username': username}
#     projects = send_post_request('get_projects', params).get('projects', [])

#     if request.method == 'POST':
#         action = request.form.get('action', 'addProject')
        
#         if action == 'addProject':
#             title = request.form['title']
#             note = request.form['note']
#             params = {'username': username, 'title': title, 'note': note}
#             result = send_post_request('addProject', params)
#             return jsonify({"success": True})
        
#         elif action == 'deleteProject':
#             title = request.form['title']
#             params = {'username': username, 'title': title}
#             result = send_post_request('deleteProject', params)
#             return jsonify({"success": True, "result": result})
        
#         elif action == 'editProject':
#             old_title = request.form['oldTitle']
#             new_title = request.form['newTitle']
#             new_note = request.form['newNote']
#             params = {'username': username, 'oldTitle': old_title, 'newTitle': new_title, 'newNote': new_note}
#             result = send_post_request('editProject', params)
#             return jsonify({"success": True, "result": result})

#     user_activity = get_user_activity()
#     user_data = user_activity[user_activity["Username"] == username]
#     if not user_data.empty:
#         user_status = user_data["ActivityLevel"].values[0]
#         total_notes = user_data["TotalNotes"].values[0]
#     else:
#         user_status = "Getting Started"
#         total_notes = 0

#     motivational_message = get_motivational_message(user_status, total_notes)

#     return render_template(
#         'main.html',
#         username=username,
#         projects=projects,
#         user_status=user_status,
#         motivational_message=motivational_message
#     )

# def get_user_activity():
#     response = requests.get(GSHEET_URL)
#     data = response.json()["data"]
#     df = pd.DataFrame(data)
#     # Only count non-deleted projects
#     df = df[(df["Title"] != "") & (df["Status"] != "Deleted")]
#     user_activity = df.groupby("Username").size().reset_index(name="TotalNotes")

#     def activity_label(note_count):
#         if note_count > 10:
#             return "Most Active"
#         elif 5 <= note_count <= 10:
#             return "Moderately Active"
#         else:
#             return "Getting Started"

#     user_activity["ActivityLevel"] = user_activity["TotalNotes"].apply(activity_label)
#     return user_activity

# def get_motivational_message(user_status, total_notes):
#     messages = {
#         "Most Active": f"Fantastic job! You're a leader on the Productivity Champion leaderboard with {total_notes} notes! 🏆",
#         "Moderately Active": f"You're doing great! Keep it up to reach the top ranks. You've added {total_notes} notes so far. 🚀",
#         "Getting Started": f"Don't miss out! Start adding notes to unlock your full potential. You have {total_notes} notes. 💪",
#     }
#     return messages.get(user_status, "Keep going!")

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
# @app.route('/pricing')
# def pricing():
#     return render_template('pricing.html')
# if __name__ == "__main__":
#     # app.run(debug=False, port=5000, host='0.0.0.0')
#     app.run()

# -----------

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import pandas as pd

app = Flask(__name__)
app.secret_key = 'pygen-and-co-8113261-2024-projXs'

# Google Apps Script URL
GSHEET_URL = "https://script.google.com/macros/s/AKfycbyvtHc34HgLZ7IKCUT-57cuXrAlp53RhDM4pOCAyjm8Z17iJ6Rrgw1lvBVRxlnqTbs/exec"

# Early Access Email
EARLY_ACCESS_EMAILS = ["yawark498@gmail.com", "ameerhamza.khan@pygen.co", "tubabshr@gmail.com"]

# Helper function for sending POST requests
def send_post_request(action, params):
    data = {'action': action, **params}
    response = requests.post(GSHEET_URL, json=data)
    return response.json()

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('index.html', logged_in=False)
    return redirect(url_for('main_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    params = {'email': email, 'password': password}
    result = send_post_request('login', params)

    if 'Login successful!' in result['result']:
        session['username'] = email  # Store user session
        return redirect(url_for('main_page'))

    return jsonify(result)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    params = {'username': username, 'email': email, 'password': password}
    result = send_post_request('signup', params)

    if 'Signup successful!' in result['result']:
        session['username'] = email
        return redirect(url_for('main_page'))

    return jsonify(result)

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    params = {'username': username}
    projects = send_post_request('get_projects', params).get('projects', [])

    if request.method == 'POST':
        action = request.form.get('action', 'addProject')
        
        if action == 'addProject':
            title = request.form['title']
            note = request.form['note']
            params = {'username': username, 'title': title, 'note': note}
            result = send_post_request('addProject', params)
            return jsonify({"success": True})
        
        elif action == 'deleteProject':
            title = request.form['title']
            params = {'username': username, 'title': title}
            result = send_post_request('deleteProject', params)
            return jsonify({"success": True, "result": result})
        
        elif action == 'editProject':
            old_title = request.form['oldTitle']
            new_title = request.form['newTitle']
            new_note = request.form['newNote']
            params = {'username': username, 'oldTitle': old_title, 'newTitle': new_title, 'newNote': new_note}
            result = send_post_request('editProject', params)
            return jsonify({"success": True, "result": result})

    user_activity = get_user_activity()
    user_data = user_activity[user_activity["Username"] == username]
    
    if not user_data.empty:
        user_status = user_data["ActivityLevel"].values[0]
        total_notes = user_data["TotalNotes"].values[0]
    else:
        user_status = "Getting Started"
        total_notes = 0

    motivational_message = get_motivational_message(user_status, total_notes)

    # Check if user has early access
    if username in EARLY_ACCESS_EMAILS:
        return render_template(
            'main2.html',  # Early access page
            username=username,
            projects=projects,
            user_status=user_status,
            motivational_message=motivational_message
        )
    else:
        return render_template(
            'main.html',  # Normal version
            username=username,
            projects=projects,
            user_status=user_status,
            motivational_message=motivational_message
        )

def get_user_activity():
    response = requests.get(GSHEET_URL)
    data = response.json()["data"]
    df = pd.DataFrame(data)
    df = df[(df["Title"] != "") & (df["Status"] != "Deleted")]
    user_activity = df.groupby("Username").size().reset_index(name="TotalNotes")

    def activity_label(note_count):
        if note_count > 10:
            return "Most Active"
        elif 5 <= note_count <= 10:
            return "Moderately Active"
        else:
            return "Getting Started"

    user_activity["ActivityLevel"] = user_activity["TotalNotes"].apply(activity_label)
    return user_activity

def get_motivational_message(user_status, total_notes):
    messages = {
        "Most Active": f"Fantastic job! You're a leader on the Productivity Champion leaderboard with {total_notes} notes! 🏆",
        "Moderately Active": f"You're doing great! Keep it up to reach the top ranks. You've added {total_notes} notes so far. 🚀",
        "Getting Started": f"Don't miss out! Start adding notes to unlock your full potential. You have {total_notes} notes. 💪",
    }
    return messages.get(user_status, "Keep going!")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == "__main__":
    app.run()