import google.generativeai as genai

API_KEY = ''
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

base = input("Digite um livro e/ou gênero literário que você gosteria de ler: ")
response = model.generate_content(f'Recomende 3 livro com base em {base}')
print(response.text)
