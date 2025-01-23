from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'pygen-and-co-8113261-2024-projXs'  # Replace with an environment variable in production

# Google Apps Script URL (replace with your actual URL)
GSHEET_URL = "https://script.google.com/macros/s/AKfycbykSer38aeWUFsyOfVkEv4ul7kJrz2DZhk85WX-GpkIuncRs53kaoiF1jpLuBYU2g/exec"


# Function to send POST requests to the Google Apps Script API
def send_post_request(action, params):
    try:
        data = {'action': action, **params}
        response = requests.post(GSHEET_URL, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending POST request: {e}")
        return {"result": "error", "message": "Failed to connect to the API."}


# Get the latest user activity data
def get_user_activity():
    try:
        response = requests.get(GSHEET_URL)
        response.raise_for_status()
        data = response.json().get("data", [])
        if not data:
            return []

        # Group data by "Username" and count the notes
        user_activity = {}
        for item in data:
            username = item.get("Username")
            if username and item.get("Title"):
                user_activity[username] = user_activity.get(username, 0) + 1

        # Apply activity labels
        activity_data = []
        for username, total_notes in user_activity.items():
            activity_level = activity_label(total_notes)
            activity_data.append({
                "Username": username,
                "TotalNotes": total_notes,
                "ActivityLevel": activity_level
            })

        return activity_data

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching user activity: {e}")
        return []


# Route: Index Page
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main_page'))
    return render_template('index.html', logged_in=False, terms_url=url_for('terms'), doc_url=url_for('documentation'))


# Route: Terms and Conditions Page
@app.route('/terms')
def terms():
    return render_template('terms.html')


# Route: Documentation Page
@app.route('/documentation')
def documentation():
    return render_template('doc-projxs.html')


# Route: Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    params = {'email': email, 'password': password}
    result = send_post_request('login', params)
    if result.get('result') == 'Login successful!':
        session['username'] = email
        return redirect(url_for('main_page'))
    return jsonify(result)


# Route: Signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    params = {'username': username, 'email': email, 'password': password}
    result = send_post_request('signup', params)
    if result.get('result') == 'Signup successful!':
        session['username'] = email
        return redirect(url_for('main_page'))
    return jsonify(result)


# Route: Main Page
@app.route('/main', methods=['GET', 'POST'])
def main_page():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']

    # Handle new project addition
    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']
        params = {'username': username, 'title': title, 'note': note}
        result = send_post_request('addProject', params)
        return jsonify(result)

    # Fetch user projects and activity data
    user_projects = send_post_request('get_projects', {'username': username}).get('projects', [])
    user_activity = get_user_activity()

    # Get user-specific activity data
    user_data = next((item for item in user_activity if item["Username"] == username), None)

    if user_data:
        user_status = user_data["ActivityLevel"]
        total_notes = user_data["TotalNotes"]
    else:
        user_status = "Getting Started"
        total_notes = 0

    motivational_message = get_motivational_message(user_status, total_notes)

    return render_template(
        'main.html',
        username=username,
        projects=user_projects,
        user_status=user_status,
        motivational_message=motivational_message,
        terms_url=url_for('terms'),
        doc_url=url_for('documentation')
    )


# Helper Function: Get Motivational Message
def get_motivational_message(user_status, total_notes):
    messages = {
        "Most Active": f"Fantastic job! You're a leader on the Productivity Champion leaderboard with {total_notes} notes! 🏆",
        "Moderately Active": f"You're doing great! Keep it up to reach the top ranks. You've added {total_notes} notes so far. 🚀",
        "Getting Started": f"Don't miss out! Start adding notes to unlock your full potential. You have {total_notes} notes. 💪",
    }
    return messages.get(user_status, "Keep going! Every step counts.")


# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def activity_label(note_count):
    if note_count > 10:
        return "Most Active"
    elif 5 <= note_count <= 10:
        return "Moderately Active"
    return "Getting Started"


if __name__ == "__main__":
    app.run()
