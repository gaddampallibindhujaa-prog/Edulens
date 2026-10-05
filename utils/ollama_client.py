import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt, model):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()
    return response.json()["response"]

def generate_questions(material, difficulty, num_questions, categories, model):

    material = material[:3000]

    prompt = f"""
Create {num_questions} multiple choice questions from this material.

Difficulty: {difficulty}

For each question use exactly this format:

QUESTION: What is ...?
A) Option 1
B) Option 2
C) Option 3
D) Option 4
ANSWER: A
CATEGORY: Concept Understanding
TOPIC: Topic

Material:
{material}
"""

    raw = ask_ollama(prompt, model)

    # Show Ollama's actual response
    print("\n--- OLLAMA RESPONSE ---")
    print(raw)
    print("--- END RESPONSE ---\n")

    questions = []
    blocks = raw.split("QUESTION:")

    for i, block in enumerate(blocks[1:], 1):

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if len(lines) < 6:
            continue

        question = lines[0]

        options = []

        for line in lines:
            if line.startswith("A)"):
                options.append(line[2:].strip())
            elif line.startswith("B)"):
                options.append(line[2:].strip())
            elif line.startswith("C)"):
                options.append(line[2:].strip())
            elif line.startswith("D)"):
                options.append(line[2:].strip())

        answer = "A"

        for line in lines:
            if line.startswith("ANSWER:"):
                answer = line.replace("ANSWER:", "").strip()

        if len(options) == 4:

            correct = {
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3]
            }

            questions.append({
                "id": f"q{i}",
                "type": "mcq",
                "question": question,
                "options": options,
                "correct_answer": correct.get(answer, options[0]),
                "category": "Concept Understanding",
                "topic": "General",
                "marks": 1
            })

    if not questions:
        raise ValueError(
            "No questions were detected. Check the Ollama response in the terminal."
        )

    return questions[:num_questions]

def evaluate_open_answer(question, answer, model):

    prompt = f"""
Question: {question}

Student answer: {answer}

Is the answer Correct, Partially Correct, or Incorrect?
Give one short reason.
"""

    return ask_ollama(prompt, model)


def generate_weakness_summary(topic_scores, model):

    prompt = f"""
These are the topic scores:

{topic_scores}

Identify the weak topics and give 2 short improvement suggestions.
"""

    return ask_ollama(prompt, model)