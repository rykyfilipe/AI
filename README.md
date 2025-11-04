Lista participanti :

- Bondor Ricardo-Filipe
- Ozarchevici Eduardo-Iosua
- Gontineac Mario
- Nita Alexandru

## Sistem Q&A pentru AI – Generator + Verificare (răspuns de la utilizator)

Acest proiect include:

- generator de întrebări (bazat pe o bază de cunoștințe);
- (opțional) generator de răspunsuri simple, bazate pe reguli – util pentru demo în `prototip_1.py`;
- verificator care evaluează răspunsul (scor + feedback) față de cunoștințe.

Integrarea completă se face prin scriptul `main.py` care rulează pipeline-ul: Generare întrebări → Răspuns scris de utilizator → Verificare (scor + feedback).

### Cum rulezi

1. Asigură-te că ești în folderul proiectului.
2. Rulează pipeline-ul interactiv:

```bash
python3 main.py
```

3. Introdu un prompt. Exemple:
   - `generează 3 întrebări despre n-queens`
   - `vreau 5 intrebari din C2`
   - `dă-mi 2 întrebări despre graph coloring`
   - `quiz: 4 questions game theory`

Pentru ieșire tastează `exit` sau `quit`.

### Structura componentelor

- `knowledge.py` – sursa unică pentru cunoștințe (`cursuri`), sinonime și șabloane de întrebări.
- `prototip_1.py` – conține `GeneratorIntrebari` și poate rula standalone; returnează structurat rezultatele (întrebare, problemă, info) și poate (opțional) genera răspunsuri automate pentru demo.
- `generator_raspunsuri.py` – conține `GeneratorRaspunsuri` (răspunsuri simple, bazate pe reguli și cuvinte-cheie) – folosit doar în modul demo.
- `verificare_raspunsuri.py` – conține `EvaluatorRaspunsuri` (scor + feedback) și un mic demo când este rulat direct.
- `main.py` – orchestrator: generează întrebări, cere răspunsul utilizatorului și afișează scorul/feedback-ul pentru fiecare întrebare.

Nu sunt necesare dependențe externe (funcționează cu Python 3 standard).
