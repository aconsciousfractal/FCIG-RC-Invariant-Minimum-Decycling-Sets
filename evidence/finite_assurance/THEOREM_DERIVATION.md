# Standalone Derivation of the Mykkeltveit Half-Plane Coboundary Theorem

**Date:** 2026-08-12

**Status:** `PROVED_SELF_CONTAINED`

## 0. Decision and scope

This document gives a self-contained all-order construction of an
RC-invariant ordinary binary minimum decycling set at every even order.  Its
load-bearing step is the exact half-plane coboundary identity

```text
1_RC(M) - 1_M = nabla chi.
```

Here `M` is a tie-symmetrized Mykkeltveit selector and `chi` is the indicator
of the open upper half-plane for the lower-word cyclotomic embedding.  The
identity supplies an integral, nonnegative defect potential.  The
positive-potential firing lemma then gives a finite legal F-move path to an
RC-fixed ordinary MDS.

In particular, the fact that the
Mykkeltveit selector remains an MDS under arbitrary choices on zero-embedding
PCRs is reproved here.  Finite witnesses and executable checks are regression
evidence only.

## 1. Frozen normalization

Let `k>=4` be even and put

```text
zeta = exp(2*pi*i/k).
```

For a binary word `w=x_0...x_(k-1)`, define

```text
P(w) = sum_(j=0)^(k-1) x_j zeta^(j+1),
W(w) = sum_(j=0)^(k-1) x_j.
```

Let `R` be left rotation and let `tau_k` be reverse complement:

```text
R(x_0...x_(k-1)) = x_1...x_(k-1)x_0,
tau_k(w)_j = 1-x_(k-1-j).
```

The length-`k` word `w` is also the labelled arc

```text
t(w)=x_0...x_(k-2)  ->  h(w)=x_1...x_(k-1)
```

of the lower de Bruijn graph `D=B(2,k-1)`.  On a lower word
`u=u_0...u_(k-2)`, define

```text
lambda(u) = sum_(j=0)^(k-2) u_j sin(2*pi*(j+1)/k),
chi(u) = 1 if lambda(u)>0, and 0 otherwise.
```

The gradient convention is

```text
(nabla q)(w) = q(t(w))-q(h(w)).
```

PCRs are sets of distinct rotations, so imprimitive words are never unfolded
into repeated labelled occurrences.  The two homopolymer PCRs are singleton
loops and remain mandatory selected words.

The case `k=2` is handled separately in Section 9.

## 2. Geometric covariance

### Lemma 2.1 - rotation and reverse complement

For every length-`k` word `w`,

```text
P(Rw)             = zeta^(-1) P(w),
P(tau_k w)        = -conj(P(Rw)),
P(R tau_k w)      = -conj(P(w)).
```

#### Proof

The first equality follows by reindexing and using `zeta^k=1`.  For the
second,

```text
P(tau_k w)
 = sum_i (1-x_(k-1-i)) zeta^(i+1)
 = -sum_j x_j zeta^(-j)
 = -conj(P(Rw)),
```

because the sum of all `k`-th roots of unity is zero.  Rotate once to obtain
the third equality.  QED.

### Lemma 2.2 - lower coordinates and lower RC symmetry

For every length-`k` word `w`,

```text
Im P(w)  = lambda(t(w)),
Im P(Rw) = lambda(h(w)).
```

For every lower word `u`,

```text
lambda(tau_(k-1) u) = lambda(u),
chi(tau_(k-1) u) = chi(u).
```

#### Proof

The bit omitted from `t(w)` multiplies `zeta^k=1` and hence contributes no
imaginary part.  The second displayed identity follows by applying the first
one to `Rw`.

For lower RC, reindex and use

```text
sin(2*pi*(k-r)/k) = -sin(2*pi*r/k)
```

together with the vanishing sum of the `k-1` nontrivial sine coordinates.
The strict-sign indicator is therefore invariant.  QED.

## 3. The geometric selector

On every PCR with nonzero embedding choose exactly one word as follows:

1. choose the point on the negative real axis, if it exists;
2. otherwise choose the unique `w` satisfying

   ```text
   Im P(w)<0<Im P(Rw).
   ```

On a PCR on which `P` is identically zero, temporarily choose an arbitrary
representative.

Call the resulting set `M`.

If a nonzero PCR had minimal period `d<k`, then

```text
P(R^d w)=zeta^(-d)P(w)=P(w)
```

would force `P(w)=0`.  Thus every nonzero PCR has full period `k`, and its
embedded rotations are the vertices of a nondegenerate regular `k`-gon.
The stated negative-axis/lower-to-upper rule is therefore unique.  By
construction, `M` contains exactly one word in every PCR.

## 4. The seed is an ordinary MDS for arbitrary zero ties

### Theorem 4.1 - tie-independent seed acyclicity

For every choice of representatives on the zero-embedding PCRs, the set `M`
of Section 3 is an ordinary MDS.

#### Proof

Define the auxiliary complex coordinate

```text
Q(w)=P(w)-W(w).
```

If `y=x_1...x_(k-1)a` is a successor of `w` in the lower graph and
`delta=a-x_0`, then

```text
P(y)=zeta^(-1)P(w)+delta,
W(y)=W(w)+delta,
Q(y)=-W(w)+zeta^(-1)P(w).
```

Thus `Q(y)` is obtained by rotating `Q(w)` clockwise through `2*pi/k`
around the real centre `-W(w)`.

Consider a directed path using only residual arcs, that is, words outside
`M`.

First, the path cannot move from `Im P<=0` to `Im P>0`.  A strict
lower-to-upper crossing is selected by rule 2.  A departure from the negative
real axis is selected by rule 1.  From the positive real axis the clockwise
rotation enters the lower half-plane, and from the origin the next imaginary
coordinate is zero.

Consequently a residual directed cycle would lie entirely in one of the two
regions `Im P>0` or `Im P<=0`.

Put `theta=2*pi/k` and write a nonzero `P(w)=rho exp(i*phi)`.  Along an edge
whose two endpoints remain in the open upper half-plane, one has
`theta<phi<pi`, and therefore

```text
Re Q(y)-Re Q(w)
 = 2*rho*sin(theta/2)*sin(phi-theta/2) > 0.
```

Hence no residual cycle lies in the upper half-plane.

Along an edge whose two endpoints remain in the closed lower half-plane,
the same formula is strictly negative whenever `P(w)` is nonzero: a
residual starting point on the negative ray is excluded by rule 1, while
remaining in the lower region forces `pi+theta<=phi<=2*pi`.  Equality is
therefore possible only when `P(w)=0`.  On a cycle every step must be an
equality.  Hence every starting word on the cycle has `P(w)=0`.  For a
successor `y`, the relation `P(y)=a-x_0` then forces `a=x_0`, because `y` is
also a zero-embedding word.  Every edge of the alleged cycle is therefore a
pure rotation.  The cycle is a zero-embedding PCR, but `M` contains one of
its words.  This contradicts residuality.

The residual lower graph is a DAG.  Through the frozen line-graph
correspondence, `B(2,k)\M` is a DAG as well.  Since every decycling set must
meet every PCR and `M` meets each exactly once, `M` has minimum cardinality.
QED.

## 5. RC-equivariant zero ties

The family of zero-embedding PCRs is stable under `tau_k` by Lemma 2.1.
Partition that family into its orbits under RC.

For a paired orbit `{C,tau_k C}`, choose any `w in C` and choose `tau_k w`
in the mate.  The stable case is supplied by the following elementary lemma.

### Lemma 5.1 - fixed words in a stable PCR

Let `C` be an RC-stable binary PCR at even length `k`, and let `d` be its
minimal period.  Then `d` is even and `C` contains exactly two RC-fixed
words.

#### Proof

Choose `w in C` and `s modulo d` such that

```text
tau_k(w)=R^s w.
```

Because the period word is carried to its bitwise complement, stability pairs
its zeros and ones; hence `d` is even.  With cyclic positions indexed modulo
`d`, the identity above reads

```text
w_r = complement(w_(s-1-r)).
```

The positional involution `r -> s-1-r` cannot have a fixed point, since a
fixed position would force a bit to equal its complement.  For even `d`, the
congruence

```text
2r = s-1  (mod d)
```

has a solution exactly when `s` is odd.  Therefore `s` is even.

A rotation `R^i w` is RC fixed precisely when

```text
tau_k(R^i w)=R^(-i)tau_k(w)=R^(s-i)w=R^i w,
```

or equivalently when `2i=s (mod d)`.  Since both `d` and `s` are even, this
congruence has exactly `gcd(2,d)=2` solutions modulo `d`.  QED.

For an RC-stable PCR, choose either of the two fixed words from Lemma 5.1.

This produces an RC-invariant set of zero-sector representatives.  Theorem
4.1 shows that imposing these ties does not change ordinary-MDS status.

## 6. The half-plane coboundary

Let `m=1_M` for the tie-symmetrized selector of Section 5.

### Theorem 6.1 - exact RC defect

For every length-`k` word `w`,

```text
m(tau_k w)-m(w)
  = chi(t(w))-chi(h(w))
  = (nabla chi)(w).
```

Equivalently,

```text
1_RC(M)-1_M = nabla chi.                         (6.1)
```

#### Proof

Put

```text
A=Im P(w),
B=Im P(Rw).
```

For `tau_k w`, Lemma 2.1 exchanges the ordered imaginary coordinates to
`(B,A)`.

If `A` and `B` are both nonzero, the selector rule gives

```text
m(tau_k w)-m(w)
 = 1[B<0<A]-1[A<0<B]
 = 1[A>0]-1[B>0].
```

If `A=0`, write `P(w)=r` real.  Then

```text
B=-r sin(2*pi/k).
```

For `r<0`, both sides equal `-1`; for `r>0`, both sides equal zero.

If `B=0`, write `P(Rw)=r` real.  For `r>0`, both sides equal `+1`; for
`r<0`, both sides equal zero.

For `k>2`, the case `A=B=0` with nonzero `P(w)` is impossible, because
`P(Rw)=zeta^(-1)P(w)` and `zeta` is not real.  On the zero sector the chosen
tie set is RC-invariant, so the left side is zero; both lower coordinates
also have zero imaginary part, so the right side is zero.

Lemma 2.2 identifies `1[A>0]-1[B>0]` with
`chi(t(w))-chi(h(w))`.  QED.

### Corollary 6.2 - integral defect representation

Equation (6.1) represents the literal indicator difference between `M` and
`RC(M)` as the integral gradient of the nonnegative binary potential `chi`.
The direct legal realization in Section 7 uses this identity without invoking
any separate component, quotient or connectivity theorem.

## 7. Legal realization of the coboundary

The direct realization below makes the even construction independent of any
separate component criterion.

### Lemma 7.1 - positive-potential firing

Let `A,N` be ordinary MDSs and suppose

```text
1_N-1_A = nabla q
```

for an integral potential `q>=0` with minimum zero.  If `A!=N`, some lower
state `u` with `q(u)>0` admits a legal F-move from `A`.

#### Proof

Assume otherwise.  At every positive state `u`, disabledness supplies an
incoming nonloop residual arc `v->u`; otherwise all incoming companions are
selected and the frozen F-move is legal.  On that residual arc,

```text
1_N(v->u)=q(v)-q(u) in {0,1},
```

so `q(v)>=q(u)>0`.  Repeating this predecessor choice in the finite positive
state set creates a directed cycle made entirely of arcs outside `A`,
contradicting that `A` is a decycling set.  QED.

The valid-source-move preservation theorem of
Marçais--DeBlasio--Kingsford (Section 4.1, Proposition 2) guarantees that a
legal F-move preserves ordinary-MDS status.  Its indicator change is
`nabla 1_u` under the convention above.

### Lemma 7.2 - paired defect descent

Let the current ordinary MDS be `A` and suppose

```text
1_RC(A)-1_A = nabla q,
```

where `q>=0` and `q o tau_(k-1)=q`.  If `A` is not RC-fixed, choose an
enabled positive state `u` from Lemma 7.1 and fire it.  Then the new MDS `A'`
satisfies

```text
1_RC(A')-1_A'
 = nabla(q-1_u-1_(tau_(k-1)u)).                    (7.1)
```

#### Proof

RC reverses lower arcs, hence

```text
RC(nabla 1_u)=-nabla 1_(tau_(k-1)u).
```

Subtract the indicator update of `A` from its RC image to obtain (7.1).
By Lemma 2.2, positivity occurs in lower RC pairs.  Since `k-1` is odd,
`tau_(k-1)` has no fixed word, so the two subtracted coordinates are
distinct.  The new potential remains nonnegative and RC-invariant.  A
previously zero coordinate is untouched, so the minimum remains zero.  QED.

## 8. Even existence theorem

### Theorem 8.1

For every even `k>=4`, there exists an RC-invariant ordinary binary MDS in
`B(2,k)`.

#### Proof

Start from the tie-symmetrized ordinary MDS `M` of Sections 3--5.  Theorem
6.1 gives its nonnegative binary RC-invariant defect potential `chi`.

If `M` is not fixed, apply Lemmas 7.1 and 7.2.  Every firing preserves
ordinary-MDS status, preserves a nonnegative RC-invariant defect potential,
preserves its minimum-zero normalization, and lowers its coordinate sum by
two.  The process is finite.  It cannot stop at a non-RC-fixed set, because
Lemma 7.1 would then supply another enabled positive firing with
`N=RC(A)`.

For completeness, the potential itself also closes exactly.  At a terminal
RC-fixed set the indicator defect is zero, so `nabla q=0`.  The underlying
lower binary de Bruijn graph is connected (indeed, appending the letters of
any target lower word gives a directed walk to it), and therefore `q` is
constant.  Its preserved minimum is zero, so `q=0`.  Thus the terminal
ordinary MDS is literally RC fixed.  QED.

## 9. The case k=2 and the parity iff corollary

For `k=2`,

```text
{00,01,11}
```

is an RC-invariant ordinary MDS.  Together with Theorem 8.1 this proves even
existence for every `k>=2`.

The companion manuscript proves directly that, for every fixed-point-free
complement alphabet and every odd `k>=3`, every RC-invariant decycling set has
cardinality strictly larger than the PCR count.  Its proof uses one primitive
rotation cycle with two reverse-complement-fixed lower endpoints and then the
free reverse-complement action on odd PCRs.  Specializing to the binary
alphabet and composing with the even theorem gives:

> For binary `k>=2`, an RC-invariant ordinary MDS exists if and only if `k`
> is even.

## 10. Source and assurance boundary

The only imported mathematical facts are:

1. the ordinary necklace-count minimum and classical constructions of
   Mykkeltveit and Champarnaud--Hansel--Perrin;
2. valid source-move preservation from
   Marçais--DeBlasio--Kingsford, Section 4.1, Proposition 2.

The manuscript proves the odd obstruction, the zero-tie seed theorem, the
half-plane coboundary and the terminating legal descent. The executable finite
panel reconstructs the declared orders through `k=12` by two separate methods
and rejects explicit convention and envelope mutations. It is assurance for
this derivation, not a premise of an all-order quantifier.

## Claim boundary

Established in this derivation and the companion manuscript:

- the tie-independent Mykkeltveit seed proof;
- the RC-equivariant zero-sector tie;
- the exact half-plane coboundary identity;
- the legal paired-potential descent;
- the all-even existence theorem and its composition with the independently
  proved odd obstruction.

Not admitted:

- novelty, priority or literature exhaustion;
- DNA/alphabet-general even existence;
- a new odd-premium formula;
- algorithmic optimality or complexity improvement;
- biological utility or empirical sketching performance.

## Disposition

This derivation is shipped as readable provenance behind the paper.  The paper
is the reader-facing theorem authority; the finite-assurance protocol and its
two implementations are convention-level falsification controls only.
