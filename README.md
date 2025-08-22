# OptiFit - AI-Powered Diet & Fitness Recommendations

OptiFit is a comprehensive health and fitness application that provides personalized diet and workout recommendations using AI. It includes BMI/BMR calculations and advanced food image analysis capabilities.

## ‍💻 Author

**Supriyo Dawn**

## 🚀 Features

### Core Features
- **Personalized Diet Recommendations**: AI-powered meal suggestions based on your profile
- **Workout Recommendations**: Customized exercise plans

- **BMI & BMR Calculations**: Scientific health metrics using Mifflin-St Jeor Equation
- **Activity Level Integration**: Accurate TDEE calculations based on activity level
- **AI Coach Bot**: Interactive chat interface for personalized fitness and nutrition advice

### Advanced Food Analysis
- **Image Recognition**: Upload food images for instant analysis
- **Calorie Estimation**: Automatic calorie counting for identified foods
- **Health Assessment**: 5-star health rating system
- **Nutritional Insights**: Benefits and concerns for each food item
- **Drag & Drop Interface**: Modern, intuitive image upload experience

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>

   # OptiFit

   A fitness and nutrition recommendation system using AI and Indian food datasets.

   ## Structure
   - `src/` - Main application code (Flask app, models, logic)
   - `data/` - Datasets and text resources (CSV, TXT)
   - `static/` - CSS, JS, and static assets
   - `templates/` - HTML templates
   - `tests/` - Test files

   ## Setup
   See `requirements.txt` for dependencies.

   ## Usage
   Run the app from `src/app.py`.
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 📋 Usage

### Getting Started
1. **Fill out your health profile** with age, gender, weight, height, and preferences
2. **Select your activity level** for accurate calorie calculations
3. **Submit the form** to get personalized recommendations

### Food Image Analysis
1. **Upload a food image** using drag & drop or file browser
2. **Click "Analyze Food"** to get instant nutritional analysis
3. **Review results** including calories, health rating, and nutritional insights

### AI Coach Bot
1. **Click "Chat with AI Coach"** on the homepage to access the chat interface
2. **Use quick prompt buttons** for common questions about workouts, nutrition, and recovery
3. **Type custom questions** in the chat input for personalized advice
4. **Use voice input** with microphone button (supports Hindi, English, and Indian English)
5. **Get multilingual responses** in the same language as your question
6. **Get concise, formatted responses** with bullet points and proper alignment
7. **Real-time responses** with conversation memory for contextual follow-ups

### Multilingual Support
- **Hindi Voice Input**: Click microphone button and speak in Hindi
- **English Voice Input**: Switch to English for voice commands
- **Indian English**: Optimized for Indian English pronunciation
- **Automatic Language Detection**: AI responds in the same language as your question
- **Hindi Quick Prompts**: Pre-built Hindi questions for common fitness queries

### Understanding Results
- **BMI Categories**: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (≥30)
- **BMR**: Basal Metabolic Rate - calories burned at rest
- **TDEE**: Total Daily Energy Expenditure - total daily calorie needs
- **Health Ratings**: 1-5 star system (Poor to Excellent)

## 🔧 Technical Details

### AI Models Used
- **Food Recognition**: Hugging Face Food101 model for image classification
- **Diet Recommendations**: Groq LLM with LangChain integration
- **AI Coach Bot**: Google Gemini Pro with LangChain conversation memory
- **Multilingual Support**: Native Hindi and English language processing
- **Nutrition Database**: Comprehensive food nutrition database

### Health Calculations
- **BMI**: Weight (kg) / Height (m)²
- **BMR**: Mifflin-St Jeor Equation
- **TDEE**: BMR × Activity Multiplier

### Activity Multipliers
- Sedentary: 1.2 (Little or no exercise)
- Light: 1.375 (Light exercise 1-3 days/week)
- Moderate: 1.55 (Moderate exercise 3-5 days/week)
- Active: 1.725 (Hard exercise 6-7 days/week)
- Very Active: 1.9 (Very hard exercise, physical job)

## 🎨 UI Features

### Modern Design
- **Gradient Backgrounds**: Beautiful purple gradient theme
- **Glassmorphism Effects**: Modern glass-like card designs
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Works on all device sizes
- **Icon Integration**: Font Awesome icons throughout

### Interactive Elements
- **Drag & Drop**: Intuitive image upload
- **Real-time Analysis**: Instant food recognition
- **Visual Feedback**: Loading states and progress indicators
- **Health Stars**: Visual health rating system

## 📊 Supported Food Categories

The application can recognize and analyze various food types including:
- Fruits (apples, bananas, etc.)
- Proteins (chicken, fish, eggs, etc.)
- Grains (rice, bread, pasta, etc.)
- Dairy (milk, cheese, etc.)
- Beverages (coffee, tea, water, etc.)
- Desserts (cake, ice cream, etc.)
- And many more...

## 🔒 Privacy & Security

- **Local Processing**: Food images are processed locally
- **No Data Storage**: User data is not stored permanently
- **Secure API**: Environment variables for API keys
- **HTTPS Ready**: Production-ready security features

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production server (AWS, Heroku, etc.)
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run with production WSGI server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the documentation
- Review the code comments
- Create an issue in the repository

---

**OptiFit** - Your health, optimized with AI! 🏃‍♂️💪