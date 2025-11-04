import random
import re
from generator_raspunsuri import GeneratorRaspunsuri
from knowledge import cursuri, sinonime, sabloane_intrebari

# EXTRACTOR
class ExtractorParametri:
    @staticmethod
    def extrage_numar_intrebari(prompt):
        match = re.search(r'(\d+)\s*(întrebări|intrebari|questions|întrebare|intrebare|q|questions)', prompt, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 1

    @staticmethod
    def extrage_subiect(prompt):
        prompt_norm = prompt.lower().replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")
        prompt_norm = re.sub(r'\s+', ' ', prompt_norm)
        for topic, synonyms in sinonime.items():
            for syn in synonyms:
                if syn in prompt_norm:
                    return topic
        return None

# GENERATOR DE ÎNTREBĂRI
class GeneratorIntrebari:
    def __init__(self, genereaza_raspunsuri: bool = True):
        self.extractor = ExtractorParametri()
        self.raspuns_gen = GeneratorRaspunsuri()
        self.genereaza_raspunsuri = genereaza_raspunsuri

    def genereaza_o_intrebare_din_subiect(self, subiect):
        """Generează o întrebare (fără print și fără răspuns auto)."""
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

    def genereaza_din_prompt(self, prompt):
        print(f"\nPrompt: '{prompt}'\n")
        numar_intrebari = self.extractor.extrage_numar_intrebari(prompt)
        subiect = self.extractor.extrage_subiect(prompt)

        if subiect is None:
            print("Nu am putut identifica subiectul din prompt.")
            self._afiseaza_subiecte_disponibile()
            return []

        if subiect in cursuri:
            return self._genereaza_din_curs(subiect, numar_intrebari)
        else:
            return self._genereaza_din_problema(subiect, numar_intrebari)

    def _genereaza_din_curs(self, curs, numar):
        probleme = list(cursuri[curs].keys())
        print(f"Generez {numar} întrebări din: {curs}\n")
        print("-"*70 + "\n")
        rezultate = []
        for idx in range(numar):
            problema = random.choice(probleme)
            intrebare = self._genereaza_o_intrebare(problema)
            info = self._get_info_problema(problema)
            raspuns = None
            if self.genereaza_raspunsuri:
                raspuns = self.raspuns_gen.genereaza(intrebare, problema, info)

            print(f"Întrebarea {idx + 1}:\n{intrebare}")
            if self.genereaza_raspunsuri and raspuns is not None:
                print(f"Răspuns: {raspuns}\n")
            rezultate.append({
                "intrebare": intrebare,
                "problema": problema,
                "info": info,
                **({"raspuns": raspuns} if self.genereaza_raspunsuri else {}),
            })
        return rezultate

    def _genereaza_din_problema(self, problema, numar):
        print(f"Generez {numar} întrebări despre: {problema}\n")
        print("-"*70 + "\n")
        rezultate = []
        for idx in range(numar):
            intrebare = self._genereaza_o_intrebare(problema)
            info = self._get_info_problema(problema)
            raspuns = None
            if self.genereaza_raspunsuri:
                raspuns = self.raspuns_gen.genereaza(intrebare, problema, info)

            print(f"Întrebarea {idx + 1}:\n{intrebare}")
            if self.genereaza_raspunsuri and raspuns is not None:
                print(f"Răspuns: {raspuns}\n")
            rezultate.append({
                "intrebare": intrebare,
                "problema": problema,
                "info": info,
                **({"raspuns": raspuns} if self.genereaza_raspunsuri else {}),
            })
        return rezultate

    def _genereaza_o_intrebare(self, problema):
        info_problema = None
        curs_nume = None
        for nume_curs, curs in cursuri.items():
            if problema in curs:
                info_problema = curs[problema]
                curs_nume = nume_curs
                break

        # Alege șablon potrivit pentru tipul problemei
        is_game_theory = curs_nume == "C3: Game Theory"
        if is_game_theory:
            candidati = [s for s in sabloane_intrebari if ("Nash" in s or "MinMax" in s or "Alpha-Beta" in s) or ("strategie" in s or "complexitate" in s)]
        else:
            candidati = [s for s in sabloane_intrebari if ("Nash" not in s and "Alpha-Beta" not in s)]
        sablon = random.choice(candidati if candidati else sabloane_intrebari)
        strategii = ", ".join(info_problema["strategii"])
        strategie = random.choice(info_problema["strategii"])
        optimizari = ", ".join(info_problema["optimizari"]) if info_problema["optimizari"] else "N/A"

        intrebare = sablon.format(
            problema=problema.replace("_", " "),
            strategii=strategii,
            strategie=strategie,
            optimizari=optimizari
        )

        return intrebare

    def _get_info_problema(self, problema):
        for curs in cursuri.values():
            if problema in curs:
                return curs[problema]
        return None

    def _afiseaza_subiecte_disponibile(self):
        print("\nCursuri disponibile:\n")
        for curs, probleme_dict in cursuri.items():
            print(f"{curs}")
            for problema in probleme_dict.keys():
                print(f"   • {problema}")
        print()

# PROGRAM PRINCIPAL
if __name__ == "__main__":
    generator = GeneratorIntrebari()
    print("\nGenerator de întrebări")
    print("-"*70)
    print("Introduceți prompt-uri pentru a genera întrebări.")
    print("Exemple:")
    print("  • 'generează 3 întrebări despre n-queens'")
    print("  • 'vreau 5 intrebari din C2'")
    print("  • 'dă-mi 2 întrebări despre graph coloring'")
    print("  • 'quiz: 4 questions game theory'")
    print("  • 'exit' pentru a ieși\n")

    while True:
        prompt = input(" Prompt: ").strip()
        if prompt.lower() in ["exit", "quit", "iesire", "ieșire"]:
            break
        if not prompt:
            print("  Introduceți un prompt valid!\n")
            continue
        generator.genereaza_din_prompt(prompt)
        print()
