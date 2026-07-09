# C++ Fundamentals — Quant Interview Cheat Sheet

Extends [`../../company-tags/citadel/c++-fundamentals.md`](../../company-tags/citadel/c++-fundamentals.md) with the topics that recur in Citadel, HRT, Optiver, DRW, and Two Sigma loops. Not a language tutorial — a *what interviewers actually ask* index.

## Value categories & memory

- Copy vs move vs reference. When does the compiler elide? What is RVO / NRVO?
- Rule of 0 / 3 / 5. When you need it, when to `= default` / `= delete`.
- Small buffer optimization (SBO) — why `std::string` doesn't always heap-allocate.
- Alignment, padding, `alignas`. Cache line = 64B. False sharing.

## Undefined behavior traps

- Signed integer overflow → UB.
- Reading uninitialized memory.
- Modifying an object twice between sequence points (pre-C++11).
- Iterator invalidation after `push_back` if `vector` reallocates.
- Returning a reference to a local. Dangling references.
- Reinterpret casts violating strict aliasing.

## RAII & smart pointers

- `unique_ptr` (move-only) vs `shared_ptr` (refcount) vs `weak_ptr` (break cycles).
- Custom deleters — how to write one for a C-API resource.
- `enable_shared_from_this` — why bare `shared_ptr(this)` is a footgun.

## Templates

- Function vs class templates. Template deduction rules.
- SFINAE / `if constexpr` (C++17) / concepts (C++20).
- Variadic templates + parameter pack expansion.
- CRTP (Curiously Recurring Template Pattern) — static polymorphism, why it's used in low-latency code.

## STL nuances

- `vector<bool>` is not a container (proxy references) — don't use it.
- `unordered_map` vs `map` — hash quality matters; open addressing (`absl::flat_hash_map`) faster in cache.
- `emplace` vs `push_back` — perfect forwarding, avoids one copy.
- Custom hash: overload `std::hash` OR pass a functor to `unordered_map`.

## Concurrency

- `std::mutex` vs `std::atomic`. Memory orders: relaxed / acquire / release / seq_cst — when to use each.
- Lock-free single-producer single-consumer ring buffer — be able to sketch it.
- False sharing: pad hot atomics to 64B.
- `thread_local` — one instance per thread; when do you need it in a trading system? (per-thread order id generator).

## Compiler / performance

- What does `-O2` actually do vs `-O3`? When does `-O3` hurt?
- `__builtin_expect` / `[[likely]]` / `[[unlikely]]`.
- `__restrict__` — signals no aliasing so the compiler can vectorize.
- Profile-guided optimization (PGO), link-time optimization (LTO).
- Branch prediction basics — why a sorted `if (a[i] > 128)` loop is 3× faster than unsorted.

## Common Citadel-flavored questions

- "Explain destructor order for a class with member and base."
- "What's wrong with this code?" (given a snippet with subtle UB or lifetime bug).
- "Implement a fixed-capacity lock-free queue for SPSC."
- "Design a memory-pool allocator for fixed-size objects."
- "Given `std::vector<T> v`, why is `v[i]` faster than `v.at(i)`?" (bounds check vs no bounds check).
- "How would you find a memory leak in a running trading process?" (valgrind, jemalloc profiler, tcmalloc profiler, LD_PRELOAD interpose).

## Learning path

1. Effective Modern C++ (Meyers) — read Ch. 1–8, do the exercises mentally.
2. C++ Concurrency in Action (Williams) — Ch. 1–5 covers what quant loops actually ask.
3. cppreference.com — bookmark [std::vector](https://en.cppreference.com/w/cpp/container/vector), [std::atomic](https://en.cppreference.com/w/cpp/atomic/atomic), [std::memory_order](https://en.cppreference.com/w/cpp/atomic/memory_order).
4. Compiler Explorer (godbolt.org) — every time you claim "the compiler will optimize this", verify.
