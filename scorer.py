def score_ad(headline, description):
    score = 0
    reasons = []

    if len(headline) <= 30:
        score += 25
        reasons.append("✅ Headline within character limit")
    else:
        reasons.append("❌ Headline too long")

    power_words = ["free", "instant", "guaranteed", "proven",
                   "save", "now", "limited", "exclusive", "best", "top"]
    if any(word in description.lower() for word in power_words):
        score += 25
        reasons.append("✅ Contains power words")
    else:
        reasons.append("❌ No power words found")

    if "!" in description or "?" in description:
        score += 25
        reasons.append("✅ Has emotional punctuation")
    else:
        reasons.append("❌ Missing emotional punctuation")

    cta_words = ["try", "get", "start", "buy", "join",
                 "discover", "shop", "learn", "sign up", "claim"]
    if any(word in description.lower() for word in cta_words):
        score += 25
        reasons.append("✅ Has a clear CTA")
    else:
        reasons.append("❌ No clear CTA")

    return score, reasons
