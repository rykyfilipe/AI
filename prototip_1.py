import random
import re

# BAZA DE CUNOȘTINȚE STRUCTURATĂ

cursuri = {
    "C1: Search Problems": {
        "n-queens": {
            "descriere": "Problema de a plasa N regine pe o tablă de șah",
            "strategii": ["backtracking", "local search", "constraint satisfaction"],
            "optimizari": ["MRV", "FC", "AC-3"]
        },
        "knight_tour": {
            "descriere": "Problema călărețului - parcurgerea tuturor pătratelor unei table",
            "strategii": ["backtracking", "heuristic search", "depth first search"],
            "optimizari": ["Warnsdorff heuristic", "pruning"]
        },
        "hanoi": {
            "descriere": "Problema Turnurilor din Hanoi",
            "strategii": ["recursion", "dynamic programming", "iterative"],
            "optimizari": ["memoization"]
        }
    },
    "C2: Constraint Satisfaction": {
        "graph_coloring": {
            "descriere": "Colorarea unui graf cu numărul minim de culori",
            "strategii": ["backtracking", "constraint satisfaction", "greedy"],
            "optimizari": ["AC-3", "MRV", "FC"]
        },
        "sudoku": {
            "descriere": "Problema de completare a unui puzzle sudoku",
            "strategii": ["backtracking", "constraint propagation", "AC-3"],
            "optimizari": ["AC-3", "MRV", "forward checking"]
        }
    },
    "C3: Game Theory": {
        "nash_equilibrium": {
            "descriere": "Echilibrul Nash într-un joc în formă normală",
            "strategii": ["dominance elimination", "best response", "mixed strategy"],
            "optimizari": []
        },
        "minmax_alphabeta": {
            "descriere": "Strategia MinMax cu optimizarea Alpha-Beta",
            "strategii": ["minimax", "alpha-beta pruning", "iterative deepening"],
            "optimizari": ["alpha-beta pruning", "transposition tables"]
        }
    }
}

# Dicționar de sinonime pentru căutare
sinonime = {
    "n-queens": ["n-queens", "nqueens", "regine", "8 regine"],
    "knight_tour": ["knight tour", "knight's tour", "cavaler", "calaret"],
    "hanoi": ["hanoi", "turnuri"],
    "graph_coloring": ["graph coloring", "colorare graf", "coloring"],
    "sudoku": ["sudoku"],
    "nash_equilibrium": ["nash", "equilibrium", "echilibru"],
    "minmax_alphabeta": ["minmax", "alpha-beta", "alphabeta", "game tree"],
    "C1: Search Problems": ["c1", "search", "problems"],
    "C2: Constraint Satisfaction": ["c2", "constraint", "satisfaction", "csp"],
    "C3: Game Theory": ["c3", "game theory", "game"]
}

#  ȘABLOANE DE ÎNTREBĂRI

sabloane_intrebari = [
    "Pentru problema {problema}, care este cea mai potrivită strategie dintre următoarele: {strategii}?",
    "Explicați de ce {strategie} este cea mai bună alegere pentru {problema}.",
    "Pentru {problema} rezolvată cu {strategie}, ce optimizare este cea mai eficientă: {optimizari}?",
    "Care sunt avantajele și dezavantajele utilizării {strategie} pentru {problema}?",
    "Pentru jocul dat în forma normală, există echilibru Nash pur?",
    "Pentru arborele dat, care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate cu MinMax + Alpha-Beta?",
    "Cum diferă {strategie} de alte strategii în rezolvarea {problema}?",
    "Ce complexitate în timp și spațiu are {strategie} pentru {problema}?"
]

# EXTRACTOR DE PARAMETRI

class ExtractorParametri:
    @staticmethod
    def extrage_numar_intrebari(prompt):
        """Extrage numărul de întrebări din prompt"""
        # Cautam pattern-uri: "2 întrebări", "3 questions", "vreau 5", etc.
        match = re.search(r'(\d+)\s*(întrebări|intrebari|questions|întrebare|intrebare|q|questions)', prompt, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Dacă nu găsim, default e 1
        return 1
    
    @staticmethod
    def extrage_subiect(prompt):
        """Extrage subiectul/cursul/capitolul din prompt"""
        # Normalizează: lowercase, elimină accente și spații extra
        prompt_norm = prompt.lower().replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")
        prompt_norm = re.sub(r'\s+', ' ', prompt_norm)  # elimină spații multiple
        
        # Cauta în dicționarul de sinonime
        for topic, synonyms in sinonime.items():
            for syn in synonyms:
                if syn in prompt_norm:
                    return topic
        
        return None
    
    @staticmethod
    def get_toate_problemele():
        """Returnează toate problemele disponibile"""
        probleme = []
        for curs in cursuri.values():
            probleme.extend(list(curs.keys()))
        return probleme
    
    @staticmethod
    def get_probleme_din_curs(curs):
        """Returnează problemele din cursul specificat"""
        if curs in cursuri:
            return list(cursuri[curs].keys())
        return []

# GENERATOR DE ÎNTREBĂRI

class GeneratorIntrebari:
    def __init__(self):
        self.extractor = ExtractorParametri()
    
    def genereaza_din_prompt(self, prompt):
        """
        Primește prompt-ul utilizatorului și generează DOAR întrebări
        """
        print(f"\n Prompt-ul tău: '{prompt}'\n")
        
        # Extragem parametrii
        numar_intrebari = self.extractor.extrage_numar_intrebari(prompt)
        subiect = self.extractor.extrage_subiect(prompt)
        
        # Dacă nu găsim subiect, informăm utilizatorul
        if subiect is None:
            print("Nu am putut identifica subiectul din prompt.")
            print("\n SUBIECTELE DISPONIBILE:")
            self._afiseaza_subiecte_disponibile()
            return
        
        # Determinam tipul subiectului (curs sau problemă)
        if subiect in cursuri:
            # E un curs întreg
            self._genereaza_din_curs(subiect, numar_intrebari)
        else:
            # E o problemă specifică
            self._genereaza_din_problema(subiect, numar_intrebari)
    
    def _genereaza_din_curs(self, curs, numar):
        """Generează întrebări din toate problemele unui curs"""
        probleme = self.extractor.get_probleme_din_curs(curs)
        
        if not probleme:
            print(f" Cursul '{curs}' nu are probleme.")
            return
        
        # Selectam probleme random
        probleme_selectate = random.choices(probleme, k=min(numar, len(probleme) * 3))
        
        print(f" Generos {numar} întrebări din: {curs}\n")
        print("="*70 + "\n")
        
        for idx in range(numar):
            problema = random.choice(probleme)
            intrebare = self._genereaza_o_intrebare(problema)
            print(f"❓ Întrebarea {idx + 1}:\n{intrebare}\n")
    
    def _genereaza_din_problema(self, problema, numar):
        """Generează întrebări pentru o problemă specifică"""
        # Găsim cursul care conține această problemă
        curs_gasit = None
        for curs, probleme_dict in cursuri.items():
            if problema in probleme_dict:
                curs_gasit = curs
                break
        
        if not curs_gasit:
            print(f"Problema '{problema}' nu a fost găsită.")
            self._afiseaza_subiecte_disponibile()
            return
        
        print(f" Generos {numar} întrebări despre: {problema} (din {curs_gasit})\n")
        print("="*70 + "\n")
        
        for idx in range(numar):
            intrebare = self._genereaza_o_intrebare(problema)
            print(f" Întrebarea {idx + 1}:\n{intrebare}\n")
    
    def _genereaza_o_intrebare(self, problema):
        """Generează o singură întrebare pentru o problemă"""
        # Găsim informațiile problemei
        info_problema = None
        for curs in cursuri.values():
            if problema in curs:
                info_problema = curs[problema]
                break
        
        if not info_problema:
            return "Eroare: nu s-a găsit problema."
        
        # Selectam un șablon random
        sablon = random.choice(sabloane_intrebari)
        
        # Completam șablonul cu date reale
        strategii = ", ".join(info_problema["strategii"])
        strategie = random.choice(info_problema["strategii"])
        
        if info_problema["optimizari"]:
            optimizari = ", ".join(info_problema["optimizari"])
        else:
            optimizari = "N/A"
        
        # Formatam întrebarea
        intrebare = sablon.format(
            problema=problema.replace("_", " "),
            strategii=strategii,
            strategie=strategie,
            optimizari=optimizari
        )
        
        return intrebare
    
    def _afiseaza_subiecte_disponibile(self):
        """Afișează toate subiectele și problemele disponibile"""
        print("\n CURSURI DISPONIBILE:\n")
        for curs, probleme_dict in cursuri.items():
            print(f"🎓 {curs}")
            for problema in probleme_dict.keys():
                print(f"   • {problema}")
        print()

# PROGRAM PRINCIPAL

if __name__ == "__main__":
    generator = GeneratorIntrebari()
    
    print("\n" + "="*70)
    print("🎓 GENERATOR DE ÎNTREBĂRI - SMARTEST")
    print("="*70)
    print("\nIntroduceți prompt-uri pentru a genera întrebări.")
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