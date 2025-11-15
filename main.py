from typing import List, Dict, Any
import re

from generator_intrebari import GeneratorIntrebari  
from verificare_raspunsuri import EvaluatorRaspunsuri
from generator_raspunsuri import GeneratorRaspunsuri
from knowledge import cursuri, sinonime


def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")
    )


def _extrage_numar_intrebari(prompt: str) -> int:
    m = re.search(r"(\d+)\s*(întrebări|intrebari|questions|întrebare|intrebare|q|questions)", prompt, re.IGNORECASE)
    return int(m.group(1)) if m else 1


def _extrage_subiect(prompt: str):
    p = re.sub(r"\s+", " ", _normalize(prompt))
    for topic, syns in sinonime.items():
        for s in syns:
            if s in p:
                return topic
    return None


def _afiseaza_subiecte_disponibile():
    print("\nCursuri disponibile:\n")
    for curs, probleme in cursuri.items():
        print(curs)
        for problema in probleme.keys():
            print(f"   • {problema}")
    print()


def ruleaza_pipeline(prompt: str) -> List[Dict[str, Any]]:
    """Derulează Q&A: pentru fiecare întrebare generată, preia răspunsul utilizatorului,
    generează și un răspuns automat, apoi le evaluează pe ambele cu aceeași metodă."""
    gen = GeneratorIntrebari()
    evaluator = EvaluatorRaspunsuri()
    rasp_gen = GeneratorRaspunsuri()

    # extrage parametri din prompt
    numar_intrebari = _extrage_numar_intrebari(prompt)
    subiect = _extrage_subiect(prompt)
    print(f"Subiect: {subiect}")

    if subiect is None:
        print("Nu am putut identifica subiectul din prompt.")
        _afiseaza_subiecte_disponibile()
        return []

    rezultate: List[Dict[str, Any]] = []

    for i in range(numar_intrebari):
        item = gen.genereaza_o_intrebare_din_subiect(subiect)
        print("-" * 70)
        print(f"Întrebarea {i + 1}:\n{item['intrebare']}")

        #  Generează răspuns automat pentru întrebare și îl afișează
        auto_ans = rasp_gen.genereaza(item["intrebare"], item["problema"], item["info"])
        item["raspuns_generat"] = auto_ans
        print(f"Răspuns generat:  {auto_ans}")

        # Cere răspunsul utilizatorului
        print("Introduceți răspunsul (o linie) și apăsați Enter:")
        user_ans = input("Răspuns: ").strip()
        item["raspuns_utilizator"] = user_ans

        # Evaluează ambele răspunsuri cu aceeași metodă (inclusiv similaritatea cosine)
        comparatie = evaluator.compara(
            intrebare=item["intrebare"],
            raspuns_utilizator=user_ans,
            raspuns_generat=auto_ans,
            problema=item["problema"],
            info=item["info"],
        )
        item["evaluare"] = comparatie
        # Feedback imediat: scor pe bază de similaritate cosine
        print(f"Răspuns utilizator: {user_ans}")
        print(f"Scor (cosine): {comparatie.get('scor_cosine', 0)}  | Similaritate: {comparatie.get('similaritate', 0):.2f}")
        rezultate.append(item)

    return rezultate


def afiseaza_rezultate(rezultate: List[Dict[str, Any]]):
    if not rezultate:
        return
    print("\nRezultatele verificării:")
    print("-" * 70)
    for i, item in enumerate(rezultate, 1):
        print(f"#{i}")
        print(f"Întrebare: {item['intrebare']}")
        # Afișează ambele răspunsuri și scorul pe bază de cosine
        print(f"Răspuns utilizator: {item.get('raspuns_utilizator','')}")
        print(f"Răspuns generat:  {item.get('raspuns_generat','')}")
        ev = item.get("evaluare", {})
        print(f"Scor (cosine): {ev.get('scor_cosine','N/A')}  | Similaritate: {ev.get('similaritate',0):.2f}")
        print("-" * 70)


if __name__ == "__main__":
    print("\nQ&A interactiv: generare întrebări, răspuns generat, verificare.")
    print("-" * 70)
    print("Introduceți un prompt pentru a începe.")
    print("Exemple:")
    print("  • 'generează 3 întrebări despre n-queens'")
    print("  • 'vreau 5 intrebari din C2'")
    print("  • 'dă-mi 2 întrebări despre graph coloring'")
    print("  • 'quiz: 4 questions game theory'")
    print("  • 'exit' pentru a ieși\n")

    while True:
        try:
            prompt = input(" Prompt: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if prompt.lower() in ["exit", "quit", "iesire", "ieșire"]:
            break
        if not prompt:
            print("  Introduceți un prompt valid!\n")
            continue

        rez = ruleaza_pipeline(prompt)
        afiseaza_rezultate(rez)
        print()
