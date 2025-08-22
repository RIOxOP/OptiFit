import random

# Optional heavy imports guarded so the module can be imported even if packages are not installed
try:
    import pandas as pd
except Exception:
    pd = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
except Exception:
    TfidfVectorizer = None
    linear_kernel = None

# Load dataset once at import if pandas is available
CSV_PATH = r"c:\Projects\Minor Project\OptiFit\Cleaned_Indian_Food_Dataset.csv"
if pd is not None:
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception:
        df = pd.DataFrame(columns=["recipe_name", "ingredients", "cuisine", "diet_type"])
else:
    # pandas not available; fallback to empty list
    df = []

ING_COL = 'TranslatedIngredients' if 'TranslatedIngredients' in df.columns else (
    'Cleaned-Ingredients' if 'Cleaned-Ingredients' in df.columns else 'ingredients')
NAME_COL = 'TranslatedRecipeName' if 'TranslatedRecipeName' in df.columns else (
    'recipe_name' if 'recipe_name' in df.columns else 'name')
CUISINE_COL = 'Cuisine' if 'Cuisine' in df.columns else 'cuisine'
DIET_COL = 'diet_type' if 'diet_type' in df.columns else None

# Precompute TF-IDF matrix on ingredients if sklearn/pandas are available
if pd is not None and TfidfVectorizer is not None and ING_COL in df.columns and not df[ING_COL].isna().all():
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df[ING_COL].fillna(''))
else:
    tfidf = None
    tfidf_matrix = None


def search_recipes_by_ingredients(query, top_n=6):
    """Return top_n recipes whose ingredients best match the query string."""
    if tfidf is None or tfidf_matrix is None:
        # Fallback: if pandas available use sample, otherwise return first N items from list
        if pd is not None and hasattr(df, 'sample'):
            samples = df.sample(n=min(top_n, len(df))) if len(df) > 0 else []
            return samples.to_dict('records') if len(samples) > 0 else []
        else:
            # df is a list
            return df[:top_n]

    q_vec = tfidf.transform([query])
    cosine_similarities = linear_kernel(q_vec, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[-top_n:][::-1]
    results = df.iloc[related_docs_indices]
    return results.to_dict('records')


def filter_recipes(preferences: dict, top_n=6):
    """preferences keys: veg_or_nonveg, diet_type, allergens (comma separated), cuisine"""
    # Build a query string for ingredients search
    parts = []
    if preferences.get('allergics'):
        # Exclude allergens by filtering later
        allergens = [a.strip().lower() for a in preferences.get('allergics', '').split(',') if a.strip()]
    else:
        allergens = []

    if preferences.get('foodtype'):
        parts.append(preferences.get('foodtype'))
    if preferences.get('region'):
        parts.append(preferences.get('region'))
    if preferences.get('veg_or_nonveg'):
        parts.append(preferences.get('veg_or_nonveg'))

    query = ' '.join(parts) if parts else ''
    candidates = search_recipes_by_ingredients(query, top_n=50)
    filtered = []
    for r in candidates:
        name = r.get(NAME_COL, '')
        ingredients = r.get(ING_COL, '')
        cuisine = r.get(CUISINE_COL, '')
        diet = r.get(DIET_COL, '') if DIET_COL else ''

        pref = preferences.get('veg_or_nonveg', '').lower()
        if pref:
            if pref == 'vegetarian' and 'non' in diet.lower():
                continue
            if pref in ['non-vegetarian', 'nonveg', 'non-vegetarian'] and 'veg' in diet.lower() and 'non' not in diet.lower():
                pass

        region = preferences.get('region', '').lower()
        if region and region not in cuisine.lower() and region not in name.lower():
            pass

        skip = False
        for a in allergens:
            if a and a in ingredients.lower():
                skip = True
                break
        if skip:
            continue

        filtered.append({
            'name': name,
            'ingredients': ingredients,
            'cuisine': cuisine,
            'diet_type': diet,
            'all_attributes': r  # include all attributes for template rendering
        })
        if len(filtered) >= top_n:
            break

    # If no filtered results, fallback to random
    if not filtered:
        if pd is not None and hasattr(df, 'sample'):
            sampled = df.sample(n=min(top_n, len(df))) if len(df) > 0 else []
            return sampled.to_dict('records') if len(sampled) > 0 else []
        else:
            return df[:top_n]

    return filtered


def generate_recipe_text(recipe_record, target_calories=None):
    """Create a short recipe description from a record."""
    name = recipe_record.get('name') or recipe_record.get('recipe_name') or 'Recipe'
    ingredients = recipe_record.get('ingredients', '')
    cuisine = recipe_record.get('cuisine', 'Various')
    diet = recipe_record.get('diet_type', 'Mixed')

    # Simple ingredient list formatting
    ing_list = [i.strip() for i in ingredients.split(',') if i.strip()]
    ing_preview = ', '.join(ing_list[:8]) + ('' if len(ing_list) <= 8 else ', ...')

    lines = []
    lines.append(f"{name} ({cuisine})")
    lines.append(f"Diet: {diet}")
    lines.append("Ingredients: " + ing_preview)
    if target_calories:
        lines.append(f"Approx. target calories: {target_calories} kcal")

    # Quick steps placeholder
    lines.append("Quick steps: Combine ingredients and cook as per standard recipes. Adjust spices to taste.")

    return '\n'.join(lines)
