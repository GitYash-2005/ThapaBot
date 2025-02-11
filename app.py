from flask import Flask, render_template, request, session, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1, #controls randomness 1:creative 0:deterministic
    "top_p": 0.95,#how our model choses words
    "top_k": 40,
    "max_output_tokens": 8192, #limits the length of the response
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="your  name is Alice and you are made by Mr Yash Thapa. You have to help people for anything that they ask for . try to be short but very accurate and please be very polite use emojis to be very create ask questions sometimes so that you can understand the user properly"
)

chat_histories = {}

@app.route('/')
def home():
    if 'sid' not in session:
        session['sid'] = os.urandom(16).hex()
        chat_histories[session['sid']] = []
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    to_exit = ["exit", "end", "bye", "quit", "see you"]
    
    if 'sid' not in session:
        return jsonify({'response': 'Session expired. Please refresh the page.', 'status': 'error'})
    
    sid = session['sid']
    history = chat_histories.get(sid, [])
    
    if user_input.lower() in to_exit:
        response = "Goodbye! Have a great day! 😊"
        del chat_histories[sid]
        session.pop('sid', None)
        return jsonify({'response': response, 'status': 'exit'})
    
    try:
        # Append user message to history
        history.append({"role": "user", "parts": [user_input]})
        
        # Start chat with existing history
        chat = model.start_chat(history=history)
        response = chat.send_message(user_input)
        bot_response = response.text
        
        # Append bot response to history
        history.append({"role": "model", "parts": [bot_response]})
        chat_histories[sid] = history
        
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}", 'status': 'error'})

# In app.py, modify the run command to:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Add this line