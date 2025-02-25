import statistics

def get_float(range):
    if "-" in range:
        return float(statistics.mean([float(i) for i in range.split("-")]))
    elif "–" in range:
        return float(statistics.mean([float(i) for i in range.split("–")]))
    elif ">" in range:
        if "±" in range:
            return float(range.split("±")[0][1:])
        print(range[1:])
        return float(range[1:])
    elif "±" in range:
        return float(range.split("±")[0])
    else:
        return float(range)
