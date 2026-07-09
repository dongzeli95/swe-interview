# ML Coding — "Implement X From Scratch"

Almost every GenAI MLE loop has one round where you must implement an ML primitive from memory, in plain Python or NumPy (no PyTorch shortcuts allowed on many teams). These are the highest-yield primitives.

## Classical ML

### 1. K-means
- Input: `X: (n, d)`, `k: int`.
- Loop: assign each point to nearest centroid; recompute centroids; stop when assignments stable OR max iters.
- Gotchas: empty cluster handling, k-means++ init, distance metric.
- Common follow-up: how would you parallelize on 100M points?

### 2. K-Nearest Neighbors (KNN)
- Brute force: `O(n·d)` per query. Discuss KD-tree, ball tree, LSH for large n.
- Weighted KNN vs uniform. Classification (majority vote) vs regression (mean).

### 3. Linear Regression
- Closed form: `θ = (XᵀX)⁻¹Xᵀy`. Complexity, numerical stability.
- Gradient descent: derive the update rule.
- Ridge (L2) and Lasso (L1) — how the penalty modifies each.

### 4. Logistic Regression
- Sigmoid + binary cross-entropy. Derive gradient.
- Multi-class: softmax + categorical cross-entropy.

### 5. Naive Bayes (Multinomial / Gaussian)
- Bag-of-words setup. Log-space to avoid underflow. Laplace smoothing.

### 6. Principal Component Analysis (PCA)
- Two ways: eigendecomposition of covariance, or SVD.
- Explain why SVD is more numerically stable.

### 7. Decision Tree (ID3 / CART)
- Impurity: Gini vs entropy. Splitting logic. When to stop (max depth, min samples).

## Neural network primitives

### 8. Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(QKᵀ / √dk) V
```
- Implement in NumPy. Show masking (causal for GPT, padding for encoder).
- Explain why we divide by √dk (variance stabilization).

### 9. Multi-Head Attention
- Wrap #8. Split `d_model` into `h` heads of dim `d_k = d_model / h`.
- Combine: concat + `Wo`.

### 10. Softmax with numerical stability
- Subtract `max(x)` before exp. Explain why (overflow avoidance).
- Log-softmax variant.

### 11. Cross-Entropy Loss + Backward
- Forward: `L = -Σ y_true · log(y_pred)`.
- Combined softmax+cross-entropy backward: gradient simplifies to `y_pred - y_true`.

### 12. LSTM cell (forward pass)
- Gates: input, forget, output, candidate. State: cell + hidden.
- Explain what problem the forget gate solves (vanishing gradient).

### 13. LayerNorm & BatchNorm
- Formulas + when to use which. Training vs eval mode difference for BN.

### 14. Dropout (train + eval)
- Inverted dropout: scale by `1/(1-p)` at train time so eval is unchanged.

## LLM-specific

### 15. Byte-Pair Encoding (BPE) tokenizer
- Step 1: initialize vocab with all bytes / chars.
- Step 2: count adjacent pair frequencies.
- Step 3: merge most frequent pair; add to merge table.
- Repeat until target vocab size.
- Encoding: apply merges in priority order.

### 16. Beam search decoding
- Maintain top-k partial hypotheses at each step. Score = sum of log-probs (or length-normalized).
- Explain vs greedy vs nucleus sampling.

### 17. Top-k / Top-p (nucleus) sampling
- Top-k: keep top k logits, renormalize.
- Nucleus: keep smallest set whose cumulative prob ≥ p.
- Combined with temperature.

### 18. RoPE (Rotary Position Embedding)
- Sketch how it works: rotate Q, K by position-dependent complex-plane rotation.
- Why it's used vs sinusoidal or learned position embeddings.

### 19. KV-cache for autoregressive inference
- What gets cached? What doesn't?
- Memory footprint: `2 · L · n_heads · d_head · seq_len` fp16 bytes per layer.
- Discuss paged attention (vLLM).

## How to prep

- Do one from each of the three sections each week during roadmap Week 10.
- Type them in a text editor, no autocomplete, no reference. 25 min budget.
- If stuck: peek, do it, then redo cold the next day.
- Common combo: interviewer asks you to implement attention, then asks "now add causal masking", then asks "what does batch dimension look like?".

## References

- Karpathy's zero-to-hero (see `resources.md` #1) — walks through most of these.
- Sebastian Raschka's LLMs from Scratch (`resources.md` #5) — book form.
- `attention-is-all-you-need-pytorch` on GitHub — clean reference implementation.
