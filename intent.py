
def detect_intent(message: str):

    msg = message.lower()

    if any(word in message for word in [
        "summarize",
        "summary",
        "what have we talked",
        "what we have talked",
        "recap",
        "repeat"
    ]):
        return "summary"

    if "career" in msg:
        return "career_query"

    if "love" in msg or "relationship" in msg:
        return "love_query"

    if "planet" in msg:
        return "planet_query"

    if "spiritual" in msg or "meditation" in msg:
        return "spiritual_query"

    return "general"


def should_retrieve(intent: str):

    retrieval_intents = [
        "career_query",
        "love_query",
        "planet_query",
        "spiritual_query"
    ]

    return intent in retrieval_intents