import utils
from questions import QUESTIONS
import settings

def load_segments():
    with open(settings.MESSAGE_FILE, "r", encoding="utf-8") as file:
        content = file.read()
    segments = [segment.strip() for segment in content.split("\n\n")]
    return [segment for segment in segments if segment]

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

def format_segment_block(message, questions, answers):
    lines = ["State", message, ""]
    for index, (question, answer) in enumerate(zip(questions, answers), start=1):
        lines.append(f"Question {index} ({question['type']})")
        lines.append(question["instructions"])
        formatter = FORMATTERS[question["type"]]
        lines.append(formatter(question, answer))
        lines.append("")
    return "\n".join(lines).rstrip("\n")

def main():
    segments = load_segments()
    model = utils.load_model()
    blocks = []
    for segment in segments:
        answers = utils.run_decision(model, segment, QUESTIONS)
        blocks.append(format_segment_block(segment, QUESTIONS, answers))
    with open(settings.OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n\n".join(blocks))

if __name__ == "__main__":
    main()
