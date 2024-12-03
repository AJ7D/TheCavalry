import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load user data from user.json
def load_user_data():
    with open('user.json', 'r') as f:
        return json.load(f)

# Save user data back to user.json
def save_user_data(data):
    with open('user.json', 'w') as f:
        json.dump(data, f, indent=4)

# Load plan data from data.json
def load_plan_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# Save plan data back to data.json
def save_plan_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Load rewards data from data.json
def load_rewards_data():
    with open('rewards.json', 'r') as f:
        return json.load(f)

# Save rewards data back to data.json
def save_rewards_data(data):
    with open('rewards.json', 'w') as f:
        json.dump(data, f, indent=4)

# Load challenge data from challenges.json
def load_challenges_data():
    with open('challenges.json', 'r') as f:
        return json.load(f)

# Save challenge data back to challenges.json
def save_challenges_data(data):
    with open('challenges.json', 'w') as f:
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

# Index route (Dashboard)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['username']
    user_data = load_user_data()
    plans_data = load_plan_data()

    # Get the logged-in user's data
    user = next((u for u in user_data if u['username'] == username), None)
    if user:
        user_plans = next((item['plans'] for item in plans_data if item['username'] == username), [])
        total_savings = sum(plan.get('locked', 0) for plan in user_plans)
        return render_template('index.html', user=user, plans=user_plans, total_savings=total_savings)
    return redirect(url_for('login'))

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
            plan_to_view['locked'] += lock_amount
            user['amount'] -= lock_amount  # Decrease user's available amount
            flash(f"{lock_amount} has been locked into your plan.", "success")
        
        # Unlock Funds
        if unlock_amount > 0 and unlock_amount <= plan_to_view['locked']:
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

# Delete plan route
@app.route('/delete_plan/<int:plan_id>', methods=['POST'])
def delete_plan(plan_id):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    username = session['username']
    plans_data = load_plan_data()

    # Find the user's plans
    user_plans = next((item['plans'] for item in plans_data if item['username'] == username), None)
    if user_plans:
        # Remove the plan by plan_id
        plans_data = [plan for plan in user_plans if plan['plan_id'] != plan_id]
        save_plan_data(plans_data)  # Save updated plan data

        flash('Plan deleted successfully!', 'success')
    else:
        flash('Error: Plan not found.', 'danger')

    return redirect(url_for('index'))

# Challenges route
@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['username']
    user_data = load_user_data()
    plans_data = load_plan_data()
    challenges_data = load_challenges_data()

    # Find the user's data
    user = next((u for u in user_data if u['username'] == username), None)

    # Sum the total savings (locked funds) across the user's plans
    total_savings = sum(plan.get('locked', 0) for plan in plans_data if plan['username'] == username)

    # Update challenges based on savings
    for challenge in challenges_data:
        if challenge['type'] == 'savings' and total_savings >= challenge['goal'] and not challenge['claimed']:
            challenge['completed'] = True

    if request.method == 'POST':
        # Handle challenge claiming (if points are available)
        challenge_id = int(request.form['challenge_id'])
        challenge = next((ch for ch in challenges_data if ch['id'] == challenge_id), None)

        if challenge and challenge['completed'] and not challenge['claimed']:
            user['points'] += challenge['points']
            challenge['claimed'] = True
            save_user_data(user_data)  # Save user data (points)
            save_challenges_data(challenges_data)  # Save challenges state (claimed)
            flash(f"Congratulations! You've unlocked {challenge['points']} points for completing the challenge.", "success")
        else:
            flash("You haven't completed this challenge yet or you've already claimed the reward.", "danger")

    return render_template('challenges.html', user=user, challenges=challenges_data, total_savings=total_savings)
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

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
