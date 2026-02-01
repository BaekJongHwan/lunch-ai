import google.generativeai as genai
genai.configure(api_key="AIzaSyC4fiZRe4KB6mTbhrmwN5d4DKw2DiQZ8D8")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)