# GENERATOR DE RASPUNSURI

class GeneratorRaspunsuri:
    def genereaza(self, intrebare, problema, info):
        intrebare_l = intrebare.lower()
        # normalizare simplă fără diacritice pentru potriviri robuste
        def norm(t: str) -> str:
            return (
                t.lower()
                .replace("ă","a").replace("â","a").replace("î","i")
                .replace("ș","s").replace("ţ","t").replace("ț","t")
            )
        intrebare_n = norm(intrebare)

        # identifică o strategie menționată în întrebare, dacă există
        strategie_intrebata = None
        for s in info.get("strategii", []):
            if s.lower() in intrebare_l:
                strategie_intrebata = s
                break
        if not strategie_intrebata and info.get("strategii"):
            strategie_intrebata = info["strategii"][0]

        # helper de justificare pe scurt in functie de strategie
        def justificare(s: str) -> str:
            s_l = s.lower()
            prob = problema.replace('_',' ')
            if "constraint" in s_l:
                return (
                    f"{s} este potrivita pentru {prob} deoarece reduce spatiul de cautare prin propagarea constrangerilor"
                    f" (ex. AC-3/FC) si selectia informata a variabilelor (MRV), mentinand completitudinea."
                )
            if "backtracking" in s_l:
                return (
                    f"{s} este potrivita pentru {prob} deoarece este completa si corecta; combinata cu MRV/FC/AC-3 reduce"
                    f" semnificativ ramurile explorate fata de backtracking simplu."
                )
            if "greedy" in s_l:
                return (
                    f"{s} poate fi rapida pentru {prob}, dar nu garanteaza solutii optime; e utila ca euristica sau baseline."
                )
            return f"{s} este potrivita pentru {prob} in functie de constrangeri si euristici disponibile."

        # întrebări despre alegerea celei mai bune strategii
        if "cea mai buna" in intrebare_n or "cea mai potrivita" in intrebare_n:
            s = strategie_intrebata or (info.get('strategii') or ["strategia aleasa"])[0]
            return justificare(s)

        # întrebări generice despre strategii
        if "strategie" in intrebare_n and "cum difera" not in intrebare_n and "difera" not in intrebare_n:
            strategii = ", ".join(info.get("strategii", []))
            return f"Strategiile folosite pentru {problema.replace('_',' ')} sunt: {strategii}."

        # întrebări comparative: cum diferă X de altele
        if "difera" in intrebare_n or "cum difera" in intrebare_n or "compara" in intrebare_n:
            s = strategie_intrebata or (info.get('strategii') or ["strategia aleasa"])[0]
            strategii = [x for x in info.get('strategii', []) if x.lower() != (s or "").lower()]
            alt1 = strategii[0] if strategii else "o alta strategie"
            alt2 = strategii[1] if len(strategii) > 1 else None
            opt = ", ".join(info.get("optimizari", []))
            comp = (
                f"{s} abordeaza {problema.replace('_',' ')} ca un CSP: aplica propagarea constrangerilor (ex. {opt or 'AC-3/FC'}) "
                f"si heuristici (ex. MRV) pentru a restrange domeniile inainte de explorare. "
                f"Fata de {alt1}, {s} reduce cautarea prin filtrare si mentine completitudinea; "
            )
            if alt2:
                comp += f"comparativ cu {alt2}, {s} este mai putin lacom/euristic si tinde sa ofere solutii corecte, desi toate raman exponentiale in worst-case."
            else:
                comp += f"in timp ce toate strategiile raman exponentiale in worst-case, filtrarea reduce numarul de incercari."
            return comp

        # întrebări de tip "de ce/avantaje"
        if "avantaj" in intrebare_n or "de ce" in intrebare_n:
            s = strategie_intrebata or (info.get('strategii') or ["strategia aleasa"])[0]
            return justificare(s)

        # întrebări despre asignarea variabilelor cu Backtracking + (FC/MRV/AC-3)
        if "asignarea variabilelor" in intrebare_n or ("backtracking" in intrebare_n and ("fc" in intrebare_n or "mrv" in intrebare_n or "ac-3" in intrebare_n or "ac3" in intrebare_n)):
            opt = ", ".join(info.get("optimizari", [])) or "FC/MRV/AC-3"
            return (
                f"Folosind backtracking cu {opt}, se selecteaza variabila urmatoare (ex. MRV), "
                f"se restrange domeniul cu forward checking/AC-3 si se continua daca nu apar conflicte. "
                f"Strategia de baza este backtracking, iar optimizarile (" + opt + ") reduc cautarea."
            )

        # întrebări despre optimizari
        if "optimiz" in intrebare_n:
            opts = info.get("optimizari", [])
            if not opts:
                return f"Pentru {problema.replace('_',' ')}, nu sunt specificate optimizari."

            # Dacă se cere explicit "cea mai (eficienta)", alege o singură optimizare
            if "cea mai" in intrebare_n or "mai eficienta" in intrebare_n:
                # Heuristică simplă: dacă întrebarea/strategia menționează constraint propagation, preferă AC-3 dacă există
                preferata = None
                if ("constraint propagation" in intrebare_n) and any(o.lower().startswith("ac-3") or o.lower().startswith("ac3") for o in opts):
                    preferata = next((o for o in opts if o.lower().startswith("ac-3") or o.lower().startswith("ac3")), None)
                elif ("backtracking" in intrebare_n) and any(o.lower() == "mrv" for o in opts):
                    preferata = next((o for o in opts if o.lower() == "mrv"), None)
                # Altfel, alege prima din listă ca default (ordonarea din knowledge.py reflectă o preferință)
                preferata = preferata or opts[0]

                strat = strategie_intrebata or (info.get('strategii') or [None])[0] or "strategia aleasa"
                return (
                    f"Pentru {problema.replace('_',' ')}, cea mai eficienta optimizare este {preferata}"
                    + (f" cand folosim {strat}." if strat else ".")
                )

            # Altfel, enunță lista de optimizări disponibile
            return f"Optimizari folosite pentru {problema.replace('_',' ')}: {', '.join(opts)}."

        # întrebări despre complexitate
        if "complexitate" in intrebare_n:
            return f"Complexitatea depinde de strategie. De exemplu, {info['strategii'][0]} are o complexitate mare, dar este corecta, iar local search este mai rapida dar nu garanteaza solutia."

        # game theory
        if "nash" in intrebare_n:
            return "Echilibrul Nash apare cand niciun jucator nu poate castiga mai mult schimbandu-si strategia unilateral."

        if "minmax" in intrebare_n or "alpha-beta" in intrebare_n:
            return "MinMax exploreaza toate starile posibile, iar Alpha-Beta reduce numarul de noduri evaluate prin taierea ramurilor inutile."

        # fallback generic
        return f"{info['descriere']} Se poate rezolva cu: {', '.join(info['strategii'])}."
