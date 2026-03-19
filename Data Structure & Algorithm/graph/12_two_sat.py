"""
Algorithm
=====================
- Build an implication graph from the formula:
    - Each variable x gets two nodes: x (positive literal) and ¬x (negative literal)
    - Each clause (a ∨ b) is encoded as two implication edges:
        ¬a → b  (if a is false, b must be true)
        ¬b → a  (if b is false, a must be true)
- Run Kosaraju's (or Tarjan's) algorithm to find all strongly connected
  components (SCCs) in the implication graph
- If any variable x and its negation ¬x belong to the same SCC, the formula
  is unsatisfiable — return "NO"
- Otherwise, assign truth values using the topological order of the SCCs:
    - If the SCC of ¬x comes before the SCC of x in topological order,
      assign x = True; otherwise assign x = False

Correctness
=====================
The implication graph encodes every constraint: a clause (a ∨ b) is logically
equivalent to (¬a → b) ∧ (¬b → a). An SCC groups literals that are mutually
forced — if one is true, all must be. Therefore:
- If x and ¬x are in the same SCC, accepting x forces ¬x and vice versa,
  making the formula unsatisfiable
- If they are in different SCCs, topological order of the condensation DAG
  gives a consistent assignment: a literal in a later SCC "dominates" and is
  preferred as true, which never creates a contradiction because implications
  only flow forward in topological order

Runtime
=====================
O(V + E), where V = 2 * num_variables (one node per literal) and
E = 2 * num_clauses (two implication edges per clause)
- Building the implication graph is O(V + E)
- Kosaraju's / Tarjan's SCC runs in O(V + E)
- Assigning truth values by SCC order is O(V)
"""

import importlib.util, pathlib

_mod_path = pathlib.Path(__file__).parent / "04_strongly_connected_components.py"
_spec = importlib.util.spec_from_file_location("strongly_connected_components", _mod_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
strongly_connected_components = _mod.strongly_connected_components


def two_sat(num_variables, clauses):
    # Input:
    # - num_variables: number of boolean variables (1-indexed)
    # - clauses: list of 1- or 2-literal tuples using DIMACS-style integers:
    #     positive i  → variable i is True
    #     negative -i → variable i is False
    #   e.g. [(1, -2), (2,), (-1, 3)] means (x1 ∨ ¬x2) ∧ (x2) ∧ (¬x1 ∨ x3)
    #
    # Output:
    # - assignments: dict {variable: bool} if satisfiable, or "NO" if not
    # - all outputs from the run of strongly_connected_components() are also
    #   available to you

    n = num_variables

    # Node encoding: variable i (1-indexed)
    #   positive literal  i  -> node i - 1
    #   negative literal -i  -> node i - 1 + n
    def node(lit):
        return (lit - 1) if lit > 0 else (-lit - 1 + n)

    def negate(v):
        return v + n if v < n else v - n

    # Build implication graph as adjacency list {vertex: [neighbors]}
    # Clause (a ∨ b)  =>  ¬a → b  and  ¬b → a
    # Clause (a,)     =>  ¬a → a  (forces a to be true)
    graph = {v: [] for v in range(2 * n)}
    for clause in clauses:
        if len(clause) == 1:
            a = clause[0]
            graph[negate(node(a))].append(node(a))
        else:
            a, b = clause
            graph[negate(node(a))].append(node(b))
            graph[negate(node(b))].append(node(a))

    _, ccnum, _, _, _ = strongly_connected_components(graph)

    # strongly_connected_components assigns ccnum starting from 1, processing
    # sink SCCs first — so lower ccnum = topologically later (closer to sink).
    # Assign x = True if x's SCC is later (lower ccnum) than ¬x's SCC.
    assignments = {}
    for i in range(n):
        pos = i
        neg = i + n
        if ccnum[pos] == ccnum[neg]:
            return "NO"
        assignments[i + 1] = ccnum[pos] < ccnum[neg]

    return assignments


if __name__ == "__main__":
    # Test 1: Unit clause forces a variable
    # (x1) ∧ (x2) → both must be True
    result = two_sat(2, [(1,), (2,)])
    print(f"Test 1: {result} (expected x1=True, x2=True)")

    # Test 2: Classic satisfiable formula
    # (x1 ∨ x2) ∧ (¬x1 ∨ x2) → x2 must be True, x1 can be either
    result = two_sat(2, [(1, 2), (-1, 2)])
    print(f"Test 2: {result} (expected x2=True)")

    # Test 3: Unsatisfiable — direct contradiction
    # (x1) ∧ (¬x1) → impossible
    result = two_sat(1, [(1,), (-1,)])
    print(f"Test 3: {result} (expected NO)")
