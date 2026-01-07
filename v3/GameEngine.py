import itertools
import math
import random
from v3.Node import Node

class GameEngine:
    """Handles the math/logic: Tree generation, Nash solving, Minimax."""

    @staticmethod
    def generate_random_tree(depth, branching_factor, min_val=1, max_val=20):
        if depth == 0:
            return Node(value=random.randint(min_val, max_val))
        node = Node()
        for _ in range(branching_factor):
            node.children.append(GameEngine.generate_random_tree(depth - 1, branching_factor, min_val, max_val))
        return node

    @staticmethod
    def tree_to_ascii(node, prefix="", is_last=True, is_max=True, accumulator=None):
        """Creates a string representation of the tree."""
        if accumulator is None:
            accumulator = []

        connector = "└── " if is_last else "├── "
        label = f"({node.value})" if node.is_leaf() else ("MAX" if is_max else "MIN")
        accumulator.append(f"{prefix}{connector}{label}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            GameEngine.tree_to_ascii(child, child_prefix, is_last_child, not is_max, accumulator)

        return "\n".join(accumulator)

    @staticmethod
    def solve_alpha_beta(root_node):
        """Returns (root_value, visited_leaves_count)."""
        visited_leaves = 0

        def alpha_beta(node, alpha, beta, is_max):
            nonlocal visited_leaves
            if node.is_leaf():
                visited_leaves += 1
                return node.value

            if is_max:
                v = -math.inf
                for child in node.children:
                    v = max(v, alpha_beta(child, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha: break
                return v
            else:
                v = math.inf
                for child in node.children:
                    v = min(v, alpha_beta(child, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha: break
                return v

        val = alpha_beta(root_node, -math.inf, math.inf, True)
        return val, visited_leaves

    @staticmethod
    def generate_n_player_game(num_players=3, strategies_per_player=2):
        """
        Generează o structură de joc pentru N jucători.
        Returnează:
          - payoffs: Dict {(s1, s2, ...): (payoff1, payoff2, ...)}
          - ranges: Lista cu numărul de strategii pt fiecare jucător [2, 2, 2]
        """
        # Definim câte strategii are fiecare jucător (presupunem egal pentru simplitate)
        ranges = [range(strategies_per_player) for _ in range(num_players)]

        payoffs = {}
        # Generăm produsul cartezian al tuturor strategiilor (ex: (0,0,0), (0,0,1)...)
        all_profiles = itertools.product(*ranges)

        for profile in all_profiles:
            # Generăm payoff-uri random pentru fiecare jucător în acest profil
            payoff_tuple = tuple(random.randint(0, 9) for _ in range(num_players))
            payoffs[profile] = payoff_tuple

        return payoffs, strategies_per_player

    @staticmethod
    def format_n_player_game(payoffs, num_players):
        """Afișează jocul sub formă de listă (matricea e imposibil de desenat pt N>2)."""
        output = [f"Joc cu {num_players} jucători. Payoffs (J1, J2, ...):"]
        for profile, scores in payoffs.items():
            strat_str = ", ".join([f"S{i}" for i in profile])
            output.append(f"  Strategii [{strat_str}] -> Payoffs {scores}")
        return "\n".join(output)

    @staticmethod
    def solve_n_player_nash(payoffs, num_players, strategies_per_player):
        equilibria = []

        # Iterăm prin TOATE profilurile posibile de strategii
        all_profiles = payoffs.keys()

        for profile in all_profiles:
            is_nash = True
            current_payoffs = payoffs[profile]  # Ex: (3, 5, 1) pentru profilul (0, 1, 0)

            # Verificăm pentru FIECARE jucător 'i' dacă poate devia unilateral
            for player_idx in range(num_players):
                player_current_strategy = profile[player_idx]
                player_current_payoff = current_payoffs[player_idx]

                # Căutăm o strategie alternativă pentru acest jucător
                can_improve = False
                for alt_strat in range(strategies_per_player):
                    if alt_strat == player_current_strategy:
                        continue

                    # Construim profilul ipotetic unde doar jucătorul 'i' schimbă
                    alt_profile_list = list(profile)
                    alt_profile_list[player_idx] = alt_strat
                    alt_profile = tuple(alt_profile_list)

                    # Vedem cât ar câștiga jucătorul 'i' în noul scenariu
                    alt_payoff = payoffs[alt_profile][player_idx]

                    if alt_payoff > player_current_payoff:
                        can_improve = True
                        break  # Am găsit o mișcare mai bună, deci nu e Nash

                if can_improve:
                    is_nash = False
                    break  # Dacă un singur jucător pleacă, profilul nu e Nash

            if is_nash:
                equilibria.append(f"Profil {profile} -> Payoffs {current_payoffs}")

        return equilibria if equilibria else ["Niciun echilibru Nash pur"]