import streamlit as st
import importlib
import re
from llm_prompt import build_prompt, call_llm_api

st.title("Personalized Fitness Plan Generator")

# Helper to parse LLM response into structured sessions
def parse_llm_response(response):
    # Simple parser: expects each day to start with 'Day X' and exercises as bullet points
    days = re.split(r'(?=Day \d+)', response)
    plan = []
    for day in days:
        if not day.strip():
            continue
        lines = day.strip().split('\n')
        header = lines[0]
        focus = ''
        exercises = []
        for line in lines[1:]:
            if line.lower().startswith('focus'):
                focus = line.split(':', 1)[-1].strip()
            elif line.strip().startswith('-'):
                exercises.append(line.strip().lstrip('-').strip())
        plan.append({
            'header': header,
            'focus': focus,
            'exercises': exercises
        })
    return plan

with st.form("fitness_form"):
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    fitness_goals = st.multiselect(
        "Fitness Goals",
        ["Strength", "Flexibility", "Mobility", "Endurance", "Weight Loss"]
    )
    days_per_week = st.slider("Days per week", 1, 7, 3)
    minutes_per_session = st.slider("Minutes per session", 10, 90, 30)
    preferred_workouts = st.multiselect(
        "Preferred Workout Types",
        ["Yoga", "Cardio", "Weight Training", "Calisthenics", "Stretching"]
    )
    equipment = st.radio(
        "Equipment Available",
        ["No Equipment", "Basic", "Full Gym"]
    )
    injuries = st.text_area("Any injuries or restrictions?")
    consent = st.checkbox(
        "I agree that this is not medical advice and that any workout plans are suggestions only."
    )
    submitted = st.form_submit_button("Generate Plan")
    if not consent:
        st.info("Please provide consent to generate a plan.")

if submitted and consent:
    user_inputs = {
        "age": age,
        "fitness_level": fitness_level,
        "fitness_goals": fitness_goals,
        "minutes_per_session": minutes_per_session,
        "days_per_week": days_per_week,
        "preferred_workouts": preferred_workouts,
        "equipment": equipment,
        "injuries": injuries,
    }
    prompt = build_prompt(user_inputs)
    with st.spinner("Generating your plan with AI..."):
        try:
            llm_response = call_llm_api(prompt)
            plan = parse_llm_response(llm_response)
            st.info("AI-Generated Weekly Plan:")
            for session in plan:
                st.subheader(session['header'] + (f": {session['focus']}" if session['focus'] else ""))
                if session['exercises']:
                    st.markdown('\n'.join([f"- {ex}" for ex in session['exercises']]))
            st.success("Your personalized fitness plan is ready!")
        except Exception as e:
            st.error(f"Error generating plan: {e}")
    if st.button("Regenerate Plan"):
        st.experimental_rerun()
elif submitted and not consent:
    st.error("You must provide consent to generate a plan.") 