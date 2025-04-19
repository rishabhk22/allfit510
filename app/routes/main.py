from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.workout import WorkoutPlan

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/workout-plan', methods=['GET', 'POST'])
@login_required
def workout_plan():
    if request.method == 'POST':
        # Process workout plan generation
        goals = request.form.getlist('goals')
        fitness_level = request.form.get('fitness_level')
        available_time = request.form.get('available_time')
        
        # TODO: Implement workout plan generation logic
        flash('Workout plan generated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('workout_plan.html')

@bp.route('/progress')
@login_required
def progress():
    return render_template('progress.html') 