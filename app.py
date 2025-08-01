from flask import Flask, render_template, request, jsonify
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re
import math

app = Flask(__name__)

load_dotenv()

# BMI and BMR Calculation Functions
def calculate_bmi(weight_kg, height_ft):
    """Calculate BMI given weight in kg and height in feet"""
    # Convert height from feet to meters
    height_m = height_ft * 0.3048
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(weight_kg, height_ft, age, gender):
    """Calculate BMR using Mifflin-St Jeor Equation"""
    # Convert height from feet to cm
    height_cm = height_ft * 30.48
    
    if gender == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return round(bmr)

def calculate_tdee(bmr, activity_level="moderate"):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "sedentary": 1.2,      # Little or no exercise
        "light": 1.375,        # Light exercise 1-3 days/week
        "moderate": 1.55,      # Moderate exercise 3-5 days/week
        "active": 1.725,       # Hard exercise 6-7 days/week
        "very_active": 1.9     # Very hard exercise, physical job
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.55)
    return round(bmr * multiplier)

# --- LangChain Setup (Original Structure) ---
llm_resto = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile", # As per your request
    temperature=0.0
)

prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype', 'bmi', 'bmi_category', 'bmr', 'tdee'],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
        "Restaurants:\n"
        "- name1\n- name2\n- name3\n- name4\n- name5\n- name6\n\n"
        "Breakfast:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n- item6\n\n"
        "Dinner:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Workouts:\n"
        "- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n- workout6\n\n"
        "Criteria:\n"
        "Age: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
        "BMI: {bmi} ({bmi_category}), BMR: {bmr} calories, TDEE: {tdee} calories, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}.\n"
        "Please consider the BMI category and caloric needs when making recommendations."
    )
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods = ['POST'])
def recommend():
    if request.method == "POST":
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        veg_or_nonveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']
        activity_level = request.form['activity_level']

        # Calculate BMI and BMR
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)

        chain = LLMChain(llm = llm_resto, prompt = prompt_template_resto)

        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_nonveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype,
            'bmi': bmi,
            'bmi_category': bmi_category,
            'bmr': bmr,
            'tdee': tdee
        }

        results = chain.run(input_data)

        restaurant_names = re.findall(r'Restaurants:\s*(.*?)\n\n', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)

        def clean_list(block):
            return [line.strip("- ")for line in block.strip().split("\n") if line.strip()]

        restaurant_names = clean_list(restaurant_names[0]) if restaurant_names else []
        breakfast_names = clean_list(breakfast_names[0]) if breakfast_names else []
        dinner_names = clean_list(dinner_names[0]) if dinner_names else []
        workout_names = clean_list(workout_names[0]) if workout_names else []

        return render_template('result.html', 
                             restaurant_names=restaurant_names, 
                             breakfast_names=breakfast_names, 
                             dinner_names=dinner_names, 
                             workout_names=workout_names,
                             bmi=bmi,
                             bmi_category=bmi_category,
                             bmr=bmr,
                             tdee=tdee,
                             weight=weight,
                             height=height,
                             age=age,
                             gender=gender)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)