import openai
from my_secrets import OPENAI_API_KEY

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
    
    example = '''\n\n---\n\nExample of the desired workout plan format:\n\nDay 1: Legs, shoulders, and abs\nLegs: dumbbell squats — 3 sets of 6–8 reps\nShoulders: standing shoulder press — 3 sets of 6–8 reps\nLegs: dumbbell lunge — 2 sets of 8–10 reps per leg\nShoulders: dumbbell upright rows — 2 sets of 8–10 reps\nHamstrings: Romanian dumbbell deadlift — 2 sets of 6–8 reps\nShoulders: lateral raises — 3 sets of 8–10 reps\nCalves: seated calf raises — 4 sets of 10–12 reps\nAbs: crunches with legs elevated — 3 sets of 10–12 reps\n\nDay 2: Chest and back\nChest: dumbbell bench press or floor press — 3 sets of 6–8 reps\nBack: dumbbell bent-over rows — 3 sets of 6–8 reps\nChest: dumbbell fly — 3 sets of 8–10 reps\nBack: one-arm dumbbell rows — 3 sets of 6–8 reps\nChest: pushups — 3 sets of 10–12 reps\nBack/chest: dumbbell pullovers — 3 sets of 10–12 reps\n\nDay 3: Arms and abs\nBiceps: alternating biceps curls — 3 sets of 8–10 reps per arm\nTriceps: overhead triceps extensions — 3 sets of 8–10 reps\nBiceps: seated dumbbell curls — 2 sets of 10–12 reps per arm\nTriceps: bench dips — 2 sets of 10–12 reps\nBiceps: concentration curls — 3 sets of 10–12 reps\nTriceps: dumbbell kickbacks — 3 sets of 8–10 reps per arm\nAbs: planks — 3 sets of 30-second holds\n\n---\n\n'''
    
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
        f"1. Day X: [Day Name]\n"
        f"2. Focus: [Main focus area for the day]\n"
        f"3. Duration: [Total workout duration]\n"
        f"4. Intensity: [Workout intensity level]\n"
        f"5. Exercises: [List 4-6 exercises with sets, reps, rest periods, and a 1-2 sentence description for each exercise. The list should be elaborate and well described.]\n"
        f"6. Notes: [Any important notes about form, progression, or modifications]\n\n"
        f"Make sure to:\n"
        f"- Strictly follow the workout distribution percentages provided\n"
        f"- Include proper warm-up and cool-down exercises\n"
        f"- Consider the user's fitness level and goals\n"
        f"- Provide modifications for exercises if needed\n"
        f"- Include rest days appropriately and distribute them for optimal recovery (not all at once, but spaced for best recovery)\n"
        f"- Add notes about proper form and technique\n"
        f"- Consider the user's available equipment\n"
        f"- Account for any injuries or medical conditions\n"
        f"- Suggest appropriate intensity levels\n"
        f"- Include progression recommendations\n"
        f"- Ensure the weekly plan reflects the exact workout distribution percentages\n"
        f"- Make the workout descriptions clear, detailed, and easy to follow.\n"
        f"{example}"
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