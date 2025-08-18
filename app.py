from flask import Flask, render_template, request, jsonify
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re
import math
import json

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

# --- AI Coach Bot Setup ---
llm_coach = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7  # Slightly higher temperature for more creative responses
)

# AI Coach Prompt Template
coach_prompt_template = PromptTemplate(
    input_variables=['human_input'],
    template=(
        "You are an expert AI fitness and nutrition coach. Provide SHORT, CONCISE, and WELL-FORMATTED responses.\n\n"
        "RESPONSE FORMAT:\n"
        "• Use bullet points (•) for lists\n"
        "• Keep each point brief (1-2 lines max)\n"
        "• Use clear headings when needed\n"
        "• Maximum 5-6 points per response\n"
        "• Be encouraging and practical\n\n"
        "TOPICS:\n"
        "• Workout routines and exercises\n"
        "• Nutrition and meal planning\n"
        "• Recovery and supplement advice\n"
        "• Fitness tips and motivation\n"
        "• Weight loss and muscle building\n\n"
        "MULTILINGUAL SUPPORT:\n"
        "• Respond in the same language as the user's question\n"
        "• Support both Hindi and English\n"
        "• Maintain consistent formatting in all languages\n\n"
        "IMPORTANT: Keep responses under 150 words. Use proper formatting with bullet points.\n"
        "For medical advice, remind users to consult healthcare professionals.\n\n"
        "Human: {human_input}\n"
        "AI Coach:"
    )
)

prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype', 'bmi', 'bmi_category', 'bmr', 'tdee'],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
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

        breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)

        def clean_list(block):
            return [line.strip("- ")for line in block.strip().split("\n") if line.strip()]

        breakfast_names = clean_list(breakfast_names[0]) if breakfast_names else []
        dinner_names = clean_list(dinner_names[0]) if dinner_names else []
        workout_names = clean_list(workout_names[0]) if workout_names else []

        return render_template('result.html', 
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

@app.route('/chat')
def chat():
    """Render the chat page"""
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat_api():
    """Handle chat messages via API"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Create LLM chain with the coach prompt
        coach_chain = LLMChain(
            llm=llm_coach,
            prompt=coach_prompt_template,
            verbose=False
        )
        
        # Get response from the chain
        ai_response = coach_chain.run(human_input=user_message)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error in chat API: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again.',
            'status': 'error'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)