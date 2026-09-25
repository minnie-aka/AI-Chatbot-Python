from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
import traceback

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key="AIXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
@app.route("/")
def home():
    return render_template("index.html")

def pet_advisor(user_input):
    print(f"\n--- NEW REQUEST: {user_input} ---")
    
    prompt = f"""
    You are a professional Pet Care Product Advisor with strong domain knowledge.

    Task:
    - Understand the pet type and specific problem
    - Recommend 2–3 relevant product categories
    - Give a short reason for each recommendation

    Rules:
    - Keep response within 3–5 lines
    - Focus on products, not medical diagnosis
    - If query is not pet-related, reply: "Sorry, I can only help with pet-related product queries."

    User Query: {user_input}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.3,
                top_p=0.8
            )
        )

        if response.text:
            print("STATUS: API WORKED SUCCESSFULLY")
            return response.text
        else:
            raise Exception("API returned an empty response.")

    except Exception as e:
        print(f"STATUS: API FAILED")
        print(f"ERROR DETAILS: {str(e)}")
        
        user = user_input.lower()
        if "dog" in user and "dry skin" in user:
            return "Use medicated dog shampoo and omega-3 supplements to improve skin hydration."
        elif "cat" in user:
            return "Use an anti-shedding brush and provide protein-rich food for healthy fur."
        elif any(word in user for word in ["pet","animal","bird","fish","rabbit"]):
            return "I recommend looking for specialized grooming tools and vitamin supplements for your pet's specific needs."
        else:
            return "Sorry, I can only help with pet-related product queries."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"reply": "Invalid request"}), 400

    user_input = data.get("message", "")
    reply = pet_advisor(user_input)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("Server starting on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
