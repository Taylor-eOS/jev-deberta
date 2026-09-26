from typed_decisions.open_jev import OpenJev

MODEL_NAME = "com-kotobalabs/open-jev-deberta-v3-large"
MESSAGE = "Xenophon accompanied the Ten Thousand, a large army of Greek mercenaries hired by Cyrus the Younger, who intended to seize the throne of Persia from his brother, Artaxerxes II. Although Cyrus' mixed army fought to a tactical victory at Cunaxa in Babylon, Cyrus was killed, rendering the actions of the Greeks irrelevant and the expedition a failure."
QUESTIONS = [
    {"type": "choice", "instructions": "Was was the purpose of the expedition?",
     "options": ["fun", "training", "winning a throne", "going for a walk", "experience"]},
    {"type": "score", "instructions": "How positive is the sentiment of this message?",
     "options": ["very negative", "negative", "neutral", "positive", "very positive"]},
    {"type": "noul", "instructions": "This is a history book segment about modern history."},
]

def load_model():
    return OpenJev.from_pretrained(MODEL_NAME)

def run_decision(model, message, questions):
    return model.decide(message, questions)

def format_choice_answer(question, answer):
    lines = [f"Answer: {answer['choice']}", f"Confidence: {answer['confidence']:.2f}"]
    for option, probability in answer["probabilities"].items():
        lines.append(f"  {option}: {probability:.2f}")
    return "\n".join(lines)

def format_score_answer(question, answer):
    lines = [f"Answer: {answer['score']:.2f}", f"Confidence: {answer['confidence']:.2f}"]
    for option, probability in answer["probabilities"].items():
        lines.append(f"  {option}: {probability:.2f}")
    return "\n".join(lines)

def format_noul_answer(question, answer):
    probability_yes = answer["noul"]
    verdict = "yes" if probability_yes >= 0.5 else "no"
    return f"Answer: {verdict} (p(yes) = {probability_yes:.2f})"

FORMATTERS = {
    "choice": format_choice_answer,
    "score": format_score_answer,
    "noul": format_noul_answer,
}

def print_report(message, questions, answers):
    print("State")
    print(message)
    print()
    for index, (question, answer) in enumerate(zip(questions, answers), start=1):
        print(f"Question {index} ({question['type']})")
        print(question["instructions"])
        #if "options" in question:
        #    print("Options: " + ", ".join(question["options"]))
        formatter = FORMATTERS[question["type"]]
        print(formatter(question, answer))
        print()

def main():
    model = load_model()
    answers = run_decision(model, MESSAGE, QUESTIONS)
    print_report(MESSAGE, QUESTIONS, answers)

if __name__ == "__main__":
    main()
