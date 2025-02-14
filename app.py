from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import os

load_dotenv()

# Set up Flask app
app = Flask(__name__)

key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API key
genai.configure(api_key=key)  # Replace with your actual API key

@app.route('/', methods=['GET', 'POST'])
def index():
    suggestions = None
    if request.method == 'POST':
        if 'required_image' not in request.files or 'derived_image' not in request.files:
            return render_template('index.html', error="Please upload both images.")
        
        required_image_file = request.files['required_image']
        derived_image_file = request.files['derived_image']
        
        if required_image_file.filename == '' or derived_image_file.filename == '':
            return render_template('index.html', error="Please select images before submitting.")
        
        required_image = Image.open(required_image_file)
        derived_image = Image.open(derived_image_file)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            "You are a professional chef evaluating the quality of a dish. Compare the derived image to the required image and provide feedback as a chef. Focus on aspects such as texture, ingredient balance, cooking technique, plating, and presentation. Identify mistakes in the derived dish and suggest improvements to achieve the high culinary standard of the required dish. Offer actionable advice on cooking methods, seasoning, and visual appeal to enhance the dish’s overall quality. Don't explain about image just tell the suggestion in food point of view. Don't provide unwanted content.",
            required_image,
            derived_image
        ])
        
        suggestions = response.text
    
    return render_template('index.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)