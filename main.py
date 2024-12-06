import google.generativeai as ai

API_KEY = ''

ai.configure(api_key = API_KEY)
model = ai.GenerativeModel('gemini-pro')
word = model.generate_content('Gere uma palavra aleatória em português com 5 letras')
print(word.text)
