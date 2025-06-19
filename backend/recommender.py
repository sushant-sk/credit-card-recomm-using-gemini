import re

def parse_reward_rate(rate_str):
    rate_str = rate_str.lower()
    if "per" in rate_str:
        match = re.search(r"(\d+(\.\d+)?)\s+point[s]?\s+per\s+(?:\u20b9|rs\.?\s*)?(\d+)", rate_str)
        if match:
            points = float(match.group(1))
            spend = float(match.group(3))
            return round(points / spend, 4)
    elif "x" in rate_str:
        match = re.search(r"(\d+(\.\d+)?)x", rate_str)
        if match:
            return float(match.group(1)) * 0.01
    elif "%" in rate_str:
        match = re.search(r"(\d+(\.\d+)?)%", rate_str)
        if match:
            return float(match.group(1)) / 100
    return 0.005  

def parse_income(income_str):
    income_str = income_str.lower().strip()
    if "lakh" in income_str:
        num = float(re.sub(r"[^\d.]", "", income_str))
        return int(num * 100000)
    elif "crore" in income_str:
        num = float(re.sub(r"[^\d.]", "", income_str))
        return int(num * 10000000)
    else:
        digits = re.sub(r"[^\d]", "", income_str)
        return int(digits or 0)

def estimate_rewards(card, answers):
    try:
        income = parse_income(answers.get("What is your monthly income?", "0"))
        monthly_spend = 0.3 * income
        annual_spend = monthly_spend * 12
        reward_rate = card.get("reward_rate", 0.005)

        if isinstance(reward_rate, str):
            reward_rate = parse_reward_rate(reward_rate)

        if "yes" in answers.get("Do you travel internationally often?", "").lower():
            if "international" in str(card.get("reward_rate", "")).lower() or any("international" in str(p).lower() for p in card.get("perks", [])):
                reward_rate *= 1.5

        reward = round(annual_spend * reward_rate, 2)
        cap = card.get("max_reward_cap")
        return min(reward, cap) if cap else reward

    except:
        return 0

def score_card(card, user_answers):
    income = parse_income(user_answers.get("What is your monthly income?", "0"))
    credit_score = 775
    raw_reward_pref = user_answers.get("Do you prefer travel, shopping, or cashback rewards?", "").lower()
    intl = "yes" in user_answers.get("Do you travel internationally often?", "").lower()

    
    if income >= 1000000:
        persona = "ultra-high"
    elif income >= 150000:
        persona = "high"
    elif income >= 60000:
        persona = "mid"
    else:
        persona = "low"

    score = 0

    
    min_income = card.get("min_income") or 0
    if income >= min_income:
        score += 15

    required_score = card.get("credit_score_required") or 0
    if credit_score >= required_score:
        score += 10

    
    prefs = [p.strip() for p in re.split(r"[,\s]+", raw_reward_pref) if p.strip()]
    reward_type = str(card.get("reward_type", "")).lower()
    if any(pref in reward_type for pref in prefs):
        score += 10

    if intl and any("international" in str(p).lower() or "forex" in str(p).lower() for p in card.get("perks", [])):
        score += 10

    
    perks_str = str(card.get("perks", [])).lower()
    name_str = card.get("name", "").lower()
    issuer = card.get("issuer", "").lower()

    perk_score = 0

    if persona in ["low", "mid"]:
        if "cinema" in perks_str or "movie" in perks_str:
            perk_score += 5
        if "dining" in perks_str or "restaurant" in perks_str:
            perk_score += 5
        if "fuel" in perks_str:
            perk_score += 3
        if "health" in perks_str or "insurance" in perks_str:
            perk_score += 5
    elif persona == "high":
        if "dining" in perks_str:
            perk_score += 2
        if "health" in perks_str:
            perk_score += 1

    if persona == "ultra-high":
        if "golf" in perks_str:
            perk_score += 10
        if "taj" in perks_str:
            perk_score += 12
        if "club marriott" in perks_str:
            perk_score += 10
        if "0% forex" in perks_str:
            perk_score += 10
        if "exclusive" in perks_str or "private" in name_str:
            perk_score += 10

    
    reward_rate = card.get("reward_rate", 0.005)
    if isinstance(reward_rate, str):
        reward_rate = parse_reward_rate(reward_rate)

    if reward_rate >= 0.015 and "cashback" in reward_type:
        if persona == "low":
            perk_score += 6
        elif persona == "mid":
            perk_score += 5
        elif persona == "high":
            perk_score += 3
        elif persona == "ultra-high":
            perk_score += 1

    perk_score = min(perk_score, 20)
    score += perk_score

    
    if issuer in ["american express", "hdfc", "axis"]:
        score += 7

    if "private" in name_str or "platinum" in name_str:
        score += 4

    
    fee = card.get("annual_fee") or 0
    if persona == "ultra-high":
        if "infinia" in name_str:
            score += 15
        elif "platinum" in name_str:
            score += 6

        if "american express" in issuer:
            if "platinum" in name_str:
                score += 20
            else:
                score += 6

        if fee >= 45000:
            score += 30
        elif fee >= 30000:
            score += 15
        elif fee < 2000:
            score -= 5
    elif persona == "high":
        if fee > 10000:
            score -= 3
    elif persona == "mid":
        if fee > 3000:
            score -= 5
    else:
        if fee > 1000:
            score -= 7

    return score

def get_recommendations(user_answers, card_data):
    eligible_cards = []
    fallback_cards = []
    user_income = parse_income(user_answers.get("What is your monthly income?", "0"))
    international_travel = user_answers.get("Do you travel internationally often?", "").lower()

    for card in card_data:
        estimated_reward = estimate_rewards(card, user_answers)
        score = score_card(card, user_answers)
        perks = [p.lower() for p in card.get("perks", []) if isinstance(p, str)]

        if international_travel == "yes" and any("lounge" in p for p in perks):
            score += 1.5

        card["estimated_reward"] = estimated_reward

        fee = card.get("annual_fee") or 1
        final_score = score + estimated_reward / (5000 if user_income >= 1000000 else 10000)
        card["score"] = final_score

        print(f"{card.get('name', 'Unknown')}: score={score:.2f}, reward={estimated_reward:.2f}, final={final_score:.2f}")

        min_income = card.get("min_income") or 0
        if user_income >= min_income:
            eligible_cards.append((final_score, card))
        else:
            fallback_cards.append((final_score, card))

    eligible_cards.sort(reverse=True, key=lambda x: x[0])
    fallback_cards.sort(reverse=True, key=lambda x: x[0])

    combined = eligible_cards[:8] + fallback_cards[:4]
    combined = sorted(combined, reverse=True, key=lambda x: x[0])[:10]

    return [card for _, card in combined]








