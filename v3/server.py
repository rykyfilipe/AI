import random

from v3.ContentGenerator import ContentGenerator
from v3.Evaluator import Evaluator

KNOWLEDGE_BASE = {
    "C1: Search Problems": {
        "n-queens": {
            "description": "Problema de a plasa N regine pe o tabla de sah astfel incat sa nu se atace.",
            "strategies": ["backtracking", "local search (min-conflicts)", "genetic algorithms"],
            "optimizations": ["MRV (Minimum Remaining Values)", "Forward Checking"],
            "type": "search_strategy"
        },
        "knight_tour": {
            "description": "Problema calaretului - parcurgerea tuturor patratelor unei table o singura data.",
            "strategies": ["backtracking", "Warnsdorff's rule"],
            "optimizations": ["pruning"],
            "type": "search_strategy"
        }
    },
    "C2: Constraint Satisfaction": {
        "graph_coloring": {
            "description": "Colorarea unui graf cu numarul minim de culori astfel incat nodurile adiacente sa aiba culori diferite.",
            "strategies": ["backtracking", "constraint satisfaction", "greedy coloring"],
            "optimizations": ["MRV", "Forward Checking", "AC-3"],
            "type": "csp"
        },
        "hanoi": {
            "description": "Problema Turnurilor din Hanoi - mutarea unui stack de discuri de diferite marimi intre tije.",
            "strategies": ["recursion", "dynamic programming", "backtracking"],
            "optimizations": ["memoization"],
            "type": "search_strategy"
        }
    },
    "C3: Game Theory": {
        "nash_equilibrium": {
            "description": "Situatia in care niciun jucator nu castiga schimbandu-si strategia unilateral.",
            "strategies": ["dominance elimination", "best response"],
            "optimizations": [],
            "type": "matrix_game"
        },
        "minmax_alphabeta": {
            "description": "Algoritm pentru jocuri cu suma nula, folosind taierea ramurilor inutile.",
            "strategies": ["minimax", "alpha-beta pruning"],
            "optimizations": ["move ordering", "transposition tables"],
            "type": "tree_game"
        }
    }
}

SYNONYMS = {
    "n-queens": ["n-queens", "regine"],
    "knight_tour": ["knight tour", "calarel", "calaret"],
    "graph_coloring": ["graph coloring", "colorare graf", "coloring", "colorare"],
    "hanoi": ["hanoi", "turnuri"],
    "nash_equilibrium": ["nash", "echilibru"],
    "minmax_alphabeta": ["minmax", "alpha-beta", "arbore", "tree"],
}

def get_topic_from_prompt(prompt):
    p_norm = prompt.lower()

    # Check for course requests (c1, c2, c3)
    if "c1" in p_norm or "curs 1" in p_norm or "search" in p_norm:
        course = KNOWLEDGE_BASE["C1: Search Problems"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]
    elif "c2" in p_norm or "curs 2" in p_norm or "csp" in p_norm or "constraint" in p_norm:
        course = KNOWLEDGE_BASE["C2: Constraint Satisfaction"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]
    elif "c3" in p_norm or "curs 3" in p_norm or "game" in p_norm or "teorie" in p_norm:
        course = KNOWLEDGE_BASE["C3: Game Theory"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]

    # Check for specific topic synonyms
    for topic_key, synonyms in SYNONYMS.items():
        if any(s in p_norm for s in synonyms):
            # Search in KB
            for course in KNOWLEDGE_BASE.values():
                if topic_key in course:
                    return topic_key, course[topic_key]

    # Fallback default
    return "minmax_alphabeta", KNOWLEDGE_BASE["C3: Game Theory"]["minmax_alphabeta"]


from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

generator = ContentGenerator()
evaluator = Evaluator()


@app.route("/api/message", methods=["POST"])
def question():
    prompt = request.get_json().get("message", "")
    import re

    match = re.search(r"(\d+)\s+intrebari", prompt, re.IGNORECASE)

    nr_intrebari = 1
    if match:
        nr_intrebari = int(match.group(1))

    else:
        nr_intrebari = 1

    questions = []

    for i in range(nr_intrebari):

        if any(keyword in prompt.lower() for keyword in ["selectie problema", "alegere", "problem selection"]):
            print("--- Tip: Alegere dintre 4+ probleme cu instanță ---")
            bundle = generator.generate_problem_selection_question()

            # Display Question
            print(f"\n[AI Question]:\n{bundle.question_text}")

            questions.append({
                "question": bundle.question_text,
                "answer": bundle.correct_answer_text,
                "topic": bundle.topic_info,
            })
        else:
            # 1. Identify Topic
            topic_key, topic_data = get_topic_from_prompt(prompt)
            print(f"--- Subiect identificat: {topic_key} ---")

            # 2. Generate Bundle (Question + Pre-computed Answer)
            bundle = generator.create_question(topic_key, topic_data)

            questions.append({
                "question": bundle.question_text,
                "answer": bundle.correct_answer_text,
                "topic": bundle.topic_info,
            })

    return jsonify({"questions": questions}), 200


@app.route("/api/evaluate", methods=["POST"])
def score():
    data = request.get_json()


    resultat = evaluator.evaluate(data.get("response", ""), data.get("bundle", ""))
    return jsonify(resultat)


if __name__ == "__main__":
    app.run(port=3000, debug=True)