import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load dataset
DATA_PATH = r"c:\Projects\Minor Project\OptiFit\Cleaned_Indian_Food_Dataset.csv"

INDIAN_CUISINES = [
    'Indian', 'North Indian Recipes', 'South Indian Recipes', 'Kerala Recipes', 'Karnataka', 'Bengali Recipes',
    'Maharashtrian Recipes', 'Lucknowi', 'Rajasthani', 'Tamil Nadu', 'Hyderabadi', 'Chettinad', 'Goan Recipes',
    'Punjabi', 'Andhra', 'Gujarati Recipes', 'Side Dish', 'Mughlai', 'Bihari', 'Sindhi', 'Uttar Pradesh', 'Assamese',
    'Oriya', 'Kashmiri', 'Manipuri', 'Chhattisgarh', 'Haryanvi', 'Jharkhand', 'Sikkimese', 'Tripuri', 'Meghalayan',
    'Nagaland', 'Arunachal', 'Mizo', 'Dogri', 'Garhwali', 'Kumaoni', 'Tulu', 'Coorg', 'Malvani', 'Awadhi', 'Bohri',
    'Banjara', 'Bastar', 'Bodo', 'Santhal', 'Konkani', 'Bengali', 'Marathi', 'Telugu', 'Kannada', 'Tamil', 'Malayali',
    'Himachali', 'Rajasthani', 'Goan', 'Uttarakhand', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Lakshadweep', 'Pondicherry'
]
# Robust loading and column detection
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()

def get_col(possibles):
    for p in possibles:
        if p in df.columns:
            return p
    return None

ING_COL = get_col(['TranslatedIngredients', 'Cleaned-Ingredients', 'ingredients', 'Ingredients', 'ingredient'])
NAME_COL = get_col(['TranslatedRecipeName', 'recipe_name', 'RecipeName', 'name'])
CUISINE_COL = get_col(['Cuisine', 'cuisine'])
DIET_COL = get_col(['diet_type', 'DietType', 'diet'])  # Will be None if not present

if ING_COL is None or df.empty:
    print(f"No ingredients column found or dataset is empty. Available columns: {list(df.columns)}")
    ING_COL = NAME_COL = CUISINE_COL = DIET_COL = None
    vectorizer = None
    nn_model = None
else:
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        X = vectorizer.fit_transform(df[ING_COL].fillna(''))
        nn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
        nn_model.fit(X)
    except Exception as e:
        print(f"Error fitting model: {e}")
        nn_model = None

def recommend_recipes(user_ingredients, top_n=5):
    """
    Recommend recipes based on user input ingredients (string).
    Returns a list of dicts with recipe info or error message.
    """
    if vectorizer is None or nn_model is None or ING_COL is None:
        return [{'error': 'Recipe model is not available. Please check the dataset and column names.'}]
    try:
        user_vec = vectorizer.transform([user_ingredients])
        distances, indices = nn_model.kneighbors(user_vec, n_neighbors=top_n)
        results = []
        for idx in indices[0]:
            rec = df.iloc[idx]
            # Return all columns for each recipe as a dict
            results.append({col: rec.get(col, '') for col in df.columns})
        if not results:
            return [{'error': 'No recipes found for the given ingredients.'}]
        return results
    except Exception as e:
        return [{'error': f'Error during recipe recommendation: {e}'}]
