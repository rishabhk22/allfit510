import streamlit as st
from openai import OpenAI
import calendar
import re

# Try to get API key from Streamlit secrets first, then fall back to local secrets
try:
    client = OpenAI(api_key=st.secrets["openai"]["OPENAI_API_KEY"])
except:
    try:
        from my_secrets import OPENAI_API_KEY
        client = OpenAI(api_key=OPENAI_API_KEY)
    except:
        raise Exception("OpenAI API key not found in either Streamlit secrets or my_secrets.py")

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
    
    example = '''\n\n---\n\nExample of the desired workout plan format:\n\nDay 1: Monday - Strength Training\nFocus: Upper Body Strength\nDuration: 45 minutes\nIntensity: Moderate to High\n\nWarm-up (5-10 minutes):\n- Arm circles: 30 seconds forward, 30 seconds backward\n- Shoulder rolls: 10 reps each direction\n- Light cardio: 3-5 minutes\n\nMain Exercises:\nChest: Dumbbell Bench Press — 3 sets of 8-10 reps\n- Keep feet flat on the floor, maintain natural arch in lower back\n- Lower weights to chest level, push up with controlled movement\n\nBack: Bent-Over Rows — 3 sets of 10-12 reps\n- Maintain flat back, pull elbows back and up\n- Squeeze shoulder blades together at top of movement\n\nShoulders: Overhead Press — 3 sets of 8-10 reps\n- Start with weights at shoulder height\n- Press up until arms are fully extended\n\nBiceps: Hammer Curls — 3 sets of 12-15 reps\n- Keep elbows close to body\n- Maintain controlled movement throughout\n\nTriceps: Tricep Dips — 3 sets of 10-12 reps\n- Keep elbows close to body\n- Lower until upper arms are parallel to floor\n\nCool-down (5-10 minutes):\n- Light stretching for all worked muscle groups\n- Deep breathing exercises\n\nNotes:\n- Rest 60-90 seconds between sets\n- Focus on proper form over weight\n- Stay hydrated throughout the workout\n- Consider using a spotter for heavy lifts\n\n---\n\n'''
    
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
        f"- Days per Week: {days} active workout days\n"
        f"- Preferred Styles: {styles}\n"
        f"- Available Equipment: {equipment}\n\n"
        f"Health Considerations:\n"
        f"- Injuries/Restrictions: {injuries}\n"
        f"- Medical Conditions: {medical_conditions}\n"
        f"- Average Sleep: {sleep_hours} hours\n\n"
        f"Lifestyle:\n"
        f"- Diet Type: {diet_type}\n"
        f"- Stress Level: {stress_level}\n\n"
        f"IMPORTANT INSTRUCTIONS FOR WORKOUT PLAN:\n"
        f"1. Create exactly {days} active workout days and {7 - int(days)} rest days\n"
        f"2. Space out the rest days strategically throughout the week\n"
        f"3. Do NOT make every day a rest day\n"
        f"4. For each workout day, include:\n"
        f"   - A proper warm-up routine (5-10 minutes)\n"
        f"   - 4-6 specific exercises with sets and reps\n"
        f"   - A cool-down routine (5-10 minutes)\n"
        f"5. For rest days, provide:\n"
        f"   - Light stretching recommendations\n"
        f"   - Optional active recovery activities\n"
        f"   - Recovery tips\n\n"
        f"WORKOUT FOCUS TYPES:\n"
        f"1. Strength Training: Focus on building muscle and increasing strength\n"
        f"2. Cardio: Focus on cardiovascular endurance and calorie burn\n"
        f"3. Mobility: Focus on flexibility, joint health, and range of motion\n"
        f"4. HIIT: High-intensity interval training for maximum calorie burn\n"
        f"5. Recovery: Light activity and stretching for active recovery\n"
        f"6. Full Body: Comprehensive workout targeting multiple muscle groups\n"
        f"7. Core: Focus on abdominal and core strength\n\n"
        f"Please create a detailed weekly workout plan with the following structure for each day:\n"
        f"Day X: [Day Name, e.g., Day 1: Monday]\n"
        f"Type: [Workout Day or Rest Day]\n"
        f"Focus: [Specify the workout focus type from the list above]\n"
        f"If Workout Day:\n"
        f"Warm-up: [List warm-up exercises specific to the focus type]\n"
        f"[Muscle Group]: [Exercise Name] — [Sets] sets of [Reps] reps [per leg/arm if applicable]\n"
        f"[Muscle Group]: [Exercise Name] — [Sets] sets of [Reps] reps [per leg/arm if applicable]\n"
        f"... (Include 4-6 exercises)\n"
        f"Cool-down: [List cool-down exercises specific to the focus type]\n"
        f"If Rest Day:\n"
        f"Recovery Activities: [List light activities/stretches]\n"
        f"Recovery Tips: [Provide recovery advice]\n"
        f"Focus: [Specify if it's a complete rest day or active recovery day]\n\n"
        f"Make sure to:\n"
        f"- Strictly follow the workout distribution percentages provided\n"
        f"- Include proper warm-up and cool-down exercises for workout days\n"
        f"- Consider the user's fitness level and goals\n"
        f"- Provide modifications for exercises if needed\n"
        f"- Space out rest days appropriately for optimal recovery\n"
        f"- Add notes about proper form and technique\n"
        f"- Consider the user's available equipment\n"
        f"- Account for any injuries or medical conditions\n"
        f"- Suggest appropriate intensity levels\n"
        f"- Include progression recommendations\n"
        f"- Ensure the weekly plan reflects the exact workout distribution percentages\n"
        f"- Make the workout descriptions clear, detailed, and easy to follow\n"
        f"- Label each day clearly as either a Workout Day or Rest Day\n"
        f"- Specify the focus type for each day\n"
        f"- Provide exactly {days} workout days and {7 - int(days)} rest days\n"
        f"- Alternate between different focus types throughout the week\n"
        f"- Include at least one complete rest day per week\n"
        f"{example}"
    )
    return prompt

def call_llm_api(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3500,
        temperature=0.7,
    )
    return response.choices[0].message.content