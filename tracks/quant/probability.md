# Probability & Brainteasers — Quant SWE

Curated set of the highest-yield probability, expected-value, and combinatorial puzzles for quant SWE loops (Citadel, Two Sigma, Jump, Jane Street, HRT). Every entry has (1) the problem, (2) the punch line, (3) how the interviewer likely wants you to reason about it.

## Coin & Bayes

### 1. Probability of no HH in N tosses

- Model: `f(n) = f(n-1) + f(n-2)`, `f(1) = 2`, `f(2) = 3`. Answer: `f(N) / 2^N`.
- Interviewer wants: recognize Fibonacci-flavored recursion, base cases, and turn count into probability.
- Also see: [`../../company-tags/citadel/fibonacci.py`](../../company-tags/citadel/fibonacci.py).

### 2. 1000 coins, 1 defective (always heads). Flip and see 10 H. What's P(defective)?

- Bayes: `P(D|10H) = P(10H|D) · P(D) / P(10H) = (1)(1/1000) / (1/1000 + (1/2)^10 · 999/1000) ≈ 50%`.
- Follow-up: `n` such that P ≥ 99% → `n = 17`.
- Interviewer wants: clean Bayes setup, then arithmetic under pressure without a calculator.

### 3. Coin with unknown bias — how do you flip fair with it? (Von Neumann)

- Flip twice; HT → 0, TH → 1, HH/TT → retry.
- Expected number of flips: `2 / (2p(1-p))`. Ask what p makes it best (p = 0.5, expected = 4).

### 4. Fair coin from a biased one, minimum flips version

- Same construction, then discuss: what if we're not allowed to reject? Rejection sampling is necessary if you want an *exactly* fair bit.

## Dice

### 5. Expected number of rolls to see all 6 faces (coupon collector)

- `E = 6 · (1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 14.7`.

### 6. Roll two dice — probability sum is 7? Sum ≥ 10?

- 6/36 = 1/6 for sum 7. Sum ≥ 10 → (4,6),(5,5),(5,6),(6,4),(6,5),(6,6) = 6/36 = 1/6.

### 7. You roll a die until you get a 6. What's E[number of rolls] given all rolls were even?

- Trick: conditioning on "all even" changes the geometric parameter. `P(6 | even) = 1/3`. So E = 3.

## Balls, urns, permutations

### 8. Two urns, 50 red / 50 blue balls total. Distribute how to maximize P(red) when you pick urn at random then a ball?

- Put 1 red in urn A, put 49 red + 50 blue in urn B. `P = 1/2 · 1 + 1/2 · 49/99 ≈ 74.7%`.
- Classic; interviewer wants the "extreme allocation" insight.

### 9. Birthday paradox — how many people for ≥50% chance two share a birthday?

- 23. Approximate via `1 - (365 · 364 · ... · (365-n+1)) / 365^n`.

### 10. N envelopes, N letters, random assignment. E[matches]?

- E = 1 (linearity of expectation — each letter has 1/N chance).

## Random walks & martingales

### 11. Random walk on integers, +1 or -1 each step. Start at 0, absorb at N or -M. P(absorb at N)?

- Symmetric walk: `M / (N + M)`.
- Interviewer wants: martingale argument OR harmonic argument.

### 12. Gambler's ruin — same as 11.

- Common Two Sigma question. Be ready to state the answer AND the biased-coin version.

## Expected value

### 13. You draw cards from a shuffled deck one at a time. E[position of first ace]?

- Symmetric: 4 aces split 52 positions into 5 gaps of equal expected size. `E = 53/5 = 10.6`.

### 14. Uniform random `X` in `[0,1]`. E[max(X, 1-X)]? E[|X - 0.5|]?

- `E[max(X, 1-X)] = 3/4`. `E[|X - 0.5|] = 1/4`.

### 15. Draw with replacement from `[1..N]` until first repeat. E[number of draws]?

- Approximate for large N: `sqrt(π N / 2)`. Birthday paradox flavor.

## Constructive / algorithmic probability

### 16. Given coin biased to p, generate uniform in [0, 1]

- Use flips as binary expansion. See [`../../company-tags/citadel/probability.py`](../../company-tags/citadel/probability.py) for a reference implementation.

### 17. Reservoir sampling — pick one element uniformly from a stream of unknown length

- On the i-th element, replace current with probability `1/i`. Prove by induction.

### 18. Random shuffle in O(n) — Fisher-Yates

- For i in [n-1..1]: swap a[i] with a[randint(0, i)]. Prove uniformity.

## Estimation / Fermi

### 19. Estimate π

- Buffon's needle, Monte Carlo (inscribed circle). See [`../../company-tags/citadel/pi.py`](../../company-tags/citadel/pi.py).

### 20. How many M&Ms in this jar?

- Estimate volume, packing density (~74%), average M&M volume. Answer within ×2 is expected.

## Practice tips

- Say the setup out loud before touching arithmetic. Interviewers grade the framing more than the number.
- Keep a Bayes / linearity-of-expectation / martingale / symmetry decision tree in your head.
- If you can't solve it, propose a Monte Carlo sanity check. "I'd simulate this in Python to verify — here's how." That still scores.
