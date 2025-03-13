import statistics

def is_active(mic, mic_threshold):
    if ">" in mic:
        return False
    mic_value = get_float(mic)
    if mic_value >= mic_threshold:
        return False
    else:
        return True

def get_float(range):
    if "-" in range:
        if ">" in range:
            return float(range.split(">")[1])
        return float(statistics.mean([float(i) for i in range.split("-")]))
    elif "–" in range:
        return float(statistics.mean([float(i) for i in range.split("–")]))
    elif ">" in range:
        if "±" in range:
            return float(range.split("±")[0][1:])
        if "=" in range:
            return float(range.split("=")[1])
        return float(range[1:])
    elif "<" in range:
        if "±" in range:
            return float(range.split("±")[0][1:])
        return float(range[1:])
    elif "±" in range:
        return float(range.split("±")[0])
    else:
        return float(range)
