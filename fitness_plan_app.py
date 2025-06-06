import streamlit as st
import importlib
import re
import pandas as pd
import numpy as np
from datetime import datetime
from llm_prompt import build_prompt, call_llm_api
import calendar

# Page config
st.set_page_config(
    page_title="AllFit - Your Personal Fitness Planner",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .workout-distribution {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .distribution-warning {
        color: #dc3545;
        font-weight: bold;
    }
    .pie-container {
        position: relative;
        width: 300px;
        height: 300px;
        margin: 0 auto;
    }
    .pie-segment {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);
        transition: transform 0.3s ease;
    }
    .pie-segment:hover {
        cursor: pointer;
        filter: brightness(1.1);
    }
    .segment-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    /* Make sidebar wider */
    section[data-testid="stSidebar"] {
        min-width: 400px;
        max-width: 33vw;
        width: 33vw;
    }
    </style>
""", unsafe_allow_html=True)

def create_interactive_pie_chart(distribution):
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Workout Type': list(distribution.keys()),
        'Percentage': list(distribution.values())
    })
    
    # Calculate angles for each segment
    total = sum(distribution.values())
    if total != 100:
        # Normalize to 100%
        factor = 100 / total
        df['Percentage'] = df['Percentage'] * factor
    
    # Create the pie chart
    st.write("### Workout Distribution")
    
    # Create a container for the pie chart
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display the pie chart
            st.pie_chart(df.set_index('Workout Type'))
        
        with col2:
            # Display the current percentages
            st.write("Current Distribution:")
            for workout_type, percentage in distribution.items():
                st.metric(workout_type, f"{percentage:.1f}%")
            
            # Add a warning if total is not 100%
            total = sum(distribution.values())
            if abs(total - 100) > 0.1:
                st.error(f"Total: {total:.1f}% (Must equal 100%)")

def adjust_distribution(distribution, changed_key, new_value):
    old_value = distribution[changed_key]
    diff = new_value - old_value
    
    # Calculate how much to adjust other values
    other_keys = [k for k in distribution.keys() if k != changed_key]
    if not other_keys:
        return distribution
    
    # Distribute the difference proportionally
    total_others = sum(distribution[k] for k in other_keys)
    if total_others == 0:
        return distribution
    
    for key in other_keys:
        ratio = distribution[key] / total_others
        distribution[key] = max(0, min(100, distribution[key] - (diff * ratio)))
    
    # Ensure the changed value is set
    distribution[changed_key] = new_value
    
    # Normalize to ensure total is 100
    total = sum(distribution.values())
    if total != 100:
        factor = 100 / total
        for key in distribution:
            distribution[key] = round(distribution[key] * factor, 1)
    
    return distribution

# Helper to parse LLM response into structured sessions
def parse_llm_response(response):
    days = re.split(r'(?=Day \d+)', response)
    plan = []
    weekday_names = [day for day in calendar.day_name]
    for idx, day in enumerate(days):
        if not day.strip():
            continue
        lines = day.strip().split('\n')
        header = lines[0]
        focus = ''
        exercises = []
        duration = ''
        intensity = ''
        notes = []
        # Try to extract weekday from header
        weekday = None
        for wd in weekday_names:
            if wd.lower() in header.lower():
                weekday = wd
                break
        for line in lines[1:]:
            line = line.strip()
            if line.lower().startswith('focus'):
                focus = line.split(':', 1)[-1].strip()
            elif line.lower().startswith('duration'):
                duration = line.split(':', 1)[-1].strip()
            elif line.lower().startswith('intensity'):
                intensity = line.split(':', 1)[-1].strip()
            elif line.strip().startswith('-'):
                exercises.append(line.strip().lstrip('-').strip())
            elif line.strip().startswith('note:'):
                notes.append(line.strip().lstrip('note:').strip())
        plan.append({
            'header': header,
            'focus': focus,
            'exercises': exercises,
            'duration': duration,
            'intensity': intensity,
            'notes': notes,
            'weekday': weekday,
            'order': idx
        })
    return plan

def display_workout_plan(plan, days_per_week):
    weekdays = [day for day in calendar.day_name]
    # Build a mapping from weekday to session
    plan_by_day = {}
    # First, use explicit weekday if present
    for p in plan:
        if p['weekday']:
            plan_by_day[p['weekday']] = p
    # For any missing, assign in order
    used_orders = set(p['order'] for p in plan if p['weekday'])
    idx = 0
    for wd in weekdays:
        if wd not in plan_by_day:
            # Find next unused plan entry
            while idx < len(plan):
                if plan[idx]['order'] not in used_orders:
                    plan_by_day[wd] = plan[idx]
                    used_orders.add(plan[idx]['order'])
                    idx += 1
                    break
                idx += 1
    tabs = st.tabs(weekdays)
    for i, day in enumerate(weekdays):
        with tabs[i]:
            session = plan_by_day.get(day)
            if session and (session['exercises'] or session['focus'] or session['duration']):
                st.markdown(f"### {session['header']}")
                if session['focus']:
                    st.markdown(f"**Focus:** {session['focus']}")
                if session['exercises']:
                    exercises_df = pd.DataFrame({'Exercise': session['exercises']})
                    st.dataframe(exercises_df, use_container_width=True)
                st.markdown("### Session Details")
                if session['duration']:
                    st.markdown(f"**Duration:** {session['duration']}")
                if session['intensity']:
                    st.markdown(f"**Intensity:** {session['intensity']}")
                if session['notes']:
                    st.markdown("### Notes")
                    for note in session['notes']:
                        st.info(note)
            else:
                st.markdown(f"### {day}")
                st.success("Rest Day 💤")

# Main app
st.title("💪 AllFit - Your Personal Fitness Planner")

# Use a wide layout for results
results_placeholder = st.container()

# Sidebar for user inputs
with st.sidebar:
    st.header("Your Profile")
    
    with st.form("fitness_form"):
        st.subheader("Basic Information")
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=18)
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, step=0.1, value=80.0)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, step=1, value=180)
        
        st.subheader("Fitness Profile")
        fitness_level = st.selectbox(
            "Fitness Level",
            ["Beginner", "Intermediate", "Advanced", "Professional"]
        )
        
        fitness_goals = st.multiselect(
            "Fitness Goals",
            ["Weight Loss", "Muscle Gain", "Strength", "Flexibility", 
             "Mobility", "Endurance", "General Fitness", "Sports Performance",
             "Rehabilitation", "Stress Relief"]
        )
        
        # Workout Distribution Section
        st.subheader("Workout Distribution")
        st.markdown("""
            <div class="workout-distribution">
                Select your workout types, then assign a percentage to each. The total must always be 100%.
            </div>
        """, unsafe_allow_html=True)

        # User selects workout types
        all_types = ["Strength", "Flexibility", "Endurance", "Mobility", "HIIT", "Yoga", "Cardio", "Pilates", "Balance", "Agility"]
        selected_types = st.multiselect("Choose workout types:", all_types, default=["Strength", "Flexibility", "Endurance", "Mobility"])

        # Initialize session state for manual percentages
        if 'manual_distribution' not in st.session_state:
            st.session_state.manual_distribution = {}
        # Remove unselected types
        for k in list(st.session_state.manual_distribution.keys()):
            if k not in selected_types:
                del st.session_state.manual_distribution[k]
        # Add new types with equal split
        if selected_types:
            equal = round(100 / len(selected_types), 1)
            for k in selected_types:
                if k not in st.session_state.manual_distribution:
                    st.session_state.manual_distribution[k] = equal

        # Show a percentage input for each selected type
        total = 0
        for k in selected_types:
            st.session_state.manual_distribution[k] = st.number_input(
                f"{k} (%)", min_value=0, max_value=100, value=int(st.session_state.manual_distribution[k]), key=f"manual_{k}")
            total += st.session_state.manual_distribution[k]

        # Show the sum and warning if needed
        st.markdown(f"<b>Total: {total}%</b>", unsafe_allow_html=True)
        if total != 100:
            st.warning("The total must be exactly 100%.")

        st.subheader("Workout Preferences")
        days_per_week = st.slider("Days per week", 1, 7, 3)
        minutes_per_session = st.slider("Minutes per session", 10, 120, 30)
        
        preferred_workouts = st.multiselect(
            "Preferred Workout Types",
            ["Yoga", "Cardio", "Weight Training", "Calisthenics", "Stretching",
             "HIIT", "Pilates", "Swimming", "Cycling", "Running", "Dancing"]
        )
        
        equipment = st.select_slider(
            "Equipment Available",
            options=["No Equipment", "Basic (Dumbbells, Resistance Bands)", 
                    "Home Gym", "Full Gym Access"]
        )
        
        st.subheader("Health Information")
        injuries = st.text_area("Any injuries or restrictions?")
        medical_conditions = st.text_area("Any medical conditions to consider?")
        sleep_hours = st.slider("Average hours of sleep per night", 4, 12, 7)
        
        st.subheader("Lifestyle")
        diet_type = st.selectbox(
            "Diet Type",
            ["No Specific Diet", "Vegetarian", "Vegan", "Keto", "Paleo", 
             "Mediterranean", "Low Carb", "High Protein"]
        )
        
        stress_level = st.select_slider(
            "Stress Level",
            options=["Low", "Moderate", "High"]
        )
        
        consent = st.checkbox(
            "I agree that this is not medical advice and that any workout plans are suggestions only."
        )
        
        submitted = st.form_submit_button("Generate Plan")
        if not consent:
            st.info("Please provide consent to generate a plan.")

# Main content area
with results_placeholder:
    if submitted and consent:
        user_inputs = {
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "fitness_level": fitness_level,
            "fitness_goals": fitness_goals,
            "workout_distribution": st.session_state.manual_distribution,
            "minutes_per_session": minutes_per_session,
            "days_per_week": days_per_week,
            "preferred_workouts": preferred_workouts,
            "equipment": equipment,
            "injuries": injuries,
            "medical_conditions": medical_conditions,
            "sleep_hours": sleep_hours,
            "diet_type": diet_type,
            "stress_level": stress_level
        }
        
        prompt = build_prompt(user_inputs)
        
        with st.spinner("🤖 AI is crafting your personalized fitness plan..."):
            try:
                llm_response = call_llm_api(prompt)
                plan = parse_llm_response(llm_response)
                
                # Display the plan
                st.success("✨ Your personalized fitness plan is ready!")
                display_workout_plan(plan, days_per_week)
                
                # Add download button for the plan
                plan_text = "\n\n".join([
                    f"{session['header']}\n"
                    f"Focus: {session['focus']}\n"
                    f"Duration: {session['duration']}\n"
                    f"Intensity: {session['intensity']}\n\n"
                    f"Exercises:\n" + "\n".join([f"- {ex}" for ex in session['exercises']]) +
                    ("\n\nNotes:\n" + "\n".join([f"- {note}" for note in session['notes']]) if session['notes'] else "")
                    for session in plan
                ])
                
                st.download_button(
                    label="📥 Download Plan",
                    data=plan_text,
                    file_name=f"fitness_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error generating plan: {e}")
        
        if st.button("🔄 Regenerate Plan"):
            st.rerun()
    elif submitted and not consent:
        st.error("You must provide consent to generate a plan.") 