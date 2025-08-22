from app import app
import recipes

app.testing = True
client = app.test_client()

print('Testing GET /recipes')
r = client.get('/recipes')
print('Status:', r.status_code)
print('Length:', len(r.data))
print('Snippet:', r.data[:300].decode('utf-8', errors='replace'))

print('\nTesting POST /recipes/generate')
form = {
    'veg_or_nonveg': 'vegetarian',
    'region': 'Punjabi',
    'foodtype': 'high protein',
    'allergics': 'nuts',
    'target_calories': '500'
}
r2 = client.post('/recipes/generate', data=form)
print('Status:', r2.status_code)
print('Length:', len(r2.data))
print('Snippet:', r2.data[:500].decode('utf-8', errors='replace'))

print('\nDirect recipes.filter_recipes() test')
res = recipes.filter_recipes(form, top_n=3)
print('Result count:', len(res))
for i, rec in enumerate(res[:3], 1):
    print(i, rec.get('name')[:80], '...')
