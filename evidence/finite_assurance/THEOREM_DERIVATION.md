# Standalone Derivation of the q-ary RC-MDS Parity Theorem

**Date:** 2026-08-16
**Revision:** 2026-09-12 (disjoint odd obstructions)

**Status:** `PUBLIC_SELF_CONTAINED_DERIVATION`

## 0. Theorem and boundary

Let `A` be a finite nonempty alphabet with a fixed-point-free involution
`a -> bar(a)`, and let `q=|A|`. For every integer `k>=2`, the directed de
Bruijn graph `B(q,k)` has a literal reverse-complement-invariant ordinary
minimum decycling set if and only if `k` is even.

The derivation also proves:

- odd `k>=3` requires at least `q` more words than the ordinary minimum;
- the exhibited monotone even-order descent has an exact firing count;
- every injective antisymmetric real weight map gives a deterministic direct
  selector;
- for an integer weight table with a finite binary encoding, membership in
  that selector has polynomial Turing bit complexity.

The case `k=1` is excluded: every symbol is a loop, so the unique ordinary
minimum is the whole alphabet and is RC invariant.

The executable capsule checks only the binary specialization through `k=12`.
It is finite convention assurance, not a premise of this derivation.

## 1. Graph and gradient conventions

For `w=w_0...w_(k-1)`, let

```text
RC(w)_i = bar(w_(k-1-i)),
R(w_0...w_(k-1)) = w_1...w_(k-1)w_0.
```

The word `w` is the lower-state arc

```text
t(w)=w_0...w_(k-2) -> h(w)=w_1...w_(k-1)
```

of `B(q,k-1)`. Reverse complement reverses this arc. The gradient convention
is

```text
(nabla f)(w)=f(t(w))-f(h(w)).
```

A PCR is a set of distinct rotations. PCRs partition `A^k`, and every PCR is
a directed cycle. Their number is

```text
N_q(k)=(1/k) sum_(d|k) phi(d) q^(k/d).
```

The ordinary minimum cardinality equals `N_q(k)`. Thus an ordinary MDS
contains exactly one distinct word from every PCR, although an arbitrary
one-per-PCR transversal need not be decycling.

For a lower word `u`, define the full companion sets

```text
L(u)={a u:a in A},  R(u)={u a:a in A}.
```

If `L(u)` lies in an ordinary MDS `M`, the valid full-alphabet F-move replaces
`L(u)` by `R(u)`. Before the move the residual lower graph has no arc entering
`u`; afterward it has no arc leaving `u`. A newly created cycle would have to
enter `u` on a restored arc and leave on a deleted one, which is impossible.
If a newly inserted outgoing companion other than the common loop had already
been selected, the result would be a smaller decycling set, contradicting
minimality. Thus the move preserves ordinary-MDS status. Its indicator update
is `nabla 1_u`. The common homopolymer loop is removed and reinserted, while
the gradient on it is zero.

## 2. Weighted cyclotomic coordinates

Assume `k>=4` is even. Choose an injective map

```text
s:A -> R\{0},  s(bar(a))=-s(a).
```

Such weights always exist. For DNA in the order `(A,C,G,T)`, use
`(-2,-1,1,2)`. Put `zeta=exp(2*pi*i/k)` and define

```text
P_s(w)=sum_(j=0)^(k-1) s(w_j) zeta^(j+1),
W_s(w)=sum_(j=0)^(k-1) s(w_j),
lambda_s(u)=sum_(j=0)^(k-2) s(u_j) sin(2*pi*(j+1)/k),
chi(u)=1[lambda_s(u)>0].
```

Reindexing gives

```text
P_s(Rw)=zeta^(-1)P_s(w),
P_s(RC w)=-conj(P_s(Rw)),
P_s(R RC w)=-conj(P_s(w)).
```

Also

```text
Im P_s(w)=lambda_s(t(w)),
Im P_s(Rw)=lambda_s(h(w)),
lambda_s(RC u)=lambda_s(u).
```

Only real linearity and antisymmetry of the weights are used in the RC
identities; raw alphabet codes are not interchangeable with `s`.  The
existence argument does not require the weights to be integral.

## 3. The geometric seed

On every PCR with nonzero embedding select exactly one word:

1. the negative-real-axis point, if it exists;
2. otherwise the unique `w` with `Im P_s(w)<0<Im P_s(Rw)`.

On a zero-embedding PCR choose one representative temporarily. Call the
one-per-PCR set `M_0` and its indicator `m_0`.

If a nonzero PCR had minimal period `d<k`, then

```text
P_s(R^d w)=zeta^(-d)P_s(w)=P_s(w)
```

would force `P_s(w)=0`. Every nonzero PCR therefore has full period and is a
nondegenerate regular `k`-gon. At even `k`, the negative ray or strict
lower-to-upper rule selects exactly one vertex.

## 4. Arbitrary zero ties preserve acyclicity

Define `Q_s=P_s-W_s`. If

```text
w=w_0...w_(k-1),  y=w_1...w_(k-1)a,
delta=s(a)-s(w_0),
```

then

```text
P_s(y)=zeta^(-1)P_s(w)+delta,
W_s(y)=W_s(w)+delta,
Q_s(y)=-W_s(w)+zeta^(-1)P_s(w).
```

A residual path cannot move from `Im P_s<=0` to `Im P_s>0`: the strict
crossing and departure from the negative ray are selected. A residual cycle
must stay in the open upper or closed lower half-plane.

Write `alpha=2*pi/k` and `P_s(w)=rho exp(i*phi) != 0`. Along an edge remaining
in the open upper half-plane,

```text
Re Q_s(y)-Re Q_s(w)
 = 2 rho sin(alpha/2) sin(phi-alpha/2) > 0.
```

Along a residual edge remaining in the closed lower half-plane, the same
quantity is strictly negative. Consequently a residual cycle could contain
only zero-embedding edges.

If consecutive labels `w,y` both have zero embedding, then
`P_s(y)=s(a)-s(w_0)=0`. Injectivity of `s` forces `a=w_0`; this is a pure
rotation. A zero-only residual cycle is therefore a zero PCR, but one of its
words was selected. Contradiction. Hence every choice of zero-PCR
representatives makes `M_0` an ordinary MDS.

## 5. RC-equivariant zero ties

RC permutes zero PCRs. For a paired orbit `{C,RC(C)}`, choose `w in C` and
`RC(w)` in its mate.

For a stable PCR of minimal period `d`, choose `w` with `RC(w)=R^s w`. In
cyclic position notation,

```text
w_r=bar(w_(s-1-r)).
```

The involution `r -> s-1-r` has no fixed point. If `d` were odd, it would
have one, so `d` is even. For even `d`, absence of a fixed position forces
`s` even. An RC-fixed rotation `R^i w` satisfies `2i=s mod d`, which has
exactly two solutions. Choosing either one makes the stable PCR tie invariant.

Thus all zero ties can be chosen RC-equivariantly without affecting the MDS
property.

## 6. Exact seed defect

For a word `w`, set

```text
A=Im P_s(w),  B=Im P_s(Rw).
```

The ordered imaginary coordinates for `RC(w)` are `(B,A)`. Away from the
rays,

```text
m_0(RC w)-m_0(w)
 = 1[B<0<A]-1[A<0<B]
 = 1[A>0]-1[B>0].
```

The negative-ray convention gives the same identity when one coordinate is
zero. In the zero sector, both sides vanish by the equivariant tie. Therefore

```text
m_0(RC w)-m_0(w)
 = chi(t(w))-chi(h(w))
 = (nabla chi)(w).                         (6.1)
```

## 7. Positive-potential firing

Let `A` and `N` be ordinary MDSs with

```text
1_N-1_A=nabla f,  f>=0,  min f=0.
```

If `A!=N`, some positive lower state admits a valid full-alphabet F-move.
Otherwise every positive state has an incoming residual nonloop arc
`v->u`. On such an arc,

```text
1_N(v->u)=f(v)-f(u) in {0,1},
```

so `f(v)>=f(u)>0`. Iterating predecessors in the finite positive support
creates a residual directed cycle, contradicting that `A` is decycling.

## 8. Paired defect update and exact move count

Suppose

```text
1_RC(A)-1_A=nabla f,
f>=0, min f=0, f(RC u)=f(u).
```

Fire one enabled positive state `u`. Since RC reverses lower arcs, the new
defect potential is

```text
f'=f-1_u-1_(RC u).
```

The lower length `k-1` is odd, so `u!=RC(u)`. Both decremented coordinates
are positive. The new potential is again integral, nonnegative, symmetric,
and minimum-zero, while `sum f'=sum f-2`.

For the seed, `f=chi`. Every homopolymer lower word has `lambda_s=0`, so the
minimum is zero. Repeated legal firings terminate. At an RC-fixed terminal,
`nabla f=0`; strong connectedness of the lower de Bruijn graph makes `f`
constant, and its minimum makes that constant zero. Thus every monotone
scheduler described above uses exactly

```text
(1/2)|{u in A^(k-1):lambda_s(u)>0}|
```

physical F-moves. This proves even-order existence for `k>=4`, without
asserting uniqueness, confluence, or shortest distance.

## 9. A direct spectral ideal

Fix a total alphabet order and its lexicographic word order. Let
`theta(u)=RC(u)` and define

```text
psi_s(u)=sum_(j=0)^(k-2) s(u_j)(zeta^(j+1)-1),
r_s(u)=Re psi_s(u),
U={u:lambda_s(u)>0}.
```

The last coefficient in `P_s(ua)-W_s(ua)` is zero, so `psi_s` depends only
on `u`. Reindexing gives

```text
psi_s(theta u)=-conj(psi_s(u)),
lambda_s(theta u)=lambda_s(u),
r_s(theta u)=-r_s(u).
```

Define

```text
a_star(u)=1 iff u in U and
  [r_s(u)<0 or (r_s(u)=0 and u<theta(u))].
```

On an edge `w:u->v` internal to `U`, both consecutive imaginary coordinates
are positive, so the seed does not select the edge. Moreover

```text
psi_s(v)-psi_s(u)=(zeta^(-1)-1)P_s(w).
```

If `P_s(w)=rho exp(i*phi)` and `alpha=2*pi/k`, then
`alpha<phi<pi` and

```text
r_s(v)-r_s(u)
 = 2 rho sin(alpha/2) sin(phi-alpha/2) > 0.       (9.1)
```

Therefore `{u:a_star(u)=1}` is an order ideal. Equation (9.1) also forbids
edges between zero-level states, so independent lexicographic choices at
zero are safe. Since lower RC has no fixed point,

```text
a_star(u)+a_star(theta u)=chi(u).                 (9.2)
```

Fire this ideal in predecessor-first order. An incoming edge already selected
by the seed needs no action. Every other incoming edge is residual. Such an
edge cannot come from outside `U`, because (6.1) and Booleanity would force it
to be seed-selected; if it comes from inside `U`, it was selected by an
earlier ideal firing. Every move is legal. Hence

```text
m_star(w)=m_0(w)+a_star(t(w))-a_star(h(w))         (9.3)
```

is a `0`-`1` MDS indicator. Combining (6.1) and (9.2) gives
`m_star(RC w)=m_star(w)`. Formula (9.3) is a deterministic direct selector,
not a simulated firing scheduler.

No integrality of `s` was used in Sections 2--9. Covariance uses real
linearity and complex conjugation; the zero-sector argument uses
injectivity; the defect potential is the Boolean indicator `chi`; and the
ideal construction uses exact comparisons of real values. Thus every
injective nonzero real map with `s(bar(a))=-s(a)` supplies the seed, legal
descent, and direct RC-invariant ordinary MDS.

## 10. Exact polynomial-bit membership

For this algorithmic statement, now specialize `s` to an integer-valued
weight map supplied in binary. No effective computation claim is made here
for an arbitrary real table without a finite exact representation.

Put

```text
c=2*cos(2*pi/k), d=phi(k)/2, B=max_a |s(a)|.
```

Let `Psi_k` be the monic minimal polynomial of `c`. It is obtained from

```text
Phi_k(z)=z^d Psi_k(z+z^(-1)).
```

The value `c` is the largest real conjugate, which canonically identifies
the root of `Psi_k` used by the sign oracle.

Define integer recurrences

```text
C_0=2, C_1=x, C_(j+1)=x C_j-C_(j-1),
S_0=0, S_1=1, S_(j+1)=x S_j-S_(j-1).
```

At `x=c`, `C_j(c)=2cos(2*pi*j/k)` and
`S_j(c)=sin(2*pi*j/k)/sin(2*pi/k)`. Exact real and imaginary signs of
`P_s`, `lambda_s`, and `r_s` are integer-polynomial signs at `c`. Reduce the
polynomials modulo `Psi_k`; zero is then literal polynomial zero.

For every nonzero reduced polynomial `g`, all conjugates satisfy the safe
bound

```text
|g(c_i)| <= M=2 B k(k+1).
```

Since `g(c)` is a nonzero algebraic integer, its norm is a nonzero integer,
so

```text
|g(c)| >= M^(-(d-1)).
```

Certified root isolation and interval refinement below half this gap decide
the sign with polynomially many bits. The cyclotomic construction,
recurrences, reduction, and standard Sturm-Habicht sign algorithms all have
bit complexity polynomial in `k`, `q`, and the weight-table bit length.

For a queried word, determine seed membership by exact signs. In the
zero-PCR branch inspect at most `k` rotations and their RC mates under a
fixed deterministic tie. Evaluate `a_star` at the tail and head and return
(9.3). No table of size `q^(k-1)` or `q^k` is stored.

## 11. The base case `k=2`

Choose representatives `a_i` of the complement pairs and impose

```text
a_1<...<a_(q/2)<bar(a_(q/2))<...<bar(a_1).
```

Delete `xy` iff `y<=x`. Residual arcs are strictly increasing, so the
residual is a DAG. Complement reverses the order, making the deletion set RC
invariant. It contains all loops and one orientation of every unordered pair:

```text
q+q(q-1)/2=q(q+1)/2=N_q(2).
```

## 12. Odd orders

Let `k=2m+1>=3` and choose a complement pair `{a,bar(a)}`. The lower words

```text
f_m=(a bar(a))^m,  g_m=(bar(a) a)^m
```

are RC fixed. The primitive word

```text
w_m=(a bar(a))^m bar(a)
```

has a PCR containing a direct arc `g_m->f_m` and a path through all other PCR
arcs from `f_m` to `g_m`. One selected word cannot destroy both directions.
If the selected set were RC invariant, RC would supply a surviving return
path, hence a residual cycle.

Write `C_a` for this PCR. Every decycling set meets it, and the preceding
argument applies whenever an invariant set selects exactly one word from it,
regardless of the set's total size. Hence it selects at least two words from
`C_a` and, by symmetry, from `RC(C_a)`. These PCRs are distinct because the
counts of `a` and `bar(a)` are interchanged. Distinct complementary alphabet
pairs use disjoint letters, so their distinguished PCRs are all distinct.
There are q such PCRs, each requiring two words, while all other PCRs require
at least one. Thus

```text
|M| >= 2q + (N_q(k)-q) = N_q(k)+q.
```

This lower bound does not determine the exact odd premium.

## 13. Assembly and DNA

Sections 8 and 11 prove even-order existence for every `k>=2`; at
`k>=4`, every admissible real weight map gives such a construction.
Section 12
proves odd-order nonexistence at ordinary minimum cardinality. Therefore the
parity theorem holds for every finite fixed-point-free complemented alphabet.

For DNA with `A<->T` and `C<->G`, an RC-invariant ordinary MDS exists exactly
at even `k` and has cardinality `N_4(k)`. The weights `(-2,-1,1,2)` give one
explicit construction.
At odd `k>=3`, the same disjoint-obstruction count gives at least `N_4(k)+4`
selected words.

## 14. Nonclaims

This derivation does not prove an exact odd premium, a unique terminal,
shortest firing distance, longest residual path, window guarantee, biological
performance, polynomial total time to list an exponentially large set, or a
polynomial-bit algorithm for an unrepresented arbitrary real weight table.
It makes no blanket novelty or priority assertion.
