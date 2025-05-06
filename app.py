
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatGroq(model="llama3-8b-8192")

# Function to calculate daily calorie requirements
def calculate_calorie_requirements(age, gender, weight, height, fitness_goal):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    if fitness_goal == "Weight Loss":
        return bmr * 1.2
    elif fitness_goal == "Weight Gain":
        return bmr * 1.5
    else:
        return bmr * 1.375

# Function to generate the plan
def generate_plan_with_prompt(metrics, prompt_template):
    prompt = prompt_template.format(**metrics)
    response = model.invoke(prompt)
    return response

# Function to format the response neatly
def format_plan(response):
    try:
        content = response.content
        sections = content.split("\n\n")
        formatted = ""
        for section in sections:
            formatted += f"**{section.strip()}**\n\n"
        return formatted
    except Exception as e:
        return f"Error formatting plan: {e}"

# Prompt template
prompt_template = """
You are a health expert. Generate a personalized weekly diet and exercise plan for {name}, a {age}-year-old {gender} with a BMI of {bmi} ({health_status}).

Fitness Goal: {fitness_goal}.
Daily Calorie Requirement: {daily_calories} kcal.
Dietary Preference: {dietary_preference}.
Food Allergies: {food_allergies}.
Local Cuisine: {local_cuisine}.
Month: {month}.

Plan should include:
1. A daily diet plan with meal timings, calorie details, and meal alternatives.
2. Exercise routines based on goals, incorporating cardio, strength, and flexibility.
3. Dynamic plan adjustments based on month and local cuisine preferences.
4. Wearable integration for tracking steps, heart rate, and calorie burn.
5. Progress monitoring for daily calorie burn and weight tracking.
6. **Food Delivery Integration**:
   - Meal suggestions based on diet plans.
   - Integration with food delivery platforms (Uber Eats, DoorDash).
   - Searching menu items that fit calorie and dietary preferences.
   - Multi-restaurant meal aggregation for complete diet fulfillment.
   - Location-based meal recommendations.
   - Customizable meal delivery schedules.

Provide a detailed plan for each weekday: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.

Return output as:
Day: {{weekday}}
  - Breakfast: Time, Description, Calories
  - Lunch: Time, Description, Calories
  - Snacks: Time, Description, Calories
  - Dinner: Time, Description, Calories
  - Exercise: Description, Duration
  - Wearable Tracking: Steps, Heart Rate, Calories Burned
  - Progress Monitoring: Daily calorie intake vs. burn.
  - Food Delivery: Suggested meal items and delivery options.
"""

# Streamlit app
st.title("AI-Based Personalized Weekly Diet and Exercise Planner")

# Input fields
st.header("Enter Your Details")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, value=25)
weight = st.number_input("Weight (kg)", min_value=1, value=70)
height = st.number_input("Height (cm)", min_value=1, value=170)
gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
fitness_goal = st.selectbox("Fitness Goal", options=["Weight Loss", "Weight Gain", "Maintenance"])
dietary_preference = st.selectbox("Dietary Preference", options=["Vegetarian", "Vegan", "Keto", "Halal", "None"])
food_allergies = st.text_input("Food Allergies (if any)")
local_cuisine = st.text_input("Preferred Local Cuisine (e.g., Indian, Italian, Chinese)")
month = st.selectbox("Select Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

bmi = round(weight / (height / 100) ** 2, 2)
health_status = "Underweight" if bmi < 18.5 else "Normal weight" if bmi <= 24.9 else "Overweight"
daily_calories = calculate_calorie_requirements(age, gender, weight, height, fitness_goal)

st.write(f"Your BMI is {bmi}, which indicates {health_status}.")
st.write(f"Your daily calorie requirement is approximately {int(daily_calories)} kcal.")

# User metrics
metrics = {
    "name": name,
    "age": age,
    "gender": gender,
    "bmi": bmi,
    "health_status": health_status,
    "fitness_goal": fitness_goal,
    "dietary_preference": dietary_preference,
    "food_allergies": food_allergies,
    "daily_calories": int(daily_calories),
    "local_cuisine": local_cuisine,
    "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "month": month,
}

# Generate and display plan
if st.button("Generate Plan"):
    with st.spinner("Generating your plan..."):
        try:
            plan = generate_plan_with_prompt(metrics, prompt_template)
            formatted_plan = format_plan(plan)
            st.header(f"Generated Diet and Exercise Plan for {month}")
            st.markdown(formatted_plan)
        except Exception as e:
            st.error(f"Error generating the plan: {e}")

