# Exact Binary-Specialization Validation Protocol

**Date:** 2026-08-12
**Mathematical-input revision:** 2026-09-12
**Status:** `EXECUTED_AND_CROSS_VALIDATED`

## 1. Purpose and boundary

This protocol tests, on the binary specialization, convention-sensitive
identities used by the alphabet-general proof.  It is finite assurance, not
an enumerative proof of an all-order or q-ary theorem.  The producer and
independent validator use no stored MDS
witness, floating-point trigonometry, SAT/SMT/MILP solver, randomness, network
request, external computational service, or closure oracle. The validator does
not import the producer.

The mathematical input is:

```text
THEOREM_DERIVATION.md
SHA-256 5f64d0091aa0d1b28273f5faa0496191f6f791ee86e8cac83264129081f0a3e1
```

The August revision widened the proof-level weight domain from integers to
reals. The September revision counts the odd obstruction separately over
complementary alphabet pairs, giving a lower bound q on the odd premium.
Neither change alters this binary even-order panel or its scientific payload.

## 2. Exact panel

The tested even orders are `k = 2,4,6,8,10,12`.  The `k=2` row reconstructs
`{00,01,11}` explicitly.  For `k>=4`, every cyclotomic sign and zero test is
exact.  The producer works in `Z[alpha]`, where
`alpha=2*cos(2*pi/k)`, using

```text
S_0=0, S_1=1, S_(j+1)=alpha*S_j-S_(j-1),
C_0=2, C_1=alpha, C_(j+1)=alpha*C_j-C_(j-1).
```

The independent validator instead uses literal hard-coded exact coordinate
tables for the five nontrivial orders and a separate DFS acyclicity oracle.

## 3. Deterministic reconstruction

Words are MSB-first.  `R` is left rotation, `RC` is reverse complement,
`t(w)` is the length-`k-1` prefix, and `h(w)` the suffix.  PCRs are sets of
distinct rotations ordered by their least integer word.

At every nonzero PCR, select the unique word `w` satisfying either

```text
Im P(w)=0 < Im P(Rw)
```

or

```text
Im P(w)<0<Im P(Rw).
```

On zero PCRs, use the following RC-equivariant tie:

1. in a paired PCR orbit, select the least word in the lower-index PCR and
   its literal reverse complement in the mate;
2. in an RC-stable zero PCR, reconstruct the exactly two RC-fixed words and
   select the lesser one.

For every tested order, record the PCR count, selected-word digest, zero-tie
census, residual-DAG status, exact lower-state potential, the identity

```text
1_RC(M)(w)-1_M(w)=chi(t(w))-chi(h(w)),
```

and the complete legal firing path to a literal RC-fixed ordinary MDS.

## 4. Legal firing path

For `k>=4`, initialize the remaining support to all lower states with
`chi=1`.  Repeatedly choose the least supported lower state whose two incoming
companion arcs are selected, perform the valid source move, and delete both
`u` and `RC(u)` from the remaining support.  After every step independently
check source enablement, one-per-PCR, residual acyclicity, nonnegative
RC-invariant potential, and the current edgewise gradient identity.  The path
must end with empty potential and a literal RC-fixed MDS.

## 5. Scientific falsification controls

Each mutation is actually applied and must be rejected by a named scientific
predicate, with the first failing order recorded:

1. right-rotation selector;
2. reversed gradient sign;
3. closed rather than open half-plane;
4. positive-axis convention;
5. broken zero-sector RC pairing;
6. unpaired defect update;
7. reversed source move.

## 6. Independent validation

The validator authenticates the two input files, parses the producer envelope,
reconstructs the complete scientific payload without producer imports,
requires canonical payload identity, and applies seven end-to-end envelope
mutations to an order row, selected word, zero tie, path step, mutation verdict,
outcome, and claim boundary.

## 7. Decision rule

- `PASS_EXACT_PARITY_CONVENTION_MAP_K2_TO_K12`: every baseline obligation
  passes, all seven scientific mutations are rejected, both implementations
  agree exactly, and all seven envelope mutations are rejected.
- `FAIL_LITERAL_PARITY_CONVENTION_OR_PATH`: a baseline identity, legal path,
  terminal invariant, or required mutation rejection fails.
- `INCONCLUSIVE_INPUT_ARITHMETIC_OR_RECONSTRUCTION_GAP`: an input, exact
  arithmetic, schema, or independent-reconstruction gap prevents a literal
  verdict.

A PASS certifies only the binary convention map through `k=12`.  The q-ary
all-order theorem and direct membership result remain deductive and
proof-based.  No novelty, priority, biological, performance, or software
claim follows from this protocol.
