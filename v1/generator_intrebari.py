import random
from knowledge import cursuri, sabloane_intrebari
from generative_functions import generate_normal_form_matrix
# GENERATOR DE ÎNTREBĂRI
class GeneratorIntrebari:
    def __init__(self):
        pass

    def genereaza_o_intrebare_din_subiect(self, subiect):
        """Generează o întrebare din subiect."""
        if subiect in cursuri:
            probleme = list(cursuri[subiect].keys())
            problema = random.choice(probleme)
        else:
            problema = subiect

        intrebare = self._genereaza_o_intrebare(problema)
        info = self._get_info_problema(problema)
        return {
            "intrebare": intrebare,
            "problema": problema,
            "info": info,
        }


    def _genereaza_o_intrebare(self, problema):
        print(f"Problema: {problema} -------------------------")
        info_problema = None
        curs_nume = None
        for nume_curs, curs in cursuri.items():
            if problema in curs:
                info_problema = curs[problema]
                curs_nume = nume_curs
                break
        print(f"Problem info: {info_problema} -------------------------")

        # Alege șablon potrivit pentru tipul problemei
        is_game_theory = curs_nume == "C3: Game Theory"
        if is_game_theory:
            candidati = [s for s in sabloane_intrebari if ("Nash" in s or "MinMax" in s or "Alpha-Beta" in s) or ("strategie" in s or "complexitate" in s)]
            print(f"These are the candidates:  {candidati}")
        else:
            # Exclude șabloanele specifice teoriei jocurilor
            candidati = [s for s in sabloane_intrebari if ("Nash" not in s and "Alpha-Beta" not in s)]
            # Dacă problema NU are optimizări de tip CSP (FC/MRV/AC-3), evită șablonul despre "asignarea variabilelor"
            opt_lower = [o.lower() for o in (info_problema.get("optimizari") or [])]
            are_csp_opt = any(x in opt_lower for x in ["fc", "mrv", "ac-3", "ac3", "ac 3"])
            if not are_csp_opt:
                candidati = [s for s in candidati if "asignarea variabilelor" not in s]
        sablon = random.choice(candidati if candidati else sabloane_intrebari)
        strategii = ", ".join(info_problema["strategii"])
        strategie = random.choice(info_problema["strategii"])
        optimizari = ", ".join(info_problema["optimizari"]) if info_problema["optimizari"] else "N/A"

        if "C3" in problema or "nash" in problema:
            joc = "[\n" + ",\n".join(str(row) for row in generate_normal_form_matrix()) + "\n]"

        intrebare = sablon.format(
            problema=problema.replace("_", " "),
            strategii=strategii,
            strategie=strategie,
            optimizari=optimizari,
            joc=joc
        )

        print(f"Intrebare: {intrebare}")
        return intrebare

    def _get_info_problema(self, problema):
        for curs in cursuri.values():
            if problema in curs:
                return curs[problema]
        return None


