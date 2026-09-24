from typed_decisions.open_jev import OpenJev

MODEL_NAME = "com-kotobalabs/open-jev-deberta-v3-large"
MESSAGE = "I was charged twice for the same order and nobody answers my emails. I want my money back."
QUESTIONS = [
    {"type": "choice", "instructions": "Which product area is the message about?",
     "options": ["fees & charges", "pin & security", "refund & dispute", "top-up", "exchange & fiat", "atm & cash", "transfer", "card", "account & identity", "other"]},
    {"type": "score", "instructions": "How positive is the sentiment of this message?",
     "options": ["very negative", "negative", "neutral", "positive", "very positive"]},
    {"type": "noul", "instructions": "The customer is asking for a refund."},
]

def load_model():
    return OpenJev.from_pretrained(MODEL_NAME)

def run_decision(model, message, questions):
    return model.decide(message, questions)

def main():
    model = load_model()
    result = run_decision(model, MESSAGE, QUESTIONS)
    print(result)

if __name__ == "__main__":
    main()
