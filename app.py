from flask import Flask, request, jsonify
import openai
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
openai.api_key = "your_openai_api_key"

def extract_key_messages(file_content):
    """Extract key messages and themes from the positioning strategy document"""
    prompt = f"Analyze the following document and extract the key messages, tone, and themes:\n\n{file_content}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI marketing strategist."},
                  {"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

def generate_content_ideas(key_messages, audience, content_types):
    """Generate content ideas based on extracted themes and content types"""
    prompt = f"Generate content ideas for {audience} based on these key messages: {key_messages}. The content types should include: {', '.join(content_types)}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

def generate_posting_schedule(start_date, num_days, content_ideas):
    """Generate an optimal posting schedule"""
    schedule = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        schedule.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Content Idea": content_ideas[i % len(content_ideas)]
        })
        current_date += timedelta(days=1)

    return schedule

@app.route('/generate-calendar', methods=['POST'])
def generate_calendar():
    data = request.json
    start_date = data.get("start_date", datetime.today().strftime("%Y-%m-%d"))
    audience = data.get("audience", "general audience")
    content_types = data.get("content_types", ["Blog Post", "Social Media Post"])
    file_content = data.get("file_content", "")

    key_messages = extract_key_messages(file_content)
    content_ideas = generate_content_ideas(key_messages, audience, content_types)
    schedule = generate_posting_schedule(start_date, 7, content_ideas.split("\n"))

    return jsonify({"schedule": schedule, "content_ideas": content_ideas})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow Wix to connect to Flask

@app.route('/generate-content', methods=['POST'])
def generate_content():
    data = request.json  # Get data sent from Wix
    
    # Example response (replace this with actual content generation logic)
    response = {
        "message": "Content calendar generated successfully!",
        "data": {
            "topics": ["Social Media Strategy", "Brand Positioning", "SEO Tips"],
            "posting_schedule": ["Monday 9 AM", "Wednesday 3 PM", "Friday 12 PM"]
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5001)  # Ensure you're running on an available port

