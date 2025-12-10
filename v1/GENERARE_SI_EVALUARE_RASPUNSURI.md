# 📚 Generare și Evaluare Răspunsuri - Documentație Completă

## 🎯 Flux General

```
ÎNTREBARE (cu tip specific)
         ↓
IDENTIFICARE TIP PROBLEM
         ↓
GENERARE RĂSPUNS (după tip)
         ↓
EVALUARE RĂSPUNS (scoring + feedback)
         ↓
COMPARARE vs Răspuns Așteptat
```

---

## 1️⃣ TIPURI DE PROBLEME (Knowledge Base)

Sistemul recunoaște **4 tipuri principale** de probleme:

### A. **Search Strategy Problems** (Probleme de Căutare)
- **Exemple**: N-Queens, Knight Tour, Hanoi
- **Caracteristici**: Implică explorare spațiu stări, backtracking
- **Strategii disponibile**: backtracking, local search, recursion
- **Optimizări**: MRV, FC (Forward Checking)

### B. **Constraint Satisfaction Problems (CSP)** 
- **Exemple**: Graph Coloring, Sudoku
- **Caracteristici**: Variabile cu domenii și constrângeri
- **Strategii disponibile**: backtracking, constraint propagation, AC-3
- **Optimizări**: AC-3, MRV, FC, memoization

### C. **Matrix Games (Game Theory)**
- **Exemple**: Nash Equilibrium
- **Caracteristici**: Joc în formă normală cu matrice payoff
- **Strategii disponibile**: dominance elimination, best response
- **Optimizări**: niciuna (pur teorie)

### D. **Tree Games (Game Theory)**
- **Exemple**: Minimax, Alpha-Beta Pruning
- **Caracteristici**: Arbore de joc cu valori leaf
- **Strategii disponibile**: minimax, alpha-beta pruning
- **Optimizări**: move ordering, transposition tables

---

## 2️⃣ GENERARE RĂSPUNSURI (generator_raspunsuri.py)

### 🔍 Cum funcționează?

**Clasă**: `GeneratorRaspunsuri` - metoda `genereaza(intrebare, problema, info)`

#### PASUL 1: Normalizare și Identificare
```python
def genereaza(self, intrebare, problema, info):
    # Normalizare text: minuscule, înlocuire diacritice
    intrebare_n = norm(intrebare.lower())  # "cea mai bună" → "cea mai buna"
    
    # Identifică strategia menționată în întrebare
    strategie_intrebata = None
    for s in info.get("strategii", []):
        if s.lower() in intrebare_l:
            strategie_intrebata = s
            break
```

#### PASUL 2: Pattern Matching pe Tip Întrebare

Sistemul recunoaște **8 tipuri de întrebări**:

| Tip | Pattern | Exemplu | Răspuns |
|-----|---------|---------|---------|
| **Best Strategy** | "cea mai bună" OU "cea mai potrivită" | "Care e cea mai bună strategie?" | Justificare strategiei + cum se aplică |
| **Generic Strategy** | "strategie" (dar NU "cum diferă") | "Ce strategii folosești?" | Lista strategii pentru problemă |
| **Comparative** | "diferă" OU "compara" OU "cum diferă" | "Cum diferă X de Y?" | Comparație detaliată între 2+ strategii |
| **Advantages/Why** | "avantaj" OU "de ce" | "De ce folosi X?" | Justificare + beneficii |
| **Variable Assignment** | "asignarea variabilelor" + (FC\|MRV\|AC-3) | "Cum se asignează variabile cu FC?" | Explicare algoritm + pași |
| **Optimizations** | "optimiz" | "Ce optimizări sunt disponibile?" | Lista + detalii |
| **Complexity** | "complexitate" | "Care e complexitatea?" | Analiză timp + spațiu |
| **Game Theory** | "nash" OU "minmax" OU "alpha-beta" | "Găsiți echilibrul Nash" | Calcul matematic |

#### PASUL 3: Generare Răspuns Personalizat

**Exemplu 1 - Best Strategy:**
```python
if "cea mai buna" in intrebare_n or "cea mai potrivita" in intrebare_n:
    s = strategie_intrebata or info["strategii"][0]
    return justificare(s)
    # Output: "Backtracking este potrivită pentru N-Queens deoarece este 
    #          completă și corectă; combinată cu MRV/FC reduce semnificativ..."
```

**Exemplu 2 - Comparative:**
```python
if "difera" in intrebare_n or "compara" in intrebare_n:
    s = strategie_intrebata  # ex: "Backtracking"
    alt1, alt2 = alte_strategii[0], alte_strategii[1]
    comp = (f"{s} abordează {problema} ca CSP: aplică propagarea constrangerilor "
            f"și heuristici MRV. Față de {alt1}, {s} reduce căutarea prin filtrare...")
    return comp
```

**Exemplu 3 - Optimizations:**
```python
if "optimiz" in intrebare_n:
    if "cea mai" in intrebare_n:
        # Alege UNA singură optimizare (cea mai eficientă)
        if "constraint propagation" in intrebare_n and "AC-3" in opts:
            preferata = "AC-3"
        return f"Cea mai eficientă optimizare este {preferata} pentru {problema}."
    else:
        # Listează TOATE optimizările disponibile
        return f"Optimizări: {', '.join(opts)}."
```

**Exemplu 4 - Game Theory (Nash):**
```python
if "nash" in intrebare_n:
    matrice = extract_matrix_from_text(intrebare_n)
    echilibru_nash = verify_nash(matrice)  # Calcul matematic
    if echilibru_nash:
        return str(echilibru_nash)  # "(0, 1), (1, 0)" - pozițiile echilibrelor
    return "Nu are echilibru Nash pur"
```

### 📋 Șabloane de Justificare

Pentru fiecare strategie, există o **justificare predefinită**:

```python
def justificare(s: str) -> str:
    if "constraint" in s.lower():
        return f"{s} reduce spațiul de căutare prin propagarea constrangerilor (AC-3/FC)"
    if "backtracking" in s.lower():
        return f"{s} este completă și corectă; combinată cu MRV/FC/AC-3 reduce ramurile"
    if "greedy" in s.lower():
        return f"{s} este rapidă dar NU garantează soluții optime"
    ...
```

---

## 3️⃣ EVALUARE RĂSPUNSURI (evaluator.py / verificare_raspunsuri.py)

### 🎯 Sistem de Scoring (0-100 puncte)

**Metodă**: `EvaluatorRaspunsuri.verifica(intrebare, raspuns, problema, info)`

#### Criterii de Evaluare:

| Criteriu | Puncte | Condiție | Feedback dacă FAIL |
|----------|--------|----------|-------------------|
| **Mențiune Strategie Corectă** | 40 | Răspunsul conține una din strategiile pentru problemă | "Nu ai menționat o strategie corectă" |
| **Optimizări (dacă cerute)** | 30 | Întrebarea are "optimiz" ȘI răspunsul conține optimizare din info | "Nu ai menționat optimizările specifice" |
| **Răspunde la Concept** | 20 | Răspunsul conține: complexitate, timp, spațiu, O(n), "mai rapid", "mai lent" | - |
| **"De ce/Avantaje"** | 20 | Dacă întrebarea e "de ce/avantaje", răspunsul trebuie cuvinte ca: "eficient", "rapid", "reduce", "optimal", "garanteaza", "mai bun" | - |
| **Descriere Problemă** | 10 | Bonus dacă apare cuvântul cheie din descriere | - |

#### Calcul Final:
```python
scor = 0

# 1. Verificare strategie (40 pct)
strategii = [normalize(s) for s in info["strategii"]]
if any(s in raspuns_normalized for s in strategii):
    scor += 40  ✓
else:
    feedback.append("Nu ai menționat o strategie corectă.")

# 2. Verificare optimizări (30 pct, doar dacă relevante)
if "optimiz" in intrebare_normalized and info["optimizari"]:
    optimizari = [normalize(o) for o in info["optimizari"]]
    if any(o in raspuns_normalized for o in optimizari):
        scor += 30  ✓
    else:
        feedback.append("Nu ai menționat optimizările...")

# 3. Concepte (20 pct)
if any(kw in raspuns_normalized for kw in ["complexitate","timp","spatiu","o(n)"]):
    scor += 20  ✓

# 4. "De ce" / Avantaje (20 pct)
if any(kw in intrebare_normalized for kw in ["de ce", "avantaje"]):
    if any(kw in raspuns_normalized for kw in ["eficient", "rapid", "reduce", "optimal"]):
        scor += 20  ✓

# 5. Descriere (10 pct bonus)
if info["descriere"].split()[0].lower() in raspuns_normalized:
    scor += 10  ✓

# Capare la 100
scor = min(scor, 100)

# Verdict final
if scor < 60:
    feedback.insert(0, "Răspuns incomplet sau incorect.")
else:
    feedback.insert(0, "Răspuns corect.")
```

#### Exemplu de Evaluare Completă:

**Întrebare**: "De ce backtracking cu MRV este mai bună pentru N-Queens?"

**Răspuns Utilizator**: "Backtracking reduce domenii și permite continuare rapida"

**Calculul**:
```
Strategii în text? "backtracking" ✓ → +40 pct
Optimizări cerute? "MRV" în info, dar NU în răspuns ✗ → +0 pct
Concept (timp/spațiu)? NU → +0 pct
"De ce" + "reduce/rapid"? ✓ → +20 pct
Descriere? NU → +0 pct
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 60 pct → "Răspuns corect"
```

### 🔄 Comparare Răspunsuri (User vs Generated)

**Metodă**: `EvaluatorRaspunsuri.compara(intrebare, raspuns_utilizator, raspuns_generat, problema, info)`

```python
def compara(self, intrebare, raspuns_util, raspuns_gen, problema, info):
    # Evaluează AMBELE răspunsuri cu aceeași metodă
    eval_user = self.verifica(intrebare, raspuns_util, problema, info)
    eval_gen = self.verifica(intrebare, raspuns_gen, problema, info)
    
    # Compară scorurile
    if eval_user["scor"] > eval_gen["scor"]:
        verdict = ">"  # User mai bun
    elif eval_user["scor"] < eval_gen["scor"]:
        verdict = "<"  # Generated mai bun
    else:
        verdict = "="  # Egal
    
    return {
        "raspuns_user": eval_user,
        "raspuns_generat": eval_gen,
        "verdict": verdict
    }
```

**Output**:
```json
{
    "raspuns_user": {
        "scor": 60,
        "feedback": "Răspuns corect. Nu ai menționat optimizările..."
    },
    "raspuns_generat": {
        "scor": 90,
        "feedback": "Răspuns corect."
    },
    "verdict": "<"  // User < Generated
}
```

---

## 4️⃣ INTEGRARE - Fluxul Complet

### Scenariul 1: Search Problems (N-Queens)

```
1. GENERARE ÎNTREBARE
   Întrebare: "Explicați de ce backtracking este cea mai bună alegere pentru N-Queens"
   Problema: "n-queens"
   Info: {
       "strategii": ["backtracking", "local search", "genetic algorithms"],
       "optimizari": ["MRV", "Forward Checking"]
   }

2. GENERARE RĂSPUNS CORECT
   Pattern: "de ce" + "cea mai bună"
   → Genereaza justificare pentru "backtracking"
   Răspuns: "Backtracking este potrivită pentru N-Queens deoarece este completă 
            și corectă; combinată cu MRV/FC reduce semnificativ ramurile explorate..."

3. EVALUARE RĂSPUNS UTILIZATOR
   User răspunde: "Backtracking merge rapid cu optimizări"
   
   Evaluare:
   - Strategie? "backtracking" ✓ → +40 pct
   - Optimizări cerute? "optimiz" NU în întrebare → +0 pct
   - Concepte? "rapid" ≠ "complexitate/timp" → +0 pct
   - "De ce" + Avantaje? "merge rapid" ✓ → +20 pct
   - Descriere? NU → +0 pct
   TOTAL: 60 pct ✓ Corect

4. COMPARARE
   eval_user = 60 pct
   eval_generated = 95 pct (răspunsul generat e mai detaliat)
   verdict = "<"
```

### Scenariul 2: CSP - Graph Coloring (Optimizări)

```
1. GENERARE ÎNTREBARE
   Întrebare: "Pentru Graph Coloring, care e cea mai eficientă optimizare dintre AC-3, MRV?"
   Problema: "graph_coloring"
   Info: {
       "strategii": ["backtracking", "constraint satisfaction", "greedy"],
       "optimizari": ["AC-3", "MRV", "FC"]
   }

2. GENERARE RĂSPUNS CORECT
   Pattern: "cea mai" + "eficienta" + "optimiz"
   → Alege AC-3 (pentru constraint propagation)
   Răspuns: "Pentru Graph Coloring, cea mai eficientă optimizare este AC-3 
            cand folosim constraint satisfaction, deoarece reduce consistent domenii variabilelor."

3. EVALUARE
   User: "AC-3 e mai bună decât MRV"
   - Strategie? "ac-3" ✓ (se recunoaște ca optimizare) → +40 pct
   - Optimizări? "ac-3" și "optimiz" în întrebare ✓ → +30 pct
   - Concept? NU → +0 pct
   - Avantaje? "mai bună" ✓ → +20 pct
   - Descriere? NU → +0 pct
   TOTAL: 90 pct ✓ Corect
```

### Scenariul 3: Game Theory - Nash Equilibrium

```
1. GENERARE ÎNTREBARE
   Întrebare: "Pentru jocul [[4,2], [2,3]], există echilibru Nash pur?"
   Problema: "nash_equilibrium"
   Info: {
       "strategii": ["dominance elimination", "best response"],
       "optimizari": []
   }

2. GENERARE RĂSPUNS CORECT
   Pattern: "nash"
   → Extract matrice din text
   → Aplică verify_nash() - calcul matematic
   Rezultat: ((0,0), (1,1)) - echilibrele Nash pure

3. EVALUARE
   User: "Echilibrele sunt la (0,0) și (1,1)"
   - Strategie? NU menționată → +0 pct
   - Optimizări? Nu relevante → +0 pct
   - Concept? NU → +0 pct
   - Avantaje? NU → +0 pct
   - Descriere? NU → +0 pct
   TOTAL: 0 pct ✗ Incorect (dar răspunsul e CORECT matematic!)
   
   ⚠️ OBSERVAȚIE: Pentru probleme de tip Game Theory, evaluarea nu funcționează bine.
                  Trebuie adăugat cod special pentru verificare răspunsuri matematice.
```

---

## 5️⃣ FUNCȚII HELPER IMPORTANTE

### 📐 Game Theory - Calcul Nash

```python
def verify_nash(matrice):
    """Găsește toate echilibrele Nash pur din matrice payoff."""
    
    # PASUL 1: Best response pentru J1 (Player 1 - rânduri)
    best_R = {}
    for coloana in range(n_cols):
        payoff_j1_per_row = [matrice[r][coloana][0] for r in range(n_rows)]
        maxim = max(payoff_j1_per_row)
        best_R[coloana] = [r for r in range(n_rows) if matrice[r][coloana][0] == maxim]
    
    # PASUL 2: Best response pentru J2 (Player 2 - coloane)
    best_C = {}
    for rand in range(n_rows):
        payoff_j2_per_col = [matrice[rand][c][1] for c in range(n_cols)]
        maxim = max(payoff_j2_per_col)
        best_C[rand] = [c for c in range(n_cols) if matrice[rand][c][1] == maxim]
    
    # PASUL 3: Intersecție = Echilibru Nash
    echilibre = []
    for r in range(n_rows):
        for c in range(n_cols):
            if r in best_R[c] and c in best_C[r]:
                echilibre.append((r, c))
    
    return echilibre
```

**Exemplu**:
```
Matrice: [[(3,4), (2,2)],
          [(1,1), (2,3)]]

Best Response J1 (Max rânduri pentru fiecare coloană):
  Col 0: max(3,1) = 3 → best_R[0] = [0]
  Col 1: max(2,2) = 2 → best_R[1] = [0,1]

Best Response J2 (Max coloane pentru fiecare rând):
  Row 0: max(4,2) = 4 → best_C[0] = [0]
  Row 1: max(1,3) = 3 → best_C[1] = [1]

Intersecție:
  (0,0): 0 in best_R[0] ✓ și 0 in best_C[0] ✓ → ECHILIBRU
  (1,1): 1 in best_R[1] ✓ și 1 in best_C[1] ✓ → ECHILIBRU

Rezultat: [(0,0), (1,1)]
```

### 🎮 Tree Games - Alpha-Beta Pruning

```python
def solve_alpha_beta(root_node):
    """Evaluează arborele cu Alpha-Beta și contează nodurile vizitate."""
    visited_leaves = 0
    
    def alpha_beta(node, alpha, beta, is_max):
        if node.is_leaf():
            visited_leaves += 1
            return node.value
        
        if is_max:
            value = -∞
            for child in node.children:
                value = max(value, alpha_beta(child, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:  # PRUNING!
                    break
            return value
        else:
            value = +∞
            for child in node.children:
                value = min(value, alpha_beta(child, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:  # PRUNING!
                    break
            return value
    
    final_value = alpha_beta(root_node, -∞, +∞, True)
    return final_value, visited_leaves
```

---

## 6️⃣ FLOW DE LUCRU - REZUMAT

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLU COMPLET                            │
└─────────────────────────────────────────────────────────────┘

INPUT: Utilizator face o ÎNTREBARE
        ↓
1️⃣  RECUNOAȘTERE TIP
   - Normalizare text
   - Pattern matching (cea mai bună, diferă, optimiz, nash, etc.)
   
2️⃣  LOOKUP KNOWLEDGE BASE
   - Găsește "problema" și "info" din Knowledge Base
   - Extrage strategii + optimizări disponibile
   
3️⃣  GENERARE RĂSPUNS
   - În funcție de tip întrebare:
     * Best Strategy → justificare + avantaje
     * Comparative → comparație 2+ strategii
     * Optimizations → enumerare + detali
     * Game Theory → calcul matematic (Nash/MinMax)
   
4️⃣  EVALUARE RĂSPUNS UTILIZATOR
   - Dă o notă din 100 pe baza criteriilor fixe
   - Oferă feedback detaliat
   
5️⃣  COMPARARE (opțional)
   - Răspuns Utilizator vs Răspuns Generat
   - Verdict: > / = / <

OUTPUT: Score + Feedback + (opțional) Comparație
```

---

## 🔧 Exemple de Cod - Integrare

```python
from generator_raspunsuri import GeneratorRaspunsuri
from evaluator import EvaluatorRaspunsuri
from knowledge import cursuri

# 1. Setup
gen = GeneratorRaspunsuri()
eval_obj = EvaluatorRaspunsuri()

# 2. Pregătire date
problema = "n-queens"
info = cursuri["C1: Search Problems"][problema]
intrebare = "De ce backtracking este cea mai bună pentru N-Queens?"

# 3. Generare răspuns corect
raspuns_generat = gen.genereaza(intrebare, problema, info)
print("Răspuns generat:", raspuns_generat)

# 4. Evaluare răspuns utilizator
raspuns_user = "Backtracking merge repede cu MRV"
evaluare = eval_obj.verifica(intrebare, raspuns_user, problema, info)
print("Scor user:", evaluare["scor"])
print("Feedback:", evaluare["feedback"])

# 5. Comparare
comparatie = eval_obj.compara(intrebare, raspuns_user, raspuns_generat, problema, info)
print(f"User {comparatie['verdict']} Generated")
```

---

## ⚠️ Limitări și Observații

1. **Game Theory Evaluation**: Evaluatorul nu verifică corectitudinea răspunsurilor matematice (Nash, MinMax). Trebuie cod special.

2. **Normalizare**: Sistemul normalizează diacritice (ă→a, î→i, etc.) dar nu tratează cuvinte sinonime (trebuie adăugat lookup pe `sinonime` dict).

3. **Scoring Rigid**: Punctele sunt fixe (40+30+20+20+10). Ar putea fi mai flexibil pe baza dificultății.

4. **Feedback Generic**: Mesajele feedback sunt predefinite. Ar putea fi mai personalizate.

5. **Context**: Evaluatorul nu ține seamă de context din răspunsul anterior (fiecare evaluare e independentă).

---

## 📞 Cum să Adaugi o Nouă Problemă?

1. **Adaugă în `knowledge.py`** (dict `cursuri`):
   ```python
   "problemaNoua": {
       "descriere": "Descriere scurtă",
       "strategii": ["str1", "str2", "str3"],
       "optimizari": ["opt1", "opt2"],
   }
   ```

2. **Adaugă Sinonime** (dacă necesară):
   ```python
   sinonime["problemaNoua"] = ["sinonim1", "sinonim2"]
   ```

3. **Adaugă Logică Specială** (dacă necesară în `generator_raspunsuri.py`):
   ```python
   if "problemaNoua" in intrebare_n:
       return f"Răspuns special pentru {problema}"
   ```

4. **Test**:
   ```python
   gen.genereaza("Ce strategie pentru problemaNoua?", "problemaNoua", info)
   ```

---

Gata! Sistemul tău e documentat complet. 🎉
