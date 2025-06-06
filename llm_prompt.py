import streamlit as st
from openai import OpenAI
import calendar
import re

# Use client-style API introduced in openai>=1.0.0
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def build_prompt(user_inputs):
    # Basic Information
    age = user_inputs.get('age', 'N/A')
    gender = user_inputs.get('gender', 'N/A')
    weight = user_inputs.get('weight', 'N/A')
    height = user_inputs.get('height', 'N/A')
    
    # Fitness Profile
    fitness_level = user_inputs.get('fitness_level', 'N/A')
    goals = ', '.join(user_inputs.get('fitness_goals', [])) or 'N/A'
    
    # Workout Distribution
    workout_distribution = user_inputs.get('workout_distribution', {})
    distribution_text = "\n".join([
        f"- {workout_type}: {percentage}%"
        for workout_type, percentage in workout_distribution.items()
    ])
    
    # Workout Preferences
    minutes = user_inputs.get('minutes_per_session', 'N/A')
    days = user_inputs.get('days_per_week', 'N/A')
    styles = ', '.join(user_inputs.get('preferred_workouts', [])) or 'N/A'
    equipment = user_inputs.get('equipment', 'N/A')
    
    # Health Information
    injuries = user_inputs.get('injuries', '').strip() or 'no injuries'
    medical_conditions = user_inputs.get('medical_conditions', '').strip() or 'no medical conditions'
    sleep_hours = user_inputs.get('sleep_hours', 'N/A')
    
    # Lifestyle
    diet_type = user_inputs.get('diet_type', 'N/A')
    stress_level = user_inputs.get('stress_level', 'N/A')
    
    prompt = (
        f"You are an expert fitness trainer and nutritionist. Create a detailed weekly workout plan for a "
        f"[{age}]-year-old [{gender}] user with the following profile:\n\n"
        f"Physical Stats:\n"
        f"- Height: {height} cm\n"
        f"- Weight: {weight} kg\n"
        f"- Fitness Level: {fitness_level}\n"
        f"- Goals: {goals}\n\n"
        f"Workout Distribution (Must strictly follow these percentages):\n"
        f"{distribution_text}\n\n"
        f"Workout Preferences:\n"
        f"- Session Duration: {minutes} minutes\n"
        f"- Days per Week: {days}\n"
        f"- Preferred Styles: {styles}\n"
        f"- Available Equipment: {equipment}\n\n"
        f"Health Considerations:\n"
        f"- Injuries/Restrictions: {injuries}\n"
        f"- Medical Conditions: {medical_conditions}\n"
        f"- Average Sleep: {sleep_hours} hours\n\n"
        f"Lifestyle:\n"
        f"- Diet Type: {diet_type}\n"
        f"- Stress Level: {stress_level}\n\n"
        f"Please create a detailed weekly workout plan with the following structure for each day:\n"
        f"Day X: [Day Name, e.g., Day 1: Monday]\n"
        f"[Muscle Group]: [Exercise Name] — [Sets] sets of [Reps] reps [per leg/arm if applicable]\n"
        f"[Muscle Group]: [Exercise Name] — [Sets] sets of [Reps] reps [per leg/arm if applicable]\n"
        f"... (Include 4-6 exercises per day)\n"
        f"Rest Day: [Short description or suggestion for rest]\n\n"
        f"Make sure to:\n"
        f"- Strictly follow the workout distribution percentages provided\n"
        f"- Include proper warm-up and cool-down exercises\n"
        f"- Consider the user's fitness level and goals\n"
        f"- Provide modifications for exercises if needed\n"
        f"- Include rest days appropriately and distribute them for optimal recovery (not all at once, but spaced for best recovery), following the user's requested days per week.\n"
        f"- Add notes about proper form and technique\n"
        f"- Consider the user's available equipment\n"
        f"- Account for any injuries or medical conditions\n"
        f"- Suggest appropriate intensity levels\n"
        f"- Include progression recommendations\n"
        f"- Ensure the weekly plan reflects the exact workout distribution percentages\n"
        f"- Make the workout descriptions clear, detailed, and easy to follow, like the format provided.\n"
        f"- Explicitly label rest days with \"Rest Day\".\n"
        f"- Provide exactly {days} workout days and {7 - days} rest days.\n"
    )
    return prompt

def call_llm_api(prompt, model="gpt-3.5-turbo"):
    openai.api_key = OPENAI_API_KEY
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3500,
        temperature=0.7,
    )
    return response.choices[0].message.content