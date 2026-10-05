def calculate_results(questions, answers):
    score = 0
    max_score = 0
    categories = {}
    topics = {}
    question_results = {}

    for q in questions:
        qid = q["id"]
        category = q.get("category", "Concept Understanding")
        topic = q.get("topic", "General")
        marks = int(q.get("marks", 1))
        answer = answers.get(qid)

        max_score += marks

        if q.get("type") == "mcq":
            correct = (
                answer is not None
                and str(answer).strip().lower()
                == str(q.get("correct_answer", "")).strip().lower()
            )
            earned = marks if correct else 0
        else:
            evaluation = q.get("_evaluation", {})
            correct = bool(evaluation.get("correct", False))
            earned = marks if correct else 0

        score += earned
        question_results[qid] = {"correct": correct, "earned": earned}

        if category not in categories:
            categories[category] = {"correct": 0, "total": 0}
        categories[category]["total"] += 1
        categories[category]["correct"] += int(correct)

        if topic not in topics:
            topics[topic] = {"correct": 0, "total": 0}
        topics[topic]["total"] += 1
        topics[topic]["correct"] += int(correct)

    for data in categories.values():
        data["accuracy"] = round(data["correct"] / data["total"] * 100, 1)

    for data in topics.values():
        data["accuracy"] = round(data["correct"] / data["total"] * 100, 1)

    accuracy = round(score / max_score * 100, 1) if max_score else 0

    return {
        "score": score,
        "max_score": max_score,
        "accuracy": accuracy,
        "total_questions": len(questions),
        "categories": categories,
        "topics": topics,
        "question_results": question_results
    }
