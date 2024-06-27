from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Mood:
    emoji: str
    sentiment: float

def get_mood(input_text: str, *, threshold: float) -> Mood:
    sentiment: float = TextBlob(input_text).sentiment.polarity

    friendly_threshold: float = threshold
    hostile_threshold: float = -threshold

    if sentiment >= friendly_threshold:
        return Mood('😃', sentiment)
    elif sentiment <= hostile_threshold:
        return Mood('😢', sentiment)
    else:
        return Mood('😐', sentiment)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_text', methods=['POST'])
def send_text():
    data = request.get_json()
    text = data['text']
    mood = get_mood(text, threshold=0.2)
    
    return jsonify({'text': text, 'mood_emoji': mood.emoji, 'sentiment': mood.sentiment})

if __name__ == '__main__':
    app.run(debug=True)
