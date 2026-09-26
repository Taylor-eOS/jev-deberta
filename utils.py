from typed_decisions.open_jev import OpenJev

MODEL_NAME = "com-kotobalabs/open-jev-deberta-v3-large"

def load_model():
    return OpenJev.from_pretrained(MODEL_NAME)

def run_decision(model, message, questions):
    return model.decide(message, questions)

def format_choice_short(question, answer):
    return f"{answer['choice']} {answer['confidence']:.2f}"

def format_score_short(question, answer):
    top_option = max(answer["probabilities"], key=answer["probabilities"].get)
    top_probability = answer["probabilities"][top_option]
    return f"{top_option} {top_probability:.2f}"

def format_noul_short(question, answer):
    probability_yes = answer["noul"]
    verdict = "yes" if probability_yes >= 0.5 else "no"
    return f"{verdict} {probability_yes:.2f}"

SHORT_FORMATTERS = {
    "choice": format_choice_short,
    "score": format_score_short,
    "noul": format_noul_short,
}
