def parse_total(text):
    total = 0
    for line in text.splitlines():
        total += int(line)
    return total
