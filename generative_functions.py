import random
import ast

def generate_normal_form_matrix(rows=3, cols=3, min_payoff=-5, max_payoff=5):
    """
    Generează o matrice de joc în formă normală.
    Returnează o listă de liste unde fiecare celulă este (payoff_J1, payoff_J2).
    """
    matrice = [
        [ (random.randint(min_payoff, max_payoff),
           random.randint(min_payoff, max_payoff))
          for _ in range(cols) ]
        for _ in range(rows)
    ]
    return matrice

def verify_nash(matrice):
    """
    Primește o matrice în forma normală (listă de liste cu perechi).
    Returnează o listă cu toate echilibrele Nash pur (ca tuple (rând, coloană)).
    """

    n_rows = len(matrice)
    n_cols = len(matrice[0])

    echilibre = []

    # Pas 1: best responses pentru J1 (rânduri)
    best_R = {c: [] for c in range(n_cols)}  # pentru fiecare coloană

    for c in range(n_cols):
        maxim = max(matrice[r][c][0] for r in range(n_rows))  # payoff J1
        for r in range(n_rows):
            if matrice[r][c][0] == maxim:
                best_R[c].append(r)

    # Pas 2: best responses pentru J2 (coloane)
    best_C = {r: [] for r in range(n_rows)}  # pentru fiecare rând

    for r in range(n_rows):
        maxim = max(matrice[r][c][1] for c in range(n_cols))  # payoff J2
        for c in range(n_cols):
            if matrice[r][c][1] == maxim:
                best_C[r].append(c)

    # Pas 3: găsim celulele care sunt best response pentru amândoi
    for r in range(n_rows):
        for c in range(n_cols):
            if r in best_R[c] and c in best_C[r]:
                echilibre.append((r, c))

    return echilibre

def extract_matrix_from_text(text):
    start = text.find('[')
    if start == -1:
        raise ValueError("Nu am găsit niciun '[' în text.")
    # parcurgem pentru a găsi paranteza de închidere corespunzătoare
    depth = 0
    end = None
    for i in range(start, len(text)):
        ch = text[i]
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                end = i
                break
    if end is None:
        raise ValueError("Parantezele drepte nu sunt echilibrate.")
    substr = text[start:end + 1]
    try:
        matrice = ast.literal_eval(substr)
    except Exception as e:
        raise ValueError(f"Evaluare literală eșuată: {e}\nSubstring extras: {substr!r}")
    return matrice


if __name__ == "__main__":
    M = generate_normal_form_matrix(3, 3)

    print("Matrice generată:")
    for row in M:
        print(row)

    # Caută echilibre Nash
    nash = verify_nash(M)

    print("\nEchilibre Nash găsite:")
    print(nash if nash else "Nu există echilibru Nash pur.")