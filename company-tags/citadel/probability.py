import random

def flip_coin():
    return random.choice([0, 1])

def generate_probability(p):
    s = 0
    i = 1

    while True:
        flip = flip_coin()
        s += flip / (2 ** i)
        
        if s < p / (2 ** i):
            return "Loss", s
        elif s > p / (2 ** i):
            return "Win", s

        i += 1

# Example usage
p = 0.75  # Target probability
result, final_s = generate_probability(p)
print(f"Result: {result}, Final s: {final_s}")
