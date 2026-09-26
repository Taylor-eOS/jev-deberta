import utils
from questions import QUESTIONS
from run_jev import load_segments
import settings

def format_segment_line(questions, answers):
    parts = []
    for question, answer in zip(questions, answers):
        formatter = utils.SHORT_FORMATTERS[question["type"]]
        parts.append(formatter(question, answer))
    return "\n".join(parts)

def main():
    segments = load_segments()
    model = utils.load_model()
    blocks = []
    for segment in segments:
        answers = utils.run_decision(model, segment, QUESTIONS)
        blocks.append(format_segment_line(QUESTIONS, answers))
    with open(settings.OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n\n".join(blocks))

if __name__ == "__main__":
    main()
