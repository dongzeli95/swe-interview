# 面经1

{% embed url="https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=831936&ctid=232499" %}

1. What's the probability of not seeing HH in N coin tosses?

Ah, now I see where you're headed. You're right. Let's think of this in terms of the Fibonacci sequence.

Let's denote by ( f(n) ) the number of sequences of length ( n ) that do not contain two consecutive heads (HH).

Consider the last coin in a sequence of ( n ) coins:

1. If the last coin is T, then the sequence is obtained by appending T to a sequence of ( n-1 ) coins that does not have HH. There are ( f(n-1) ) such sequences of length ( n-1 ).
2. If the last coin is H, then the sequence is obtained by appending TH to a sequence of ( n-2 ) coins that does not have HH (since we can't have HH). There are ( f(n-2) ) such sequences of length ( n-2 ).

This gives the recurrence relation:

f(n) = f(n-1) + f(n-2)

The base cases are:

f(1) = 2 (since for 1 coin, we can have H or T) \[ f(2) = 3 ] (since for 2 coins, we can have HT, TH, or TT but not HH)

Now, to find the probability of not seeing HH in a sequence of length ( N ) coin tosses, you would take the ratio of the number of such sequences to the total possible sequences:

P(N) = f(N) / 2^N

This will give you the desired probability.
