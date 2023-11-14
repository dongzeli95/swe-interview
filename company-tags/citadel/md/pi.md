
```python
import random

# def estimate_pi(num_samples):
#     inside_circle = 0

#     for _ in range(num_samples):
#         x, y = random.uniform(-1, 1), random.uniform(-1, 1)
#         if x**2 + y**2 <= 1:
#             inside_circle += 1

#     pi_estimate = 4 * inside_circle / num_samples
#     return pi_estimate

# # Estimate Pi using 1,000,000 samples
# pi_estimate = estimate_pi(1000000)
# print(f"Estimated Pi: {pi_estimate}")

def estimate_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x, y = random.random(), random.random()  # Random point in [0,1] x [0,1]
        distance = x**2 + y**2  # Distance from (0,0)
        if distance <= 1:  # Check if inside the quarter circle
            inside_circle += 1

    return 4 * inside_circle / num_samples  # Approximation of Pi

# Example with 1,000,000 samples
pi_estimate = estimate_pi(1000000)
print(f"Estimated Pi: {pi_estimate}")```
