
```python
def fib(n):
    F = [[1, 1],
         [1, 0]]
    if (n == 0):
        return 0
    power(F, n - 1)
 
    return F[0][0]
 
 
def multiply(F, M):
    x = (F[0][0] * M[0][0] +
         F[0][1] * M[1][0])
    y = (F[0][0] * M[0][1] +
         F[0][1] * M[1][1])
    z = (F[1][0] * M[0][0] +
         F[1][1] * M[1][0])
    w = (F[1][0] * M[0][1] +
         F[1][1] * M[1][1])
 
    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w
 
# Optimized version of
# power() in method 6
 
 
def power(F, n):
    if(n == 0 or n == 1):
        return
    M = [[1, 1],
         [1, 0]]
 
    power(F, n // 2)
    multiply(F, F)
 
    if (n % 2 != 0):
        multiply(F, M)
 
 
# Driver Code
# 1 1 2 3 5 8 13 21 34 55
if __name__ == "__main__":
    n = 7
    print(fib(n))```
