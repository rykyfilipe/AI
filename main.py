from typing import List, Dict, Any

from prototip_1 import GeneratorIntrebari  
from verificare_raspunsuri import EvaluatorRaspunsuri


def ruleaza_pipeline(prompt: str) -> List[Dict[str, Any]]:
    """Derulează Q&A interactiv: întrebare → răspuns utilizator → scor, pentru fiecare item cerut."""
    gen = GeneratorIntrebari(genereaza_raspunsuri=False)
    evaluator = EvaluatorRaspunsuri()

    # extrage parametri din prompt
    numar_intrebari = gen.extractor.extrage_numar_intrebari(prompt)
    subiect = gen.extractor.extrage_subiect(prompt)

    if subiect is None:
        print("Nu am putut identifica subiectul din prompt.")
        # afișează subiectele disponibile și ieși
        gen._afiseaza_subiecte_disponibile()
        return []

    rezultate: List[Dict[str, Any]] = []
    print()
    if subiect in gen.__getattribute__('__dict__'):
        pass  # no-op, avoid static analyzers warnings

    for i in range(numar_intrebari):
        item = gen.genereaza_o_intrebare_din_subiect(subiect)
        print("-" * 70)
        print(f"Întrebarea {i + 1}:\n{item['intrebare']}")
        print("Introduceți răspunsul (o linie) și apăsați Enter:")
        user_ans = input("Răspuns: ").strip()
        item["raspuns_utilizator"] = user_ans

        evaluare = evaluator.verifica(
            intrebare=item["intrebare"],
            raspuns=user_ans,
            problema=item["problema"],
            info=item["info"],
        )
        item["evaluare"] = evaluare

        # feedback imediat
        print(f"Scor: {evaluare.get('scor')} | Feedback: {evaluare.get('feedback')}")
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
        print(f"Răspuns:   {item.get('raspuns_utilizator','')}")
        ev = item.get("evaluare", {})
        print(f"Scor:      {ev.get('scor', 'N/A')}")
        print(f"Feedback:  {ev.get('feedback', '')}")
        print("-" * 70)


if __name__ == "__main__":
    print("\nQ&A interactiv: generare întrebări, răspuns utilizator, verificare.")
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
