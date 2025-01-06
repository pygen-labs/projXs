from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'pygen-and-co-8113261-2024-projXs'

# Google Apps Script URL
GSHEET_URL = "https://script.google.com/macros/s/AKfycbykSer38aeWUFsyOfVkEv4ul7kJrz2DZhk85WX-GpkIuncRs53kaoiF1jpLuBYU2g/exec"

# Function to send POST requests to the Google Apps Script API
def send_post_request(action, params):
    data = {
        'action': action,
        **params
    }
    response = requests.post(GSHEET_URL, json=data)
    if action == 'get_projects':
        return response.json()
    return response.json()
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
    
@app.route('/')
def index():
    # Redirect to login/signup page if not logged in
    if 'username' not in session:
        return render_template('index.html', logged_in=False)
    return redirect(url_for('main_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    params = {
        'email': email,
        'password': password
    }
    result = send_post_request('login', params)
    if 'Login successful!' in result['result']:
        session['username'] = email  # Store email in session
        return redirect(url_for('main_page'))
    return jsonify(result)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    params = {
        'username': username,
        'email': email,
        'password': password
    }
    result = send_post_request('signup', params)
    if 'Signup successful!' in result['result']:
        session['username'] = email  # Store email in session
        return redirect(url_for('main_page'))
    return jsonify(result)

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    params = {
        'username': username
    }
    projects = send_post_request('get_projects', params).get('projects', [])

    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']
        params = {
            'username': username,
            'title': title,
            'note': note,
        }
        result = send_post_request('addProject', params)
        # Return a JSON response with success status
        return jsonify({"success": True})

    return render_template('main.html', username=username, projects=projects)

@app.route('/terms.html')
def terms():
    return render_template('terms.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
