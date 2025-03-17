from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for Wix

# Load OpenAI API Key from Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_key_messages(file_content):
    """Extract key messages and themes from the positioning strategy document."""
    prompt = f"Analyze the following document and extract key messages, tone, and themes:\n\n{file_content}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI marketing strategist."},
                  {"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

def generate_content_ideas(key_messages, audience, content_types):
    """Generate content ideas based on extracted themes and content types."""
    prompt = f"Generate content ideas for {audience} based on these key messages: {key_messages}. The content types should include: {', '.join(content_types)}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content'].split("\n")

def generate_posting_schedule(start_date, num_days, content_ideas):
    """Generate an optimal posting schedule."""
    schedule = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        schedule.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Content Idea": content_ideas[i % len(content_ideas)]
        })
        current_date += datetime.timedelta(days=1)

    return schedule

@app.route('/')
def home():
    return jsonify({"message": "Flask API is running!"})

@app.route('/generate-calendar', methods=['POST'])
def generate_calendar():
    """API Endpoint to generate a content calendar."""
    data = request.json
    start_date = data.get("start_date", datetime.datetime.today().strftime("%Y-%m-%d"))
    audience = data.get("audience", "general audience")
    content_types = data.get("content_types", ["Blog Post", "Social Media Post"])
    file_content = data.get("file_content", "")

    if not file_content:
        return jsonify({"error": "No positioning strategy provided"}), 400

    # Generate content
    key_messages = extract_key_messages(file_content)
    content_ideas = generate_content_ideas(key_messages, audience, content_types)
    schedule = generate_posting_schedule(start_date, 7, content_ideas)

    return jsonify({"schedule": schedule, "content_ideas": content_ideas})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
