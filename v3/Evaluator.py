import math
import re


class Evaluator:
    @staticmethod
    def normalize(text):
        if not text: return ""
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

        if sum1 == 0 or sum2 == 0: return 0.0

        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator: return 0.0
        return numerator / denominator

    # Helper mutat în afara funcției evaluate pentru claritate
    @staticmethod
    def parse_tuple(text_chunk):
        # Caută toate secvențele de cifre, ignorând paranteze, litere sau virgule
        nums = [int(n) for n in re.findall(r'\d+', text_chunk)]
        return tuple(nums) if nums else None

    def evaluate(self, user_answer: str, system_bundle: dict) -> dict:
        # 1. Extragem textul corect (Siguranță dacă e None)
        correct_answer_text = system_bundle.get("correct_answer_text", "")

        if not correct_answer_text:
            return {"score": 0, "feedback": "Eroare: Răspunsul corect lipsește.", "correct_answer": ""}

        # 2. Similarity Check (Fallback)
        sim_score = self.cosine_similarity(user_answer, correct_answer_text)
        score = int(sim_score * 100)
        feedback = f"Similaritate semantică: {score}/100."

        # Normalizăm pentru verificări
        user_norm = Evaluator.normalize(user_answer)
        sys_norm = Evaluator.normalize(correct_answer_text)  # AICI era greșeala înainte

        # =========================================================
        # CAZ 1: LOGICĂ PENTRU MATH/MINMAX (Valori numerice)
        # =========================================================
        # Verificăm direct în textul normalizat, nu în dicționar cu cheie greșită
        if "vizitate" in sys_norm:
            nums_sys = re.findall(r'\d+', correct_answer_text)
            nums_user = re.findall(r'\d+', user_answer)

            # Verificăm dacă numerele din sistem sunt incluse în răspunsul userului
            if set(nums_sys).issubset(set(nums_user)):
                score = 100
                feedback = "Corect! Ai identificat valorile numerice corecte."
            elif not nums_user:
                score = 0
                feedback = "Nu ai introdus nicio valoare numerică."

        # =========================================================
        # CAZ 2: LOGICĂ PENTRU ECHILIBRU NASH / STRATEGII
        # =========================================================
        elif "echilibr" in sys_norm or "strategii" in sys_norm:

            # --- A. Extragerea CORECTĂ din sistem ---
            sys_pattern = r'(?:Profil|Strategii|Row|Col)\s*[:]?\s*([\[\(].*?[\]\)])'
            raw_sys_matches = re.findall(sys_pattern, correct_answer_text)

            if not raw_sys_matches:
                # Eliminăm zona de payoffs ca să nu ne încurce
                clean_text = re.sub(r'Payoffs\s*[\[\(].*?[\]\)]', '', correct_answer_text, flags=re.IGNORECASE)
                raw_sys_matches = re.findall(r'[\[\(].*?[\]\)]', clean_text)

            correct_coords = set()
            for m in raw_sys_matches:
                t = Evaluator.parse_tuple(m)
                if t: correct_coords.add(t)

            # --- B. Extragerea din răspunsul USER-ului ---
            raw_user_matches = re.findall(r'[\[\(].*?[\]\)]', user_answer)
            user_coords = set()

            # Dacă userul nu a pus paranteze (ex: "0 1"), încercăm să ghicim
            if not raw_user_matches and re.search(r'\d', user_answer):
                t = Evaluator.parse_tuple(user_answer)
                if t: user_coords.add(t)
            else:
                for m in raw_user_matches:
                    t = Evaluator.parse_tuple(m)
                    if t: user_coords.add(t)

            # --- C. Logica de Punctaj ---

            # Sub-caz: Sistemul spune că NU există echilibre
            if not correct_coords:
                negations = ["nu", "niciun", "none", "nimic", "zero", "inexistent"]
                has_negation = any(neg in user_norm for neg in negations)

                if has_negation:
                    score = 100
                    feedback = "Corect! Ai identificat că nu există niciun echilibru Nash pur."
                elif user_coords:
                    score = 0
                    feedback = "Greșit. Ai găsit echilibre, dar corect este că nu există."
                else:
                    feedback = f"Nu există echilibre. Similaritate răspuns: {score}%."

            # Sub-caz: Există echilibre
            else:
                if user_coords:
                    matched = user_coords & correct_coords

                    if len(matched) == len(correct_coords) and len(user_coords) == len(correct_coords):
                        score = 100
                        feedback = "Excelent! Ai identificat toate echilibrele corect."
                    elif matched:
                        ratio = len(matched) / len(correct_coords)
                        score = int(30 + (ratio * 70))
                        feedback = f"Parțial corect. Ai găsit {len(matched)} din {len(correct_coords)} echilibre."
                    else:
                        score = int(sim_score * 50)
                        feedback = f"Coordonatele propuse {list(user_coords)} nu sunt corecte. Corect era: {list(correct_coords)}."
                else:
                    feedback = f"Nu ai oferit coordonatele specifice (ex: (1, 1)). Similaritate text: {score}%."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": correct_answer_text
        }