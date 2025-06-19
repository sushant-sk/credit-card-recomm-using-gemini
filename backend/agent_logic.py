import google.generativeai as genai
import re

def generate_final_recommendations(
    recommended_cards,
    answers,
    user_income,
    usage_per_month,
    intl,
    persona,
    api_key
):
    if not isinstance(answers, dict):
        raise ValueError(f"'answers' must be a dict, but got {type(answers).__name__}")

    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    
    context = f"""
- Monthly Income: ₹{user_income}
- Reward Preference: {answers.get("Do you prefer travel, shopping, or cashback rewards?", "N/A")}
- International Travel: {'yes' if intl else 'no'}
- Annual Fee Preference: {answers.get("Do you want a credit card with no annual fee?", "N/A")}
- Monthly Card Usage: ₹{usage_per_month}
- Age and Occupation: {answers.get("What is your age and occupation?", "N/A")}
- Persona: {persona}
"""

    
    cards_for_gemini = recommended_cards[:10]

    card_lines = []
    for idx, card in enumerate(cards_for_gemini, start=1):
        name = card.get("name", "Unknown")
        fee = card.get("annual_fee", 0)
        est_reward = card.get("estimated_reward", 0)
        score = round(card.get("score", 0), 2)
        reward_type = card.get("reward_type", "N/A")
        perks = card.get("perks", [])
        perks_str = ", ".join(perks) if isinstance(perks, list) else str(perks)
        ratio = round(est_reward / fee, 2) if fee else 9999.0

        card_lines.append(
            f"{idx}. {name} | Score: {score} | Fee: ₹{fee} | Reward: ₹{est_reward} | Ratio: {ratio} | Perks: {perks_str}"
        )

    card_summary = "\n".join(card_lines)

    
    prompt = f"""
You're a super-friendly, enthusiastic Indian credit card expert who’s obsessed with helping people make smart financial choices and unlock elite perks! When a user gives you their details, greet them warmly like an excited financial best friend who *lives and breathes credit cards*.
You're upbeat, playful, and clever — but always practical and helpful. Think of yourself as a premium concierge who’s thrilled to craft the perfect credit card match. Start the summary with a lively and personalized welcome that reflects their vibe — income, job, goals, spending — and set the mood like you’re about to drop some secret hacks only insiders know.

DO NOT ASSUME THE USER'S NAME OR GENDER AT ALL.
The user’s profile is:
{context}

Here are 10 shortlisted credit cards based on their profile. Each card includes its Score (based on internal logic), annual fee, estimated reward, reward-to-fee ratio, and perks.

Please do the following:
1. Start with a short friendly intro (3–4 lines) addressing the user directly — summarizing what kind of person they are and what kind of cards they might love.
2. Then, categorize the cards into 3 buckets:

---

✅ **Top Picks (Best for You)**  
Pick exactly 3 cards. For each, explain why it matches their lifestyle, spend pattern, or reward preference.  
Also mention the annual and joining fees, and how those align with the user's preferences.  
Highlight the top perks that the user will likely love based on their profile.  
Format:  
`1. ✅ Card Name (Score: X.XX) – [Explanation]`  
`Top perks: [Mentioned Perks]`

---

⚠️ **Situational Picks (Good in Certain Cases)**  
Pick 2 cards that might be useful in specific scenarios (like lounge access, fuel, or zero-fee perks).  
Format:  
`4. ⚠️ Card Name (Score: X.XX) – [When or why to consider it]`  
`Perks: [Relevant niche perks to mention]`

---

❌ **Poor Fits (Avoid These)**  
Pick 3 cards that don’t fit the user’s lifestyle due to bad reward-to-fee ratios or irrelevant features.  
Format:  
`6. ❌ Card Name (Score: X.XX) – [Why it’s not suitable]`

---

🎯 Rules:
- Use only the cards below (do not invent names).
- Be warm, human, and playful when needed.
- Avoid bullet points; use clean paragraphs and numbered card lists.
- Don’t repeat cards across categories.
- Always select 8 unique cards.

Here are the 10 candidate cards:
{card_summary}
"""

    try:
        response = model.generate_content(prompt)

        if response.text:
            explanation = (
                response.text.strip()
                    .replace("• ", "")
                    .replace("•", "")
                    .replace("–", "-")
                    .replace("---", "\n---\n")
            )

            
            explanation = re.sub(r"\*\*Top Picks \(Best for You\)\*\*", "Top Picks (Best for You)", explanation)
            explanation = re.sub(r"\*\*Situational Picks \(Good in Certain Cases\)\*\*", "Situational Picks (Good in Certain Cases)", explanation)
            explanation = re.sub(r"\*\*Poor Fits \(Avoid These\)\*\*", "Poor Fits (Avoid These)", explanation)

            
            explanation = "\n".join(
                line.strip() for line in explanation.splitlines() if line.strip()
            )
            explanation = re.sub(r'\n{2,}', '\n\n', explanation)
        else:
            explanation = "No explanation returned."

        
        lines = explanation.splitlines()
        verdict_count = len([l for l in lines if any(m in l for m in ['✅', '⚠️', '❌'])])
        if verdict_count < 8:
            explanation += "\n⚠️ Warning: Fewer than 8 unique recommendations detected."

    except Exception as e:
        explanation = f"Error generating explanation: {str(e)}"

    
    final_cards = [
        {
            "name": card.get("name"),
            "reward_type": card.get("reward_type"),
            "annual_fee": card.get("annual_fee"),
            "perks": card.get("perks"),
            "estimated_reward": card.get("estimated_reward"),
        }
        for card in recommended_cards
    ]

    return {
        "card_list": final_cards,
        "gemini_recommendation": explanation
    }
