# EXPLICAȚIE DETALIATĂ - v2.py

## STRUCTURA GENERALĂ

Codul este împărțit în **5 secțiuni principale**:

```
1. KNOWLEDGE BASE - Stocarea problemelor și strategiilor
2. DOMAIN LOGIC - GameEngine pentru calcule matematice
3. QUESTION GENERATOR ENGINE - ContentGenerator pentru generare întrebări
4. EVALUATOR - Evaluarea răspunsurilor utilizatorilor
5. MAIN PIPELINE - Interfață utilizator și flux principal
```

---

## SECȚIUNEA 1: KNOWLEDGE BASE

### Ce face:
Stochează **6 probleme AI** organizate în **3 cursuri** cu:
- Descriere
- Strategii disponibile
- Optimizări posibile
- Tip problemă (pentru dispatcher)

### Structură:

```python
KNOWLEDGE_BASE = {
    "C1: Search Problems": {
        "n-queens": {
            "description": "...",
            "strategies": ["backtracking", "local search", "genetic algorithms"],
            "optimizations": ["MRV", "Forward Checking"],
            "type": "search_strategy"  # ← Tip pentru factory method
        },
        ...
    },
    "C2: Constraint Satisfaction": { ... },
    "C3: Game Theory": { ... }
}
```

### SYNONYMS (dict):
- Mapează cuvinte cheie la ID-uri de probleme
- Ex: "regine" → "n-queens", "hanoi" → "hanoi"
- Folosit pentru a recunoaște ce problemă cere utilizatorul

---

## SECȚIUNEA 2: DOMAIN LOGIC

### Clasa Node:
```python
class Node:
    def __init__(self, value=None, children=None):
        self.value = value          # Valoarea nodului (pentru frunze)
        self.children = children     # Lista de copii
    
    def is_leaf(self):
        return len(self.children) == 0
```

**Folosit pentru:** Reprezentare arbore de joc (MinMax)

---

### Clasa GameEngine:
Conține metodele matematice pentru **rezolvare probleme**.

#### 1. `generate_random_tree(depth, branching_factor)`
**Ce face:** Generează arbore random de joc

```
Exemplu cu depth=2, branching=2:

        MAX
       /   \
     MIN   MIN
    / \    / \
   (5)(3) (8)(2)

Adâncime 0 → Frunze cu valori random
Adâncime 1 → Noduri MIN/MAX
```

**Algoritm:**
- depth=0 → Returnează frunză cu valoare random
- depth>0 → Crează nod, adaugă recursive branching_factor copii

---

#### 2. `tree_to_ascii(node, ...)`
**Ce face:** Convertește arbore în reprezentare text frumoasă

```
Exemplu output:
├── MAX
│   ├── MIN
│   │   ├── (5)
│   │   └── (3)
│   └── MIN
│       ├── (8)
│       └── (2)
```

---

#### 3. `solve_alpha_beta(root_node)`
**Ce face:** Aplică algoritm **Alpha-Beta Pruning** pe arbore

**Alpha-Beta Pruning:**
- Minimizează noduri vizitate în minimax
- Taie ramuri care nu afectează rezultatul final
- Returnează: (valoare_rădăcină, număr_frunze_vizitate)

**Exemplu:**
```
Fără pruning: Vizitează 8 frunze
Cu Alpha-Beta: Vizitează 4 frunze (50% mai rapid!)
```

---

#### 4. `generate_nash_matrix(rows, cols)`
**Ce face:** Generează matrice de plăți pentru jocuri cu 2 jucători

```
Exemplu 2x2:
[[(5, 3), (2, 7)],
 [(6, 1), (4, 4)]]

(5,3) = (Plată J1, Plată J2)
```

---

#### 5. `solve_nash(matrix)`
**Ce face:** Găsește **echilibrele Nash pure**

**Echilibru Nash:** Stare unde niciun jucător nu câștigă schimbând strategie

**Algoritm:**
1. Pentru fiecare coloană → Găsește rândul cu max plată pentru J1
2. Pentru fiecare rând → Găsește coloana cu max plată pentru J2
3. Intersecție = Echilibru Nash

---

## SECȚIUNEA 3: QUESTION GENERATOR ENGINE

### Clasa QuestionBundle:
```python
class QuestionBundle:
    def __init__(self, question_text, correct_answer_text, topic_info):
        self.question_text = question_text           # Întrebarea
        self.correct_answer_text = correct_answer_text  # Răspuns corect
        self.topic_info = topic_info                 # Metadata (tip, instanță, etc)
```

**Scop:** Pachet complet cu întrebare + răspuns + info

---

### Clasa ContentGenerator:

#### `create_question(topic_key, topic_data)` - FACTORY METHOD
**Ce face:** Dirijează generarea pe baza **tipului problemei**

```python
if topic_data.get("type") == "tree_game":
    return self._create_minimax_bundle(topic_data)
elif topic_data.get("type") == "matrix_game":
    return self._create_nash_bundle(topic_data)
elif topic_data.get("type") in ["csp", "search_strategy"]:
    return self._create_strategy_bundle(topic_key, topic_data)
else:
    return self._create_theory_bundle(topic_key, topic_data)
```

---

#### `_create_minimax_bundle()` - MinMax cu Alpha-Beta

**Algoritm:**
1. Generează arbore random (depth=2-3, branching=2)
2. Rezolvă cu Alpha-Beta → obține (valoare, frunze_vizitate)
3. Formatează întrebare + răspuns

**Exemplu:**
```
[Întrebare]
Se dă arbore:
  MAX
 /   \
MIN  MIN
/\  /\
5 3 8 2

1. Care este valoarea rădăcinii cu MinMax?
2. Câte frunze sunt vizitate cu Alpha-Beta?

[Răspuns generat]
Valoarea = 5. Frunze vizitate = 4.
```

---

#### `_create_nash_bundle()` - Echilibru Nash

**Algoritm:**
1. Generează matrice 2x2 random
2. Rezolvă cu algoritm Nash → obține equilibria
3. Formatează întrebare + răspuns

**Exemplu:**
```
[Întrebare]
Matrice:
[[(5, 3), (2, 7)],
 [(6, 1), (4, 4)]]

Găsește echilibrele Nash pure.

[Răspuns generat]
Echilibru: (Row 0, Col 1) → Payoffs (2, 7)
```

---

#### `_create_strategy_bundle()` - Alegere Strategie Individual

**Ce face:** Generează întrebare de **alegere strategie** pentru o problemă specifică

**Sub-metode (una per problemă):**

##### `_create_nqueens_strategy()`
```
Generează: N random (4-6)
Instanță: N=5, 3 regine deja plasate
Opțiuni: A) Backtracking, B) Local Search, C) Genetic
Răspuns: A cu motivare
```

##### `_create_knight_tour_strategy()`
```
Generează: Tablă NxN (6-8)
Instanță: 6x6, pornire colț stânga-sus
Opțiuni: A) Backtracking pur, B) Warnsdorff, C) Forward Checking
Răspuns: B cu motivare
```

##### `_create_graph_coloring_strategy()`
```
Generează: Nr noduri (5-8), densitate (rară/medie/densă)
Instanță: 7 noduri, conexiuni dense
Opțiuni: A) AC-3, B) Greedy, C) Backtracking
Răspuns: A cu motivare
```

##### `_create_hanoi_strategy()`
```
Generează: Nr discuri (4-6)
Instanță: 5 discuri, timp <1ms
Opțiuni: A) Recursion, B) Memoization, C) Iterativ
Răspuns: C cu motivare
```

---

#### `generate_problem_selection_question()` - ALEGERE DIN 4+ PROBLEME

**CÂT E NOU ÎN CODUL ADĂUGAT:**

**Ce face:**
1. Selectează **aleatoriu 1 problemă din 4:** N-Queens, Knight's Tour, Graph Coloring, Hanoi
2. Generează **instanță specifică** pentru problema selectată
3. Formatează întrebarea cu 3 opțiuni strategii
4. Returnează bundle **FĂRĂ răspuns pre-calculat** (correct_answer_text = None)

**Algoritm:**
```python
problems = {
    "n-queens": {
        "name": "N-Queens",
        "instance_generator": lambda: {"n": random.randint(4, 6), "conflicts": random.randint(1, 3)},
        "strategies": [3 opțiuni]
    },
    ... (Knight's Tour, Graph Coloring, Hanoi)
}

# Selectează random
problem_key = random.choice(list(problems.keys()))
problem = problems[problem_key]

# Generează instanță
instance = problem["instance_generator"]()

# Formatează întrebare
question = _format_problem_selection_question(problem_key, problem, instance)

# Returnează bundle
return QuestionBundle(
    question_text=question,
    correct_answer_text=None,  # IMPORTANT: Nu e răspuns pre-calculat!
    topic_info={
        "type": "problem_selection",
        "problem": problem_key,
        "instance": instance,
        "strategies": problem["strategies"]
    }
)
```

**Exemplu output:**
```
PROBLEMA: N-Queens
Descriere: Problema de a plasa N regine pe o tablă de șah

INSTANȚĂ: N = 5, cu 2 regine deja plasate care creează conflicte.

ÎNTREBARE: Care este cea mai potrivită strategie?
A) Backtracking cu Forward Checking
B) Local Search (Min-Conflicts)
C) Genetic Algorithms

Justifică alegerea considerând complexitatea și eficiență.
```

---

## SECȚIUNEA 4: EVALUATOR

### `normalize(text)`
```python
def normalize(text):
    return text.lower().replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")
```
**Ce face:** Normalizează textul (elimină diacritice pentru comparare)

---

### `cosine_similarity(s1, s2)` - COMPARAȚIE SEMANTICĂ
```
Calcul: 
sim(s1, s2) = (cuvinte comune) / (sqrt(cuvinte_s1) * sqrt(cuvinte_s2))

Exemplu:
s1 = "Backtracking cu forward checking"
s2 = "Backtracking si forward checking"
Similarity ≈ 0.9 (90%)
```

**Rezultat: scor 0-1 (0=diferit, 1=identic)**

---

### `evaluate(user_answer, system_bundle)` - EVALUARE FINALĂ
**Ce face:** Compară răspuns utilizator cu răspuns corect

**Logică:**

#### 1. **Pentru probleme cu numere (MinMax):**
```
Extrage numere din răspuns
Verifică dacă numerele corecte sunt prezente
Score = 100 dacă corect, 0 dacă nu
```

Exemplu:
```
Correct: "Valoarea = 5. Frunze = 4."
User: "Raspunsul este 5 si 4"
→ Extrage [5, 4] din ambele
→ Score = 100
```

---

#### 2. **Pentru echilibru Nash (coordonate):**
```
Extrage coordonate (Row X, Col Y) din răspuns corect
Extrage coordonate din răspuns utilizator (flexibil: "Row X Col Y", "(X, Y)", etc)
Compară - credit parțial pentru unele equilibria
```

Exemplu:
```
Correct: "(Row 0, Col 1) → Payoffs (2, 7); (Row 1, Col 1) → Payoffs (4, 4)"
User: "0,1 si 1,1"
→ Găsește 2/2 coordonate corecte
→ Score = 100
```

---

#### 3. **Pentru strategii (răspunsuri deschise):**
```
Calcul similaritate semantică între răspuns user și răspuns corect
Score = int(similarity * 100)
```

---

## SECȚIUNEA 5: MAIN PIPELINE

### Funcția `get_topic_from_prompt(prompt)`:
**Ce face:** Identifică ce problemă cere utilizatorul din text

```python
def get_topic_from_prompt(prompt):
    p_norm = prompt.lower()
    
    # Verifică cursuri
    if "c1" in p_norm or "search" in p_norm:
        return random_topic_from_C1
    elif "c2" in p_norm or "csp" in p_norm:
        return random_topic_from_C2
    elif "c3" in p_norm or "game" in p_norm:
        return random_topic_from_C3
    
    # Verifică sinonime
    for topic_key, synonyms in SYNONYMS.items():
        if any(s in p_norm for s in synonyms):
            return get_from_KB(topic_key)
    
    # Default
    return "minmax_alphabeta"
```

**Exemplu:**
- Input: "genereaza minmax"
- Output: ("minmax_alphabeta", {descr, strategies, ...})

---

### Funcția `main()` - FLUX PRINCIPAL

```python
def main():
    generator = ContentGenerator()
    evaluator = Evaluator()
    
    while True:
        prompt = input("\nUser Input > ")
        
        if "selectie problema" in prompt:
            # RUTA NOĂ: Alegere din 4+ probleme
            bundle = generator.generate_problem_selection_question()
            print(bundle.question_text)
            user_ans = input("[Your Answer]: ")
            # Nu se evaluează automat (correct_answer = None)
        else:
            # RUTA VECHE: Intrebare specifică cu răspuns pre-calculat
            topic_key, topic_data = get_topic_from_prompt(prompt)
            bundle = generator.create_question(topic_key, topic_data)
            print(bundle.question_text)
            user_ans = input("[Your Answer]: ")
            result = evaluator.evaluate(user_ans, bundle)
            print(f"Scor: {result['score']}")
            print(f"Feedback: {result['feedback']}")
            print(f"Răspunsul corect: {result['correct_answer']}")
```

---

## FLUXUL COMPLET - EXEMPLU PRACTIC

### Scenariul 1: Utilizator cere MinMax
```
USER: "genereaza minmax"

1. main() apelează get_topic_from_prompt()
   → Returnează ("minmax_alphabeta", {...})

2. main() apelează generator.create_question()
   → Dirijează la _create_minimax_bundle()

3. _create_minimax_bundle():
   - Generează arbore random (depth=2, branching=2)
   - Apelează engine.solve_alpha_beta(tree)
     → Execută MinMax cu Alpha-Beta
     → Returnează (root_value=7, visited_leaves=4)
   - Formatează întrebare + răspuns
   - Returnează QuestionBundle

4. main() afișează întrebarea

5. USER: "Valoarea = 7, frunze = 4"

6. main() apelează evaluator.evaluate()
   - Extrage numere [7, 4] din ambele
   - Compară → Match!
   - Returnează score=100

7. Afișează: "Scor: 100, Feedback: Corect!"
```

---

### Scenariul 2: Utilizator cere SelectieProblema (NOU)
```
USER: "selectie problema"

1. main() detectează "selectie problema"
   → Apelează generator.generate_problem_selection_question()

2. generate_problem_selection_question():
   - Selectează random: "graph_coloring"
   - Generează instanță: {num_nodes: 6, density: "medie"}
   - Apelează _format_problem_selection_question()
     → Formatează întrebare cu 3 opțiuni A/B/C
   - Returnează QuestionBundle(
       question_text="PROBLEMA: Graph Coloring...",
       correct_answer_text=None,  # ← IMPORTANT!
       topic_info={problem: "graph_coloring", instance: {...}, ...}
     )

3. main() afișează întrebarea

4. USER: "A) AC-3 deoarece aceasta metoda propaga constrangeri..."

5. main() afișează:
   "Răspunsul tău: [text utilizator]
    Problem ID: graph_coloring
    Instance: {num_nodes: 6, density: 'medie'}
    Strategii disponibile: [AC-3, Greedy, Backtracking]
    (Nu se evaluează automat - este deschisă pentru evaluare manuală)"
```

---

## REZUMAT FLUX COMPLET

```
┌─────────────────────────────┐
│   USER INPUT PROMPT         │
└──────────────┬──────────────┘
               │
               ├─ "selectie problema"?
               │   └─→ generate_problem_selection_question()
               │       ├─ Selectează problem din 4
               │       ├─ Generează instanță
               │       └─ Returnează QuestionBundle (NO ANSWER)
               │
               └─ Alt prompt?
                   └─→ get_topic_from_prompt()
                       ├─ Identifică problemă
                       └─→ create_question(topic_key, topic_data)
                           ├─ Dirijează pe tip (tree/matrix/strategy/theory)
                           ├─ Rezolvă cu GameEngine
                           └─ Returnează QuestionBundle (WITH ANSWER)

                       → evaluator.evaluate()
                           ├─ Compară răspuns
                           ├─ Calculează score
                           └─ Returnează feedback
```

---

## DIFERENȚA CHEIE ÎNTRE CEI 2 TIPURI DE ÎNTREBĂRI

| Aspect | Intrebari clasice | Selectie problema (NOU) |
|--------|------------------|------------------------|
| **Răspuns pre-calculat** | DA (auto-generat) | NU (None) |
| **Evaluare automată** | DA (scor + feedback) | NU (manual) |
| **Complexitate răspuns** | Simplu (cifre/text scurt) | Complex (justificare) |
| **Nr probleme** | 1 specifică | 4+ aleatoriu |
| **Instanță** | Generat din metode specifice | Parametri random |
| **Opțiuni** | Depinde de tip | Întotdeauna A/B/C |

---

Sper că e clar acum! Întreabă orice nu-ți e clar! 🎯
