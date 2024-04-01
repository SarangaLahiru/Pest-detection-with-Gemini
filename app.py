from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import google.generativeai as genai

app = Flask(__name__)

# Load the trained machine learning model
model = load_model('insect_model1.h5')

# Define class names
class_names = [
    'Africanized Honey Bees (Killer Bees)',
    'Aphids',
    'Armyworms',
    'Brown Marmorated Stink Bugs',
    'Cabbage Loopers',
    'Citrus Canker',
    'Colorado Potato Beetles',
    'Corn Borers',
    'Corn Earworms',
    'Fall Armyworms',
    'Fruit Flies',
    'Spider Mites',
    'Thrips',
    'Tomato Hornworms',
    'Western Corn Rootworms'
]

# Create a dictionary to map numeric index to class names
index_to_class = {i: class_name for i, class_name in enumerate(class_names)}

# Function to preprocess image data
def preprocess_image(img):
    # Preprocess the image as required by your model
    img = image.load_img(img, target_size=(224, 224))  # Resize the image to match input shape
    img = image.img_to_array(img)
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    if 'image' not in request.files:
        return render_template('prediction.html', error='No file part')

    img_file = request.files['image']
    
    if img_file.filename == '':
        return render_template('prediction.html', error='No selected file')

    img_path = os.path.join('static', 'uploads', img_file.filename)
    img_file.save(img_path)

    if not os.path.exists(img_path):
        return render_template('prediction.html', error='Failed to save the uploaded image.')

    processed_img = preprocess_image(img_path)
    prediction = model.predict(processed_img)
    
    predicted_index = np.argmax(prediction)
    predicted_class = index_to_class.get(predicted_index, "Unknown")

    genai.configure(api_key="AIzaSyA6Bkhpmh6MY2-whmHejhRUsnA286YsExI")
    generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
    
    safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
    model1 = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
    user_prompt = f"can you give more details about {predicted_class} in 100 words?"
    convo = model1.start_chat(history=[
  {
    "role": "user",
    "parts": ["car"]
  },
  {
    "role": "model",
    "parts": ["**Noun**\n\n1. A motor vehicle with four wheels, an engine that powers it, and seats for one to eight people.\n2. A railway carriage for passengers.\n3. A cable car or funicular railway.\n4. (informal) A stolen vehicle.\n\n**Verb**\n\n1. To transport or drive (someone or something) in a car.\n2. (slang) To steal (a car).\n\n**Examples**\n\n1. We drove to the beach in my new car.\n2. The car was parked illegally.\n3. The car was stolen from the driveway.\n4. The thief was arrested for car theft.\n\n**Synonyms**\n\n* Automobile\n* Vehicle\n* Motor car\n* Coach\n* Saloon\n* Sedan\n* Coupe\n* Hatchback\n* Estate car\n* Station wagon\n* SUV\n* Crossover"]
  },
])

        # Send the user query and receive the response
    convo.send_message(user_prompt)
    details=convo.last.text
    print(convo.last.text)

    

    return render_template('prediction_result.html', prediction=predicted_class,details=details)

@app.route('/solution', methods=['POST', 'GET'])
def solution():
    if request.method == 'POST':
        pest = request.form['pest']
        
        # Configure the API key for authentication
        genai.configure(api_key="AIzaSyA6Bkhpmh6MY2-whmHejhRUsnA286YsExI")

        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        # Start a conversation with Gemini using the user prompt
        user_prompt = f"I'm experiencing issues with {pest}. Can you help me with a solutions in 100 words?"
        convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["car"]
  },
  {
    "role": "model",
    "parts": ["**Noun**\n\n1. A motor vehicle with four wheels, an engine that powers it, and seats for one to eight people.\n2. A railway carriage for passengers.\n3. A cable car or funicular railway.\n4. (informal) A stolen vehicle.\n\n**Verb**\n\n1. To transport or drive (someone or something) in a car.\n2. (slang) To steal (a car).\n\n**Examples**\n\n1. We drove to the beach in my new car.\n2. The car was parked illegally.\n3. The car was stolen from the driveway.\n4. The thief was arrested for car theft.\n\n**Synonyms**\n\n* Automobile\n* Vehicle\n* Motor car\n* Coach\n* Saloon\n* Sedan\n* Coupe\n* Hatchback\n* Estate car\n* Station wagon\n* SUV\n* Crossover"]
  },
])

        # Send the user query and receive the response
        convo.send_message(user_prompt)
        gemini_response=convo.last.text
        print(convo.last.text)
        

        return render_template('solutions.html', pest=pest, gemini_response=gemini_response)

    # If it's not a POST request, just render the form
    return render_template('solutions.html')


if __name__ == '__main__':
    app.run(debug=True)
