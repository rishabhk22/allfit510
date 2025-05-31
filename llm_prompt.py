import streamlit as st
from openai import OpenAI

# Use client-style API introduced in openai>=1.0.0
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def build_prompt(user_inputs):
    age = user_inputs.get('age', 'N/A')
    fitness_level = user_inputs.get('fitness_level', 'N/A')
    goals = ', '.join(user_inputs.get('fitness_goals', [])) or 'N/A'
    minutes = user_inputs.get('minutes_per_session', 'N/A')
    days = user_inputs.get('days_per_week', 'N/A')
    styles = ', '.join(user_inputs.get('preferred_workouts', [])) or 'N/A'
    equipment = user_inputs.get('equipment', 'N/A')
    injuries = user_inputs.get('injuries', '').strip() or 'no injuries'

    prompt = (
        f"You are a fitness assistant. Create a detailed weekly workout plan for a [{age}]-year-old "
        f"[{fitness_level}] user who wants to improve [{goals}] with [{minutes}]-minute sessions, "
        f"[{days}] days per week. Preferred workout styles are [{styles}]. Equipment: [{equipment}]. "
        f"Note: user has [{injuries}]. For each day, provide:\n"
        f"- The focus area\n"
        f"- The session duration\n"
        f"- A warm-up suggestion (1–2 exercises)\n"
        f"- 3–5 specific exercises, each with a one-line description and a tip\n"
        f"- A cool-down suggestion (1–2 exercises)\n"
        f"Format the plan clearly by day."
    )
    return prompt

def call_llm_api(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7,
    )
    return response.choices[0].message.content
