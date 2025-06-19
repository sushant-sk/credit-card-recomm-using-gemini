from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import get_recommendations, parse_income
from agent_logic import generate_final_recommendations
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
CORS(app)


load_dotenv()
api_key = os.getenv("api_key_google")

with open("card.json", "r") as file:
    card_data = json.load(file)

questions = [
    "What is your monthly income?",
    "Do you prefer travel, shopping, or cashback rewards?",
    "Do you travel internationally often?",
    "Do you want a credit card with no annual fee?",
    "How often do you use credit cards per month (rough estimate)?",
    "What is your age and occupation?",
]

# ✅ NEW: Persona logic based on income
def get_persona_by_income(income):
    if income < 25000:
        return "Entry-level earner who needs essential value with no fees."
    elif income < 60000:
        return "Young professional focused on cashback and savings."
    elif income < 150000:
        return "Mid-level corporate with lifestyle aspirations and moderate travel."
    elif income < 400000:
        return "High-income urban individual seeking premium perks and international travel."
    else:
        return "Ultra-high-net-worth frequent traveler who values luxury and elite access."

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        answers = request.get_json()
        if not isinstance(answers, dict):
            raise ValueError("Input must be a JSON object (dictionary)")
    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    try:
        user_income = parse_income(answers.get("What is your monthly income?", "0"))
        usage_per_month = int(answers.get("How often do you use credit cards per month (rough estimate)?", "0"))
        intl = "yes" in answers.get("Do you travel internationally often?", "no").lower()

        recommended_cards= get_recommendations(answers, card_data)
        top_cards = recommended_cards[:10]
        persona = get_persona_by_income(user_income)

        final_cards = generate_final_recommendations(
            recommended_cards=top_cards,
            answers=answers,
            user_income=user_income,
            usage_per_month=usage_per_month,
            intl=intl,
            persona=persona,
            api_key=api_key
        )

        return jsonify({"cards": final_cards})

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
