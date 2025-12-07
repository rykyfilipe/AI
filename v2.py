import random
import math
import re
from typing import List, Dict, Any, Tuple

# ==========================================
# 1. KNOWLEDGE BASE (Romanian Content)
# ==========================================
KNOWLEDGE_BASE = {
    "C1: Search Problems": {
        "n-queens": {
            "description": "Problema de a plasa N regine pe o tabla de sah astfel incat sa nu se atace.",
            "strategies": ["backtracking", "local search (min-conflicts)", "genetic algorithms"],
            "optimizations": ["MRV (Minimum Remaining Values)", "Forward Checking"],
        },
        "knight_tour": {
            "description": "Problema calaretului - parcurgerea tuturor patratelor unei table o singura data.",
            "strategies": ["backtracking", "Warnsdorff's rule"],
            "optimizations": ["pruning"],
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
    "nash_equilibrium": ["nash", "echilibru"],
    "minmax_alphabeta": ["minmax", "alpha-beta", "arbore", "tree"],
}


# ==========================================
# 2. DOMAIN LOGIC (Solvers & Generators)
# ==========================================

class Node:
    """Represents a node in the Game Tree."""

    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

    def is_leaf(self):
        return len(self.children) == 0


class GameEngine:
    """Handles the math/logic: Tree generation, Nash solving, Minimax."""

    @staticmethod
    def generate_random_tree(depth, branching_factor, min_val=1, max_val=20):
        if depth == 0:
            return Node(value=random.randint(min_val, max_val))
        node = Node()
        for _ in range(branching_factor):
            node.children.append(GameEngine.generate_random_tree(depth - 1, branching_factor, min_val, max_val))
        return node

    @staticmethod
    def tree_to_ascii(node, prefix="", is_last=True, is_max=True, accumulator=None):
        """Creates a string representation of the tree."""
        if accumulator is None:
            accumulator = []

        connector = "└── " if is_last else "├── "
        label = f"({node.value})" if node.is_leaf() else ("MAX" if is_max else "MIN")
        accumulator.append(f"{prefix}{connector}{label}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            GameEngine.tree_to_ascii(child, child_prefix, is_last_child, not is_max, accumulator)

        return "\n".join(accumulator)

    @staticmethod
    def solve_alpha_beta(root_node):
        """Returns (root_value, visited_leaves_count)."""
        visited_leaves = 0

        def alpha_beta(node, alpha, beta, is_max):
            nonlocal visited_leaves
            if node.is_leaf():
                visited_leaves += 1
                return node.value

            if is_max:
                v = -math.inf
                for child in node.children:
                    v = max(v, alpha_beta(child, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha: break
                return v
            else:
                v = math.inf
                for child in node.children:
                    v = min(v, alpha_beta(child, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha: break
                return v

        val = alpha_beta(root_node, -math.inf, math.inf, True)
        return val, visited_leaves

    @staticmethod
    def generate_nash_matrix(rows=2, cols=2):
        return [[(random.randint(0, 9), random.randint(0, 9)) for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def format_matrix(matrix):
        return "[\n" + ",\n".join([str(row) for row in matrix]) + "\n]"

    @staticmethod
    def solve_nash(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        equilibria = []

        # Find Best Response for P1 (Row player matches Row index)
        best_r = {c: [] for c in range(cols)}
        for c in range(cols):
            max_val = max(matrix[r][c][0] for r in range(rows))
            for r in range(rows):
                if matrix[r][c][0] == max_val: best_r[c].append(r)

        # Find Best Response for P2 (Col player matches Col index)
        best_c = {r: [] for r in range(rows)}
        for r in range(rows):
            max_val = max(matrix[r][c][1] for c in range(cols))
            for c in range(cols):
                if matrix[r][c][1] == max_val: best_c[r].append(c)

        # Intersection
        for r in range(rows):
            for c in range(cols):
                if r in best_r[c] and c in best_c[r]:
                    equilibria.append(f"(Row {r}, Col {c}) -> Payoffs {matrix[r][c]}")

        return equilibria if equilibria else ["Niciun echilibru Nash pur"]


# ==========================================
# 3. QUESTION GENERATOR ENGINE
# ==========================================

class QuestionBundle:
    """Holds everything needed: The question text and the computed answer."""

    def __init__(self, question_text, correct_answer_text, topic_info):
        self.question_text = question_text
        self.correct_answer_text = correct_answer_text
        self.topic_info = topic_info


class ContentGenerator:
    def __init__(self):
        self.engine = GameEngine()

    def create_question(self, topic_key, topic_data):
        """Factory method to dispatch based on topic type."""

        # 1. Handle Tree Games (Minimax)
        if topic_data.get("type") == "tree_game":
            return self._create_minimax_bundle(topic_data)

        # 2. Handle Matrix Games (Nash)
        elif topic_data.get("type") == "matrix_game":
            return self._create_nash_bundle(topic_data)

        # 3. Handle Theory Questions (Default)
        else:
            return self._create_theory_bundle(topic_key, topic_data)

    def _create_minimax_bundle(self, info):
        # Generate Data First
        depth = random.randint(2, 3)
        branching = 2
        tree = self.engine.generate_random_tree(depth, branching)

        # Solve Data
        root_val, visited = self.engine.solve_alpha_beta(tree)

        # Format Text
        tree_str = self.engine.tree_to_ascii(tree)
        question = (
            f"Se dă următorul arbore de joc (Rădăcina este MAX):\n\n{tree_str}\n\n"
            f"1. Care este valoarea în rădăcină folosind MinMax?\n"
            f"2. Câte noduri FRUNZĂ sunt vizitate dacă aplicăm Alpha-Beta Pruning (stânga-dreapta)?"
        )

        answer = (
            f"Valoarea în rădăcină este {root_val}. "
            f"Numărul de frunze vizitate cu Alpha-Beta este {visited}."
        )

        return QuestionBundle(question, answer, info)

    def _create_nash_bundle(self, info):
        # Generate Data
        matrix = self.engine.generate_nash_matrix()

        # Solve Data
        solutions = self.engine.solve_nash(matrix)
        solutions_str = "; ".join(solutions)

        # Format Text
        mat_str = self.engine.format_matrix(matrix)
        question = (
            f"Pentru jocul în formă normală de mai jos (tuplele sunt (J1, J2)):\n{mat_str}\n"
            f"Identifică toate echilibrele Nash pure."
        )

        answer = f"Echilibrele Nash sunt: {solutions_str}."

        return QuestionBundle(question, answer, info)

    def _create_theory_bundle(self, key, info):
        templates = [
            ("De ce este {strat} o strategie bună pentru {prob}?",
             "{strat} este utilă pentru {prob} deoarece {desc}."),

            ("Ce optimizări se pot aplica la {prob}?",
             "Pentru {prob} se pot folosi: {opts}."),
        ]

        q_temp, a_temp = random.choice(templates)
        strat = random.choice(info["strategies"]) if info["strategies"] else "aceasta strategie"

        q_text = q_temp.format(strat=strat, prob=key.replace("_", " "))
        a_text = a_temp.format(strat=strat, prob=key.replace("_", " "),
                               desc=info["description"],
                               opts=", ".join(info["optimizations"]))

        return QuestionBundle(q_text, a_text, info)


# ==========================================
# 4. EVALUATOR
# ==========================================

class Evaluator:
    @staticmethod
    def normalize(text):
        return text.lower().replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")

    @staticmethod
    def cosine_similarity(s1, s2):
        # Simple implementation for dependency-free run
        def get_vec(text):
            words = re.findall(r'\w+', Evaluator.normalize(text))
            vec = {}
            for w in words: vec[w] = vec.get(w, 0) + 1
            return vec

        v1, v2 = get_vec(s1), get_vec(s2)
        intersection = set(v1.keys()) & set(v2.keys())
        numerator = sum([v1[x] * v2[x] for x in intersection])

        sum1 = sum([v1[x] ** 2 for x in v1.keys()])
        sum2 = sum([v2[x] ** 2 for x in v2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator: return 0.0
        return numerator / denominator

    def evaluate(self, user_answer, system_bundle):
        # 1. Similarity Check
        sim_score = self.cosine_similarity(user_answer, system_bundle.correct_answer_text)

        # 2. Keyword/Number Extraction Check (Hard check for Math problems)
        score = int(sim_score * 100)
        feedback = f"Similaritate semantică: {score}/100."

        # Extra logic for numeric answers (MinMax)
        if "vizitate" in system_bundle.correct_answer_text:
            nums_sys = re.findall(r'\d+', system_bundle.correct_answer_text)
            nums_user = re.findall(r'\d+', user_answer)
            # Check if the numbers in correct answer appear in user answer
            if set(nums_sys).issubset(set(nums_user)):
                score = 100
                feedback = "Corect! Ai identificat valorile numerice corecte."
            elif not nums_user:
                score = 0
                feedback = "Nu ai introdus nicio valoare numerică."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": system_bundle.correct_answer_text
        }


# ==========================================
# 5. MAIN PIPELINE
# ==========================================

def get_topic_from_prompt(prompt):
    p_norm = prompt.lower()
    for topic_key, synonyms in SYNONYMS.items():
        if any(s in p_norm for s in synonyms):
            # Search in KB
            for course in KNOWLEDGE_BASE.values():
                if topic_key in course:
                    return topic_key, course[topic_key]
    # Fallback default
    return "minmax_alphabeta", KNOWLEDGE_BASE["C3: Game Theory"]["minmax_alphabeta"]


def main():
    generator = ContentGenerator()
    evaluator = Evaluator()

    print("=== AI TEACHING ASSISTANT (GAME THEORY & SEARCH) ===")
    print("Exemple comenzi: 'genereaza minmax', 'intrebare nash', 'despre n-queens', 'exit'")

    while True:
        prompt = input("\nUser Input > ").strip()
        if prompt.lower() in ["exit", "quit"]:
            break

        # 1. Identify Topic
        topic_key, topic_data = get_topic_from_prompt(prompt)
        print(f"--- Subiect identificat: {topic_key} ---")

        # 2. Generate Bundle (Question + Pre-computed Answer)
        bundle = generator.create_question(topic_key, topic_data)

        # 3. Display Question
        print(f"\n[AI Question]:\n{bundle.question_text}")

        # 4. Get User Answer
        user_ans = input("\n[Your Answer]: ")

        # 5. Evaluate
        result = evaluator.evaluate(user_ans, bundle)

        print("\n--- REZULTAT ---")
        print(f"Scor: {result['score']}")
        print(f"Feedback: {result['feedback']}")
        print(f"Răspunsul corect era: {result['correct_answer']}")


if __name__ == "__main__":
    main()