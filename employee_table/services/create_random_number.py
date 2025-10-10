import random


def generate_random_phone():
    return "+7" + "".join(str(random.randint(0, 9)) for _ in range(10))
