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

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import requests
import pandas as pd
import json
from slugify import slugify

app = Flask(__name__)
app.secret_key = 'pygen-and-co-8113261-2024-projXs'

# Google Apps Script URL
GSHEET_URL = "https://script.google.com/macros/s/AKfycbzD4AEao4XGydzVjcsR95WKpyxjbnGvm27nTJ4NidgnHL6E3lZE3fWaz4Nroe0NE-M/exec"

# Early Access Email
EARLY_ACCESS_EMAILS = []

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
    
    if request.method == 'POST':
        action = request.form.get('action', 'addProject')
        
        if action == 'addProject':
            title = request.form['title']
            note = request.form['note']
            workspace = request.form.get('workspace', 'Default')
            params = {'username': username, 'title': title, 'note': note, 'workspace': workspace}
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
            workspace = request.form.get('workspace')
            params = {'username': username, 'oldTitle': old_title, 'newTitle': new_title, 'newNote': new_note}
            if workspace:
                params['workspace'] = workspace
            result = send_post_request('editProject', params)
            return jsonify({"success": True, "result": result})
            
        elif action == 'createWorkspace':
            workspace_name = request.form['workspaceName']
            params = {'username': username, 'workspaceName': workspace_name}
            result = send_post_request('createWorkspace', params)
            return jsonify({"success": True, "result": result})
            
        elif action == 'deleteWorkspace':
            workspace_name = request.form['workspaceName']
            params = {'username': username, 'workspaceName': workspace_name}
            result = send_post_request('deleteWorkspace', params)
            return jsonify({"success": True, "result": result})
            
        elif action == 'moveProjectToWorkspace':
            title = request.form['title']
            target_workspace = request.form['targetWorkspace']
            params = {'username': username, 'title': title, 'targetWorkspace': target_workspace}
            result = send_post_request('moveProjectToWorkspace', params)
            return jsonify({"success": True, "result": result})
            
        elif action == 'getWorkspaces':
            params = {'username': username}
            result = send_post_request('getWorkspaces', params)
            return jsonify({"success": True, "workspaces": result.get('result', [])})

    # Get projects
    params = {'username': username}
    projects_result = send_post_request('getProjects', params)
    projects = projects_result.get('result', [])
    
    # Get workspaces
    workspaces_result = send_post_request('getWorkspaces', params)
    workspaces = workspaces_result.get('result', [])
    
    # Convert workspaces to JSON for JavaScript
    workspaces_json = json.dumps(workspaces)

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
            'main3.html',  # Early access page
            username=username,
            projects=projects,
            workspaces=workspaces_json,
            user_status=user_status,
            motivational_message=motivational_message
        )
    else:
        return render_template(
            'main3.html',  # Normal version
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

@app.route('/test-404')
def test_404():
    # This route deliberately returns a 404 error to test your 404 page
    return render_template('404.html'), 404

# Register a custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    # This function will handle all 404 errors in your application
    return render_template('404.html'), 404

@app.route('/main/p/<slug>')
def shared_project(slug):
    # Fetch all projects for all users (or optimize as needed)
    response = requests.get(GSHEET_URL)
    data = response.json().get("data", [])
    # Find project by slugified title
    for project in data:
        if slugify(project.get("Title", "")) == slug:
            # Only show if not deleted
            if project.get("Status") != "Deleted":
                return render_template(
                    'shared_project.html',
                    title=project.get("Title", ""),
                    note=project.get("Note", ""),
                    workspace=project.get("Workspace", "Private"),
                    username=project.get("Username", "Unknown")
                )
    return abort(404)

from model import ask_chatnote

@app.route('/chatnote', methods=['POST'])
def chatnote():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    project_title = data.get('project')
    question = data.get('message')

    if not project_title or not question:
        return jsonify({"error": "Missing project title or message"}), 400

    username = session['username']
    projects_result = send_post_request('getProjects', {'username': username})
    projects = projects_result.get('result', [])

    if not projects:
        return jsonify({"error": "No projects found"}), 404

    # Find the project note for the given project title
    project_note = ""
    for p in projects:
        if isinstance(p, dict):
            db_title = p.get('Title', p.get('title', ''))
            if db_title and db_title.lower() == project_title.lower():
                project_note = p.get('Note', p.get('note', ''))
                break

    if not project_note:
        return jsonify({"error": "Project not found or empty"}), 404

    answer = ask_chatnote(question, project_note)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=False)