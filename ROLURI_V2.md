# 📚 v2.py - Structură și Roluri Detaliate

## 🎯 Arhitectura Generală

```
┌─────────────────────────────────────────────────────────────┐
│  1. KNOWLEDGE BASE (Date statice)                           │
│     ├─ KNOWLEDGE_BASE (4 cursuri cu 8 probleme)            │
│     └─ SYNONYMS (mapare sinonime pentru căutare)           │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  2. DOMAIN LOGIC (Calcule matematice)                       │
│     ├─ Node (reprezentare arbore de joc)                   │
│     └─ GameEngine (Nash, MinMax, Alpha-Beta)               │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  3. QUESTION GENERATOR (Creare probleme)                    │
│     ├─ QuestionBundle (container pentru întrebare+răspuns)  │
│     └─ ContentGenerator (factory pentru 4 tipuri)           │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  4. EVALUATOR (Notare răspunsuri)                          │
│     └─ Evaluator (similaritate + logică specială)           │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  5. MAIN PIPELINE                                           │
│     ├─ get_topic_from_prompt() (identificare curs/problemă) │
│     └─ main() (REPL interactiv)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ KNOWLEDGE BASE

### `KNOWLEDGE_BASE` (Dict Static)
**Scopul**: Stochează metadata pentru **4 cursuri** și **8 probleme** dintr-un sistem de e-learning.

**Structură**:
```python
KNOWLEDGE_BASE = {
    "C1: Search Problems": {
        "n-queens": {
            "description": "...",
            "strategies": ["backtracking", "local search", "genetic algorithms"],
            "optimizations": ["MRV", "Forward Checking"],
            "type": "search_strategy"  # ← Identifică tipul
        },
        ...
    },
    "C2: Constraint Satisfaction": { ... },
    "C3: Game Theory": { ... }
}
```

**Probleme suportate**:
| Curs | Probleme | Tip |
|------|----------|-----|
| **C1: Search** | n-queens, knight_tour | `search_strategy` |
| **C2: CSP** | graph_coloring, hanoi | `csp` |
| **C3: Game** | nash_equilibrium, minmax_alphabeta | `matrix_game`, `tree_game` |

### `SYNONYMS` (Dict Static)
**Scopul**: Permite recunoașterea problemelor prin sinonime în limbaj natural.

**Exemplu**:
```python
"n-queens": ["n-queens", "regine"]  # User poate zice "regine" și sistemul mapează la "n-queens"
```

---

## 2️⃣ DOMAIN LOGIC (Calcule Matematice)

### `Node` (Clasă)
**Scopul**: Reprezentare unui nod din arborele de joc (pentru MinMax, Alpha-Beta).

**Atribute**:
- `value` (int/None): Valoarea payoff-ului dacă e frunză, None dacă e nod interior
- `children` (List[Node]): Lista nodurilor copil

**Metode**:
```python
def is_leaf(self) -> bool:
    """Returnează True dacă nodul nu are copii."""
    return len(self.children) == 0
```

**Exemplu**:
```
Node(value=5, children=[])  # Frunză cu valoare 5
Node(value=None, children=[...])  # Nod interior (MAX/MIN)
```

---

### `GameEngine` (Clasă Static)
**Scopul**: Efectuează calcule matematice pentru jocuri (Nash, MinMax, Alpha-Beta).

#### Metoda 1: `generate_random_tree(depth, branching_factor, min_val, max_val)`
**Ce face**: Generează un arbore aleator pentru MinMax/Alpha-Beta.

**Parametri**:
- `depth` (int): Adâncimea arborelui (ex: 3 = 3 nivele)
- `branching_factor` (int): Cât noduri copil pe nod (ex: 2 = binar)
- `min_val`, `max_val` (int): Range pentru valorile frunzelor

**Returnează**: `Node` - rădăcina arborelui generat

**Exemplu**:
```python
tree = GameEngine.generate_random_tree(depth=3, branching_factor=2)
# Generează:
#       MAX
#      /   \
#    MIN   MIN
#   / \    / \
#  ... (frunze cu valori 1-20)
```

---

#### Metoda 2: `tree_to_ascii(node, prefix, is_last, is_max, accumulator)`
**Ce face**: Convertește arborele în reprezentare text ASCII pentru afișare frumoasă.

**Parametri**:
- `node` (Node): Nodul curent
- `prefix` (str): Prefix pentru indentare
- `is_last` (bool): Dacă e ultimul copil al părintelui
- `is_max` (bool): Dacă nodul e MAX sau MIN
- `accumulator` (List): Colector de linii text (recursiv)

**Returnează**: String cu reprezentarea ASCII

**Exemplu Output**:
```
└── MAX
    ├── MIN
    │   ├── (5)
    │   └── (3)
    └── MIN
        ├── (8)
        └── (2)
```

---

#### Metoda 3: `solve_alpha_beta(root_node)`
**Ce face**: Evaluează arborele cu algoritm **Alpha-Beta Pruning** și numără frunzele vizitate.

**Logica**: 
1. Aplică recursive alpha-beta pe arbore
2. **Prune** (taie) ramuri când: $\beta \leq \alpha$
3. Numără frunzele vizitate (leaf nodes)

**Returnează**: `(root_value, visited_leaves_count)`

**Exemplu**:
```python
val, visited = GameEngine.solve_alpha_beta(tree)
# val = 5 (valoare rădăcină calculate)
# visited = 7 (din 16 frunze posibile, doar 7 vizitate datorită pruning-ului)
```

**Formula Alpha-Beta**:
```
MAX nod:  v = max(v, alpha_beta(child, α, β, False))
          α = max(α, v)
          IF β ≤ α: BREAK (pruning!)

MIN nod:  v = min(v, alpha_beta(child, α, β, True))
          β = min(β, v)
          IF β ≤ α: BREAK (pruning!)
```

---

#### Metoda 4: `generate_nash_matrix(rows, cols)`
**Ce face**: Generează matrice de joc aleator pentru Nash Equilibrium.

**Returnează**: `List[List[Tuple[int, int]]]` - matrice cu payoff-uri (J1, J2)

**Exemplu**:
```python
matrix = GameEngine.generate_nash_matrix(2, 2)
# Result: [[(4, 2), (2, 2)],
#          [(1, 1), (2, 3)]]
#          ↑ (payoff J1, payoff J2)
```

---

#### Metoda 5: `format_matrix(matrix)`
**Ce face**: Formatează matricea în string pentru afișare frumoasă.

**Returnează**: String cu matrice formatat
```
[
(4, 2), (2, 2)
(1, 1), (2, 3)
]
```

---

#### Metoda 6: `solve_nash(matrix)`
**Ce face**: Găsește **toți echilibrele Nash pur** dintr-o matrice.

**Algoritm**:
1. Pentru fiecare COLOANĂ: găsește best response pentru J1 (rândul cu max payoff)
2. Pentru fiecare RÂND: găsește best response pentru J2 (coloana cu max payoff)
3. INTERSECȚIE: Celule unde AMBII jucători sunt în best response

**Returnează**: `List[str]` cu echilibrele (ex: `["(Row 0, Col 0) -> Payoffs (4, 2)"]`)

**Exemplu**:
```python
matrix = [[(4, 2), (2, 2)],
          [(1, 1), (2, 3)]]

# J1 best responses (max per column):
#   Col 0: max(4, 1) = 4 → Row 0
#   Col 1: max(2, 3) = 3 → Row 1

# J2 best responses (max per row):
#   Row 0: max(2, 2) = 2 → Col 0, Col 1
#   Row 1: max(1, 3) = 3 → Col 1

# Intersecție:
#   (0, 0): Row 0 în BR_J1[Col 0] ✓ și Col 0 în BR_J2[Row 0] ✓ → ECHILIBRU
#   (1, 1): Row 1 în BR_J1[Col 1] ✓ și Col 1 în BR_J2[Row 1] ✓ → ECHILIBRU

# Output: ["(Row 0, Col 0) -> Payoffs (4, 2)", "(Row 1, Col 1) -> Payoffs (2, 3)"]
```

---

## 3️⃣ QUESTION GENERATOR

### `QuestionBundle` (Clasă Data Container)
**Scopul**: Pachetul complet pentru o întrebare generată.

**Atribute**:
- `question_text` (str): Textul întrebării
- `correct_answer_text` (str): Răspunsul așteptat (None pentru întrebări deschise)
- `topic_info` (Dict): Metadata despre subiect (strategii, optimizări, etc.)

**Exemplu**:
```python
bundle = QuestionBundle(
    question_text="Pentru N-Queens cu N=5, care e strategia opțimă?",
    correct_answer_text="Backtracking cu Forward Checking...",
    topic_info={
        "type": "search_strategy",
        "strategies": ["backtracking", "local search"]
    }
)
```

---

### `ContentGenerator` (Clasă)
**Scopul**: Factory pentru generarea diferitelor tipuri de întrebări.

#### Constructor
```python
def __init__(self):
    self.engine = GameEngine()  # Pentru calcule matematice
```

---

#### Metoda 1: `create_question(topic_key, topic_data)`
**Ce face**: Dispatcher care rutează la metoda corectă pe baza tipului de problemă.

**Logica**:
```python
if topic_data["type"] == "tree_game":           # MinMax/Alpha-Beta
    return self._create_minimax_bundle(...)
elif topic_data["type"] == "matrix_game":       # Nash
    return self._create_nash_bundle(...)
elif topic_data["type"] in ["csp", "search"]:  # Probleme cu instanță
    return self._create_strategy_bundle(...)
else:                                            # Default teorie
    return self._create_theory_bundle(...)
```

**Returnează**: `QuestionBundle`

---

#### Metoda 2: `_create_minimax_bundle(info)`
**Ce face**: Generează întrebare MinMax/Alpha-Beta cu arbore generat.

**Pași**:
1. Generează arbore aleator (adâncime 2-3)
2. Rezolvă cu `solve_alpha_beta()` → obține valoare + frunze vizitate
3. Formează întrebare: "Care e valoarea rădăcinii și câte frunze vizitate?"
4. Răspunsul conține ambele numere

**Exemplu Output**:
```
[Question]:
Se dă următorul arbore de joc:
└── MAX
    ├── MIN
    │   ├── (5)
    │   └── (3)
    ...

1. Care este valoarea în rădăcină?
2. Câte noduri FRUNZĂ sunt vizitate cu Alpha-Beta?

[Answer]: Valoarea este 5. Noduri vizitate: 7.
```

---

#### Metoda 3: `_create_nash_bundle(info)`
**Ce face**: Generează întrebare Nash Equilibrium cu matrice generată.

**Pași**:
1. Generează matrice 2x2 aleator
2. Rezolvă cu `solve_nash()` → obține echilibrele
3. Formează întrebare: "Identifică echilibrele Nash"
4. Răspunsul conține coordonatele

**Exemplu Output**:
```
[Question]:
Pentru jocul în formă normală:
[
(4, 2), (2, 2),
(1, 1), (2, 3)
]

Identifică toate echilibrele Nash pure.

[Answer]: Echilibrele Nash sunt: (Row 0, Col 0), (Row 1, Col 1).
```

---

#### Metoda 4: `_create_theory_bundle(key, info)`
**Ce face**: Generează întrebare generică pe teorie (pentru probleme fără instanță).

**Șabloane**:
```python
"De ce este {strat} o strategie bună pentru {prob}?"
"Ce optimizări se pot aplica la {prob}?"
```

**Exemplu Output**:
```
[Question]: De ce este backtracking o strategie bună pentru n-queens?
[Answer]: Backtracking este utilă deoarece este completă și corectă...
```

---

#### Metoda 5: `_create_strategy_bundle(key, info)`
**Ce face**: Router pentru probleme specifice cu instanță (N-Queens, Knight Tour, Graph Coloring, Hanoi).

**Dispatches**:
- `"n-queens"` → `_create_nqueens_strategy()`
- `"knight_tour"` → `_create_knight_tour_strategy()`
- `"graph_coloring"` → `_create_graph_coloring_strategy()`
- `"hanoi"` → `_create_hanoi_strategy()`

---

#### Metoda 6: `_create_nqueens_strategy(key, info)`
**Ce face**: Generează instanță N-Queens cu N aleator și regine conflictuale.

**Parametri Generați**:
- `N` (4-6): Dimensiunea tablei
- `conflicts` (1-3): Regine deja plasate care crează conflicte

**Exemplu Output**:
```
[Question]:
Pentru problema N-Queens cu N=5:
Trei regine sunt deja plasate și crează conflicte.
Cum rezolvi mai eficient?
A) Backtracking cu Forward Checking
B) Local Search (min-conflicts)
C) Genetic Algorithms

[Answer]: Răspuns: A) Backtracking cu Forward Checking...
```

---

#### Metoda 7: `_create_knight_tour_strategy(key, info)`
**Ce face**: Generează instanță Knight's Tour cu tablă de dimensiune aleatoare.

**Parametri Generați**:
- `board_size` (6-8): Dimensiunea tablei

**Exemplu Output**:
```
[Question]:
Pentru Knight's Tour pe tablă 7x7...
Care e cea mai bună abordare?
A) Backtracking pur
B) Backtracking cu Warnsdorff (MRV)
C) Backtracking cu Forward Checking

[Answer]: Răspuns: B) ... Warnsdorff reduce exponențial backtracking...
```

---

#### Metoda 8: `_create_graph_coloring_strategy(key, info)`
**Ce face**: Generează instanță Graph Coloring cu număr de noduri și densitate.

**Parametri Generați**:
- `num_nodes` (5-8): Noduri în graf
- `density` ("rară", "medie", "densă"): Densitate muchii

**Exemplu Output**:
```
[Question]:
Un graf cu 6 noduri și conexiuni medie trebuie colorat...
Alege strategia optimă...
A) CSP cu AC-3
B) Greedy coloring
C) Backtracking fără propagare

[Answer]: Răspuns: A) CSP cu AC-3 reduce spaţiu căutare...
```

---

#### Metoda 9: `_create_hanoi_strategy(key, info)`
**Ce face**: Generează instanță Hanoi cu discuri și tije.

**Parametri Generați**:
- `num_discs` (4-6): Discuri
- `num_pegs` (3-5): Tije

**Exemplu Output**:
```
[Question]:
Pentru Hanoi cu 5 discuri și 4 tije...
Care abordare alegi?
A) Recursion pură
B) Recursion cu memoization
C) Iterativ cu stivă

[Answer]: Răspuns: C) Iterativ este mai rapid, 2^5-1 = 31 pași...
```

---

#### Metoda 10: `generate_problem_selection_question()`
**Ce face**: Generează o **întrebare deschisă** unde user trebuie să aleagă din 4+ probleme și să justifice.

**Pași**:
1. Alege random o problemă din 4 disponibile
2. Generează o instanță pentru acea problemă
3. Formează întrebare cu opțiuni multiple A/B/C
4. **NU precomputa răspunsul** (correct_answer_text = None)

**Exemplu Output**:
```
[Question]:
PROBLEMA: N-Queens
Descriere: Plasa N regine pe tablă...

INSTANȚĂ: N = 5, cu 2 regine în conflict

ÎNTREBARE: Care strategie alegi?
A) Backtracking cu FC
B) Local Search
C) Genetic Algorithms

[Metadata]:
topic_info = {
    "type": "problem_selection",
    "problem": "n-queens",
    "instance": {"n": 5, "conflicts": 2},
    "strategies": [...]
}
```

---

#### Metoda 11: `_format_problem_selection_question(problem_key, problem, instance)`
**Ce face**: Formează textul întrebării pe baza tipului de problemă și instanței generate.

**Logica**: 4 branches (n-queens, knight_tour, graph_coloring, hanoi) - fiecare formatează altfel.

---

## 4️⃣ EVALUATOR

### `Evaluator` (Clasă Static)
**Scopul**: Evaluează răspunsurile utilizatorului versus răspunsurile așteptate.

#### Metoda 1: `normalize(text)`
**Ce face**: Normalizează textul pentru comparație (lowercase + înlocuire diacritice).

**Exemplu**:
```python
normalize("Echilibrul NASH la (0,0)")
# Output: "echilibrul nash la (0,0)"
```

---

#### Metoda 2: `cosine_similarity(s1, s2)`
**Ce face**: Calculează **similaritate cosinus** între 2 stringuri.

**Algoritm**:
1. Tokenizează ambele stringuri în cuvinte
2. Calculează frecvența fiecărui cuvânt
3. Aplică formula: $\cos(θ) = \frac{\text{dot product}}{\|\vec{v1}\| \cdot \|\vec{v2}\|}$

**Returnează**: Float 0.0-1.0 (1.0 = identic)

**Exemplu**:
```python
cosine_similarity(
    "Backtracking reduce căutare exponențial",
    "Backtracking reduce exponențial căutare"
)
# Output: 0.95 (foarte asemănător)
```

**Formula**:
$$\cos(θ) = \frac{\sum (v1_i \cdot v2_i)}{\sqrt{\sum v1_i^2} \cdot \sqrt{\sum v2_i^2}}$$

---

#### Metoda 3: `evaluate(user_answer, system_bundle)`
**Ce face**: Evaluează răspunsul utilizatorului și returnează scor + feedback.

**Logica Multi-Nivel**:

```python
def evaluate(self, user_answer, system_bundle):
    # 1. BASELINE: Similaritate semantică
    sim_score = cosine_similarity(user_answer, correct_answer)
    score = int(sim_score * 100)
    
    # 2. SPECIAL CASE: Răspunsuri numerice (MinMax)
    if "vizitate" in correct_answer:
        nums_correct = extract_numbers(correct_answer)
        nums_user = extract_numbers(user_answer)
        if nums_correct ⊆ nums_user:
            score = 100  # Perfect!
        elif no nums_user:
            score = 0    # Missing numbers
    
    # 3. SPECIAL CASE: Nash Equilibrium
    if "echilibr" in normalize(correct_answer):
        correct_coords = extract_coords(correct_answer)  # (0, 0), (1, 1)
        user_coords = extract_coords(user_answer)
        
        if user_coords == correct_coords:
            score = 100  # All correct
        elif user_coords ⊂ correct_coords:
            score = 50 + (|matched| / |correct|) * 50  # Partial credit
        else:
            score = sim_score * 50  # No match, use similarity
    
    return {"score": score, "feedback": message, "correct": correct_answer}
```

**3 Niveluri de Evaluare**:

| Tip Răspuns | Evaluare | Logica |
|------------|----------|--------|
| **Teorie** | Similaritate cosinus | 0-100 pt pe baza de cuvinte similare |
| **MinMax** | Extracție numere | 100 dacă găsește numerele corecte, 0 altfel |
| **Nash** | Extracție coordonate | Scor parțial pt fiecare echilibru corect |

**Exemplu MinMax**:
```
Correct: "Valoarea = 5, Noduri = 7"
User:    "Raspunsul e 5 frunze vizitate, valoare 5"
Extract: correct_nums = [5, 7], user_nums = [5, 5]
Result:  [5] ⊆ [5, 7] → Score = 100 ✓
```

**Exemplu Nash**:
```
Correct: "(Row 0, Col 0) → (4,2); (Row 1, Col 1) → (2,3)"
User:    "Echilibrele sunt la (0, 0) și (1, 1)"
Extract: correct = {(0,0), (1,1)}, user = {(0,0), (1,1)}
Match:   2/2 = 100% → Score = 100 ✓

User2:   "Doar (0, 0)"
Match:   1/2 = 50% → Score = 50 + 25 = 75 (partial)
```

---

## 5️⃣ MAIN PIPELINE

### `get_topic_from_prompt(prompt)`
**Ce face**: Parsează inputul utilizatorului și identifică cursul/problema dorită.

**Logica**:
1. **Curs Direct**: Dacă input conține "c1", "c2", "c3", "search", "constraint", "game"
   - Alege random o problemă din acel curs
2. **Sinonim**: Caută în `SYNONYMS` dict dacă menționează o problemă
3. **Fallback**: Dacă nu găsește nimic, defaultează la "minmax_alphabeta"

**Returnează**: `(topic_key, topic_data_dict)`

**Exemplu**:
```python
get_topic_from_prompt("intrebare despre regine")
# → ("n-queens", {description: "...", strategies: [...], type: "search_strategy"})

get_topic_from_prompt("c3")
# → ("nash_equilibrium" or "minmax_alphabeta", {...})  # random din C3

get_topic_from_prompt("da-mi ceva")
# → ("minmax_alphabeta", {...})  # fallback
```

---

### `main()`
**Ce face**: REPL (Read-Eval-Print Loop) interactiv pentru sistemul de învățare.

**Fluxul**:
```
1. Afișează instrucțiuni
2. Loop infinit:
   a) Citește input utilizator
   b) Dacă "exit" → quit
   c) Dacă "selectie problema" → generează problem selection bundle
   d) Altfel:
      - Identifică topic
      - Generează întrebare cu răspuns
      - Afișează întrebare
      - Citește răspuns utilizator
      - Evaluează cu scorer
      - Afișează scor + feedback
```

**Exemplu Interacțiune**:
```
User Input > intrebare nash
--- Subiect identificat: nash_equilibrium ---

[AI Question]:
Pentru jocul în formă normală de mai jos...
[matricea]
Identifică echilibrele Nash.

[Your Answer]: Echilibrele sunt la (0, 0) și (1, 1)

--- REZULTAT ---
Scor: 100
Feedback: Corect! Ai identificat corect toate echilibrele Nash.
Răspunsul corect era: (Row 0, Col 0) → Payoffs (4, 2); (Row 1, Col 1) → Payoffs (2, 3)
```

---

## 📋 TABEL COMPLET - FUNCȚII & ROLURI

| Clasă | Metodă | Scop | Input | Output |
|-------|--------|------|-------|--------|
| **Node** | `__init__` | Creare nod arbore | value, children | - |
| | `is_leaf()` | Verifică dacă frunză | - | bool |
| **GameEngine** | `generate_random_tree()` | Arbore MinMax | depth, branching | Node |
| | `tree_to_ascii()` | Text arbore | node, params | str |
| | `solve_alpha_beta()` | MinMax + pruning | root_node | (val, leaves) |
| | `generate_nash_matrix()` | Matrice joc | rows, cols | List[List[Tuple]] |
| | `format_matrix()` | String matrice | matrix | str |
| | `solve_nash()` | Echilibre Nash | matrix | List[str] |
| **QuestionBundle** | `__init__` | Container | q_text, a_text, info | - |
| **ContentGenerator** | `create_question()` | Factory dispatcher | topic_key, data | QuestionBundle |
| | `_create_minimax_bundle()` | MinMax question | info | QuestionBundle |
| | `_create_nash_bundle()` | Nash question | info | QuestionBundle |
| | `_create_theory_bundle()` | Theory question | key, info | QuestionBundle |
| | `_create_strategy_bundle()` | Strategy with instance | key, info | QuestionBundle |
| | `_create_nqueens_strategy()` | N-Queens question | key, info | QuestionBundle |
| | `_create_knight_tour_strategy()` | Knight Tour question | key, info | QuestionBundle |
| | `_create_graph_coloring_strategy()` | Graph Coloring question | key, info | QuestionBundle |
| | `_create_hanoi_strategy()` | Hanoi question | key, info | QuestionBundle |
| | `generate_problem_selection_question()` | Open-ended selection | - | QuestionBundle |
| | `_format_problem_selection_question()` | Format selection Q | problem_key, problem, inst | str |
| **Evaluator** | `normalize()` | Normalize text | text | str |
| | `cosine_similarity()` | Text similarity | s1, s2 | float |
| | `evaluate()` | Score answer | user_ans, bundle | {score, feedback, correct} |
| **Module** | `get_topic_from_prompt()` | Parse user input | prompt | (topic_key, topic_data) |
| | `main()` | REPL loop | - | Loop infinit |

---

## 🔄 FLUX DE EXECUȚIE - EXEMPLU COMPLET

```
User Input: "genereaza minmax"
     ↓
get_topic_from_prompt("genereaza minmax")
     → Identifică "minmax" în SYNONYMS
     → Returnează ("minmax_alphabeta", {...type: "tree_game"})
     ↓
ContentGenerator.create_question("minmax_alphabeta", {...type: "tree_game"})
     → Dispatches: type == "tree_game"
     → Calls: _create_minimax_bundle(...)
     ↓
_create_minimax_bundle():
   1. GameEngine.generate_random_tree(depth=2, branching=2)
      → Crează arbore cu MAX/MIN noduri și 4 frunze cu valori
   2. GameEngine.solve_alpha_beta(tree)
      → Evaluează recursive, taie branuri
      → Returnează (root_value=5, visited_leaves=3)
   3. GameEngine.tree_to_ascii(tree)
      → Formează string arbore
   4. Crează întrebare text
   5. Crează răspuns text cu numerele corecte
   6. Returnează QuestionBundle(q_text, a_text, info)
     ↓
main() afișează QuestionBundle.question_text
     ↓
User Input: "valoarea e 5, 3 frunze"
     ↓
Evaluator.evaluate(user_answer, bundle):
   1. cosine_similarity(user_ans, correct_ans) → 0.9
   2. Special case: "vizitate" în correct_ans?
      → YES! Extract numbers
      → nums_correct = [5, 3]
      → nums_user = [5, 3]
      → [5, 3] ⊆ [5, 3] → MATCH!
      → score = 100
   3. Returnează {score: 100, feedback: "Corect!", correct: "..."}
     ↓
main() afișează rezultat
```

---

## 🎯 REZUMAT ROLURI

| Componentă | Rol |
|-----------|-----|
| **KNOWLEDGE_BASE + SYNONYMS** | Bază de date probleme și cuvinte cheie |
| **Node + GameEngine** | Motor matematic pentru calcule jocuri |
| **QuestionBundle + ContentGenerator** | Generator de întrebări customizate |
| **Evaluator** | Notar răspunsuri cu 3 strategii |
| **get_topic_from_prompt() + main()** | Pipeline și interfață utilizator |

Sistmul este o **platform e-learning integrată** care generează, evaluează și cotează răspunsuri la probleme de teorie jocurilor și căutare! 🎓

