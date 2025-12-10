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

Există și un mod opțional de demo, `--auto`, care generează răspunsuri automat (bazate pe reguli simple) doar pentru a demonstra fluxul cap-coadă. Acest mod nu este destinat evaluării finale, unde răspunsul e introdus de utilizator.

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

Mod auto (demo):

```bash
python3 main.py --auto
```

Scrie apoi un prompt (ex. „genereaza 3 intrebari despre C3”) și tastează `exit` pentru a închide.

### Structura componentelor

- `knowledge.py` – sursa unică pentru cunoștințe (`cursuri`), sinonime și șabloane de întrebări.
- `prototip_1.py` – conține `GeneratorIntrebari` și poate rula standalone; returnează structurat rezultatele (întrebare, problemă, info) și poate (opțional) genera răspunsuri automate pentru demo.
- `generator_raspunsuri.py` – conține `GeneratorRaspunsuri` (răspunsuri simple, bazate pe reguli și cuvinte-cheie) – folosit doar în modul demo.
- `verificare_raspunsuri.py` – conține `EvaluatorRaspunsuri` (scor + feedback) și un mic demo când este rulat direct.
- `main.py` – orchestrator: generează întrebări, cere răspunsul utilizatorului și afișează scorul/feedback-ul pentru fiecare întrebare.

Nu sunt necesare dependențe externe (funcționează cu Python 3 standard).

### Tipuri de întrebări acoperite (cerința evaluării)

Sistemul acoperă explicit cele 4 tipuri de întrebări menționate:

1. Pentru o problemă identificată dintr-o listă de minim 4 (n-queens, generalised Hanoi, graph coloring, knight’s tour) și o instanță/sau set de instanțe: care este cea mai potrivită strategie, dintre cele menționate la curs? – acoperit prin șabloanele de strategie și verificarea pe cuvinte-cheie.
2. Pentru jocul dat în formă normală (matrice): există echilibru Nash pur? Care este acesta? – șablon dedicat pentru Game Theory; verificarea validează conceptele de bază (răspunsul exact pe o matrice reală ar necesita parsare și calcul suplimentar).
3. CSP: care va fi asignarea variabilelor rămase, date variabilele, domeniile, constrângerile și o asignare parțială, folosind Backtracking cu optimizare (FC, MRV sau AC-3)? – șablon dedicat, iar evaluatorul punctează menționarea strategiei și a optimizărilor (FC/MRV/AC-3). Răspunsul exact depinde de instanță; sistemul e pregătit să evalueze răspunsul introdus de utilizator.
4. Pentru arborele dat: care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate aplicând MinMax cu Alpha-Beta? – șablon dedicat pentru Game Theory; verificarea validează conceptele de bază.

Observație: pentru calcule exacte pe o instanță concretă (matrice de payoff sau arbore de joc), ar fi nevoie de parsare de input și algoritmi dedicați (best response, detecție Nash, minimax cu α-β). Actualul sistem oferă generare + verificare conceptuală și poate fi extins ușor cu astfel de algoritmi dacă se dorește.

### Livrabil 2 – criteriu minim

„Soluții implementate (generare întrebare și verificare răspuns) pentru una din cele 4 tipuri de întrebări.” – acest proiect îndeplinește cerința (și, de fapt, acoperă toate cele patru tipuri). Dacă vrei să demonstrezi strict un singur tip, recomandăm varianta CSP (asignare cu Backtracking + FC/MRV/AC-3):

```bash
python3 main.py
# apoi: genereaza 1 intrebare despre graph coloring
```

Introdu un răspuns care menționează Backtracking și o optimizare (ex. MRV/FC/AC-3) și vei primi scor + feedback.
