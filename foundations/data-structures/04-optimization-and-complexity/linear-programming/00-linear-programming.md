# Linear Programming

Quick reference on LP structure, standard (canonical) form, primal–dual intuition, and feasibility vs. boundedness.

## Format of a Linear Program

A complete linear program has three components:

1. **Objective function** — maximizes or minimizes a linear expression.
2. **Constraints** — linear inequalities (or equalities, depending on setup) that must hold.
3. **Non-negativity constraints** — typically one per variable: each variable is ≥ 0 (unless stated otherwise).

### Example

**Objective function:** max 2x + 3y

**Constraints:**

- x − y ≤ 5  
- x + 2y ≤ 8  
- −x + 3y ≤ 9  

**Non-negativity:** x, y ≥ 0

## Standard Form (Canonical Form)

- The objective **maximizes** the linear function (minimization can be rewritten as maximization).
- Constraints are written as **upper bounds** using ≤ (and constants on the right).
- For each constraint, the **linear expression is on the left** and the **constant is on the right**.
- **All variables** are subject to **non-negativity** (≥ 0).

## Matrix–Vector Format

LPs are often written in a **general matrix–vector** formulation. To use that formulation for the **dual** LP (especially the standard recipe for forming the dual), the **primal** should be in **standard form** as above.

## Converting Between Primal and Dual

Primal–dual conversion follows the matrix–vector setup once the primal is in standard form. A useful mnemonic from a past student: **coefficients that appear “vertically” in the primal show up “horizontally” in the dual** (and vice versa), reflecting how constraints and variables swap roles across primal and dual.

Work through a concrete small example alongside the matrix–vector formulation to lock in the pattern.

## Feasibility and Boundedness

In LP, there are a few related properties that come up repeatedly. The implications below are easier to follow if you are comfortable with **contrapositives** and careful about what “not unbounded” can mean (bounded vs infeasible).

### Feasibility

**Feasible** means a solution exists for the linear program. That can mean **exactly one** feasible solution or **infinitely many**. An LP is either feasible or not feasible — it must be one or the other.

### Bounded

**Bounded** means there is a **limit** on how much the objective can be **maximized or minimized** (depending on the problem). An LP can be bounded, unbounded, or neither — but **boundedness only makes sense when the LP is feasible**. (If there is no feasible solution, “unbounded vs bounded” is not the right question.)

### Dual bounds and unbounded primal

As a refresher: the **dual** of an LP provides an **upper bound** on the optimal value of the **original (primal)** LP (weak duality, in the usual max-primal / min-dual pairing). So if the original LP is **unbounded** in the maximization direction, there cannot be a finite upper bound from any dual feasible solution — hence the **dual LP is infeasible**:

- **If the original LP is unbounded, then the dual LP is infeasible.**

You **cannot** blindly take the contrapositive yet, because extra logical structure is involved: the **opposite of “unbounded” is not simply “bounded”** — an LP could also be **infeasible**. It only makes sense to talk about whether an LP is unbounded or not if it is **feasible**. So the precise statement is:

- **If the original LP is (feasible and) unbounded, then the dual LP is infeasible.**

That formulation is what sets up a valid **contrapositive**:

- **If the dual LP is feasible, then the original LP is either infeasible or bounded.**

### Symmetry (swap primal and dual)

Just as the dual gives an **upper** limit on the primal objective, the **original LP** also provides a **lower** limit on the objective for the **dual** LP (again in the usual paired form). So you can **swap “original” and “dual”** in these implications. For example:

- **If the dual LP is (feasible and) unbounded, then the original LP is infeasible.**
- **If the original LP is feasible, then the dual LP is either infeasible or bounded.**

From a small set of facts like these (plus contrapositives), you can derive **many** other LP properties without memorizing each one separately.

### A few more things to note

- If the **original LP is feasible and bounded**, then the **dual LP is also feasible and bounded**.
- It is **possible for both** the original LP **and** the dual LP to be **infeasible**.
- The **dual of the dual** is the **primal** LP (up to the usual rewriting conventions).

With just these basic properties and the ability to form **contrapositives**, you can recover a lot of LP facts on demand instead of memorizing long lists.
