# GENERATOR DE RASPUNSURI

class GeneratorRaspunsuri:
    def genereaza(self, intrebare, problema, info):
        intrebare_l = intrebare.lower()

        # identifică o strategie menționată în întrebare, dacă există
        strategie_intrebata = None
        for s in info["strategii"]:
            if s.lower() in intrebare_l:
                strategie_intrebata = s
                break
        if not strategie_intrebata and info.get("strategii"):
            strategie_intrebata = info["strategii"][0]

        if "cea mai bună" in intrebare_l or "cea mai potrivită" in intrebare_l:
            return f"Pentru {problema.replace('_',' ')}, o strategie potrivită este {info['strategii'][0]}."

        if "strategie" in intrebare_l:
            strategii = ", ".join(info["strategii"])
            return f"Strategiile folosite pentru {problema.replace('_',' ')} sunt: {strategii}."

        if "avantaj" in intrebare_l or "de ce" in intrebare_l:
            s = strategie_intrebata or info['strategii'][0]
            return (
                f"{s} este eficient pentru {problema.replace('_',' ')} deoarece reduce spațiul de căutare, "
                f"poate ghida căutarea către soluții mai bune și uneori oferă rezultate aproape optimale; "
                f"totuși poate fi mai lent sau poate necesita euristici potrivite."
            )

        if "optimiz" in intrebare_l:
            if info["optimizari"]:
                return f"Optimizari folosite pentru {problema.replace('_',' ')}: {', '.join(info['optimizari'])}."
            else:
                return f"Pentru {problema.replace('_',' ')}, nu sunt specificate optimizari."

        if "complexitate" in intrebare_l:
            return f"Complexitatea depinde de strategie. De exemplu, {info['strategii'][0]} are o complexitate mare, dar este corecta, iar local search este mai rapida dar nu garanteaza solutia."

        if "nash" in intrebare_l:
            return "Echilibrul Nash apare cand niciun jucator nu poate castiga mai mult schimbandu-si strategia unilateral."

        if "minmax" in intrebare_l or "alpha-beta" in intrebare_l:
            return "MinMax exploreaza toate starile posibile, iar Alpha-Beta reduce numarul de noduri evaluate prin taierea ramurilor inutile."

        return f"{info['descriere']} Se poate rezolva cu: {', '.join(info['strategii'])}."
