from flask import Flask, send_from_directory, jsonify, request, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import json


app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/data', methods=['POST'])
def post_data():
    # Get the data sent from the React app
    data = request.json  # This will automatically parse the JSON payload
    print(f"Received data: {data}")

    # Perform some processing if needed (e.g., saving to a database)
    
    # Send a response back to React
    return jsonify({"received": data['key']}), 200

@app.route('/api/buttons', methods=['GET'])
def get_buttons():
    # Map subjects to image filenames
    buttons = [
        {"subject": "Coffee", "imageSrc": "/static/images/coffee.png", "cost": 100},
        {"subject": "Voucher", "imageSrc": "/static/images/voucher.png", "cost": 500},
        {"subject": "Book", "imageSrc": "/static/images/book.png", "cost": 800},
        {"subject": "Disney+", "imageSrc": "/static/images/disney.png", "cost": 1000},
    ]
    return jsonify(buttons)


# Add route to serve React's static assets
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder + '/static', path)


# Load user data from user.json
def load_user_data():
    with open('user.json', 'r') as f:
        return json.load(f)


# Load plan data from data.json
@app.route('/static/plandata')
def load_plan_data():
    with open('data.json', 'r') as f:
        return json.load(f)


# Load challenges data from challenges.json
def load_challenges_data():
    with open('challenges.json', 'r') as f:
        return json.load(f)


# Load rewards data from rewards.json
def load_rewards_data():
    with open('rewards.json', 'r') as f:
        return json.load(f)


# Save user data back to user.json
def save_user_data(data):
    with open('user.json', 'w') as f:
        json.dump(data, f, indent=4)


# Save plan data back to data.json
def save_plan_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


# Save challenges data back to challenges.json
def save_challenges_data(data):
    with open('challenges.json', 'w') as f:
        json.dump(data, f, indent=4)


# Save rewards data back to rewards.json
def save_rewards_data(data):
    with open('rewards.json', 'w') as f:
        json.dump(data, f, indent=4)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = load_user_data()

        # Check user credentials
        user = next((u for u in user_data if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# Create new plan route
@app.route('/create_plan', methods=['GET', 'POST'])
def create_plan():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        target_amount = float(request.form['target_amount'])
        username = session['username']

        # Load plan data
        plans_data = load_plan_data()

        # Find the user's existing plans or create an empty list for them
        user_plans = next((item['plans'] for item in plans_data if item['username'] == username), None)
        if user_plans is None:
            user_plans = []
            plans_data.append({"username": username, "plans": user_plans})

        # Create a new plan
        new_plan = {
            "plan_id": len(user_plans) + 1,
            "title": title,
            "description": description,
            "target_amount": target_amount,
            "locked": 0
        }

        # Add the new plan to the user's plans
        user_plans.append(new_plan)

        # Save the updated plan data
        save_plan_data(plans_data)

        flash('New plan created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('create_plan.html')


# View and edit plan route
@app.route('/view_plan/<int:plan_id>', methods=['GET', 'POST'])
def view_plan(plan_id):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['username']
    user_data = load_user_data()
    plans_data = load_plan_data()

    # Find the logged-in user's data
    user = next((u for u in user_data if u['username'] == username), None)
    if not user:
        return redirect(url_for('login'))  # If user not found, redirect to login
    
    # Find the user's plans
    user_plans = next((item['plans'] for item in plans_data if item['username'] == username), [])
    plan_to_view = next((plan for plan in user_plans if plan['plan_id'] == plan_id), None)

    if request.method == 'POST':
        lock_amount = float(request.form['lock_amount']) if 'lock_amount' in request.form else 0
        unlock_amount = float(request.form['unlock_amount']) if 'unlock_amount' in request.form else 0
        
        # Lock Funds
        if lock_amount > 0 and lock_amount <= user['amount']:
            # Update the plan and user locked funds in the data.json file
            plan_to_view['locked'] += lock_amount
            user['amount'] -= lock_amount  # Decrease user's available amount
            
            flash(f"{lock_amount} has been locked into your plan.", "success")
        
        # Unlock Funds
        if unlock_amount > 0 and unlock_amount <= plan_to_view['locked']:
            # Update the plan and user locked funds in the data.json file
            plan_to_view['locked'] -= unlock_amount
            user['amount'] += unlock_amount  # Increase user's available amount
            
            flash(f"{unlock_amount} has been unlocked from your plan.", "success")
        else:
            flash('Invalid unlock amount. Please check the locked amount.', 'danger')

        # Save the updated user and plans data
        save_plan_data(plans_data)  # Save changes to data.json
        save_user_data(user_data)  # Save changes to user.json (just the user's amount)

        return redirect(url_for('index'))

    return render_template('view_plan.html', plan=plan_to_view, user_data=user)


# Challenges route
@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['username']
    user_data = load_user_data()
    challenges_data = load_challenges_data()
    plans_data = load_plan_data()

    # Find the logged-in user's data
    user = next((u for u in user_data if u['username'] == username), None)
    
    # Calculate total savings from user's locked funds
    total_savings = sum(plan['locked'] for plan in plans_data if plan['username'] == username)

    # Update challenge status (whether it's completed or not)
    for challenge in challenges_data:
        if challenge['type'] == 'savings':
            if total_savings >= challenge['goal']:
                challenge['completed'] = True
            else:
                challenge['completed'] = False

    # Handle challenge completion (reward points)
    if request.method == 'POST':
        challenge_id = int(request.form['challenge_id'])
        challenge = next((ch for ch in challenges_data if ch['id'] == challenge_id), None)

        if challenge and challenge['completed']:
            user['points'] += challenge['points']
            challenge['claimed'] = True  # Mark challenge as claimed
            save_user_data(user_data)
            save_challenges_data(challenges_data)
            flash(f"Congratulations! You've earned {challenge['points']} points!", "success")
        else:
            flash("You haven't completed this challenge yet.", "danger")

    return render_template('challenges.html', user=user, challenges=challenges_data)


# Rewards route
@app.route('/rewards', methods=['GET', 'POST'])
def rewards():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['username']
    user_data = load_user_data()
    rewards_data = load_rewards_data()

    # Get the logged-in user's data
    user = next((u for u in user_data if u['username'] == username), None)

    # Handle reward selection
    if request.method == 'POST':
        reward_id = int(request.form['reward_id'])
        reward = next((rw for rw in rewards_data if rw['id'] == reward_id), None)

        if reward and user['points'] >= reward['points']:
            user['points'] -= reward['points']
            flash(f"Congratulations! You've redeemed your {reward['name']} reward.", "success")
            save_user_data(user_data)
        else:
            flash("You don't have enough points for this reward.", "danger")

    return render_template('rewards.html', user=user, rewards=rewards_data)


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run()