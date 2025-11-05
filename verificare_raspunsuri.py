import re
import math
from knowledge import cursuri

class EvaluatorRaspunsuri:
    @staticmethod
    def normalize(text):
        return text.lower().replace("ă", "a").replace("î", "i").replace("ș","s").replace("ț","t")

    @staticmethod
    def _tokens(text: str):
        """Tokenizează simplu după normalizare; reține doar tokenuri alfanumerice de lungime >= 2."""
        t = EvaluatorRaspunsuri.normalize(text)
        toks = re.findall(r"\b\w+\b", t)
        return [w for w in toks if len(w) >= 2]

    @classmethod
    def cosine_similarity(cls, a: str, b: str) -> float:
        ta = cls._tokens(a)
        tb = cls._tokens(b)
        if not ta and not tb:
            return 1.0
        if not ta or not tb:
            return 0.0
        fa = {}
        fb = {}
        for w in ta:
            fa[w] = fa.get(w, 0) + 1
        for w in tb:
            fb[w] = fb.get(w, 0) + 1
        vocab = set(fa.keys()) | set(fb.keys())
        dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in vocab)
        na = math.sqrt(sum(v * v for v in fa.values()))
        nb = math.sqrt(sum(v * v for v in fb.values()))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def verifica(self, intrebare, raspuns, problema, info):
        intrebare_n = self.normalize(intrebare)
        raspuns_n = self.normalize(raspuns)

        scor = 0
        feedback = []

        # verificare strategie
        strategii = [self.normalize(s) for s in info["strategii"]]
        if any(s in raspuns_n for s in strategii):
            scor += 40
        else:
            feedback.append("Nu ai menționat o strategie corectă.")

        # verificare optimizari daca sunt cerute
        if "optimiz" in intrebare_n and info["optimizari"]:
            optimizari = [self.normalize(o) for o in info["optimizari"]]
            if any(o in raspuns_n for o in optimizari):
                scor += 30
            else:
                feedback.append("Nu ai menționat optimizările specifice problemei.")

        # verificare daca raspunde la conceptul intrebarii
        if any(kw in raspuns_n for kw in ["complexitate","timp","spatiu","o(n)", "mai rapid", "mai lent"]):
            scor += 20

        if any(kw in intrebare_n for kw in ["de ce", "avantaje"]):
            if any(kw in raspuns_n for kw in ["eficient", "rapid", "reduce","optimal","garanteaza","mai bun"]):
                scor += 20

        # bonus daca apare descrierea problemei
        if info["descriere"].split()[0].lower() in raspuns_n:
            scor += 10

        if scor > 100:
            scor = 100

        if scor < 60:
            feedback.insert(0, "Răspuns incomplet sau incorect.")
        else:
            feedback.insert(0, "Răspuns corect.")

        return {
            "scor": scor,
            "feedback": " ".join(feedback) if feedback else "Foarte bine!",
        }

    def compara(self, intrebare, raspuns_utilizator, raspuns_generat, problema, info):
        """Compară două răspunsuri (utilizator vs. generat) aplicând exact aceeași metodă de evaluare.

        Returnează ambele evaluări și un verdict simplu (utilizator >, = sau < generat) pe baza scorurilor.
        """
        eval_user = self.verifica(intrebare=intrebare, raspuns=raspuns_utilizator, problema=problema, info=info)
        eval_gen = self.verifica(intrebare=intrebare, raspuns=raspuns_generat, problema=problema, info=info)

        su = eval_user.get("scor", 0)
        sg = eval_gen.get("scor", 0)
        if su > sg:
            verdict = ">"
        elif su < sg:
            verdict = "<"
        else:
            verdict = "="

        sim = self.cosine_similarity(raspuns_utilizator or "", raspuns_generat or "")
        verdict_sim = "≈" if sim >= 0.8 else ("~" if sim >= 0.5 else "≠")
        scor_cosine = int(round(sim * 100))

        return {
            "scor_utilizator": su,
            "feedback_utilizator": eval_user.get("feedback", ""),
            "scor_generat": sg,
            "feedback_generat": eval_gen.get("feedback", ""),
            "verdict": verdict,
            "similaritate": sim,
            "verdict_sim": verdict_sim,
            "scor_cosine": scor_cosine,
        }

if __name__ == "__main__":
    # Exemplu de rulare locală
    evaluator = EvaluatorRaspunsuri()
    info = cursuri["C1: Search Problems"]["n-queens"]
    rez = evaluator.verifica(
        intrebare="De ce este backtracking o strategie buna pentru n-queens?",
        raspuns="Backtracking garanteaza solutia si exploreaza configuratiile eficiente.",
        problema="n-queens",
        info=info,
    )
    print(rez)
