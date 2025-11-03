# GENERATOR DE RASPUNSURI

class GeneratorRaspunsuri:
    def genereaza(self, intrebare, problema, info):
        intrebare_l = intrebare.lower()

        if "cea mai bună" in intrebare_l or "cea mai potrivită" in intrebare_l:
            return f"Pentru {problema.replace('_',' ')}, o strategie potrivita este {info['strategii'][0]}."

        if "strategie" in intrebare_l:
            strategii = ", ".join(info["strategii"])
            return f"Strategiile folosite pentru {problema.replace('_',' ')} sunt: {strategii}."

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
