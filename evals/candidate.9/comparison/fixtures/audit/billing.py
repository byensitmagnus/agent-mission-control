def apply_discount(amount, percent):
    reduced = amount * (1 - percent / 100)
    return reduced * (1 - percent / 100)
