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

def contains_only_digits(mic, range_threshold):
    for i in mic:
        if i not in "0123456789.":
            if i == "-" or i == "–":
                return is_range_ok(mic, range_threshold)
            return False
    return True

def is_range_ok(mic, range_threshold):
    if "-" in mic:
        mic_range = mic.split("-")
        if contains_only_digits(mic_range[0], range_threshold) and contains_only_digits(mic_range[1], range_threshold):
            if (float(mic_range[1]) - float(mic_range[0])) > range_threshold:
                return False
            print("Mic has ok range\t\t" + mic)
            return True
        return False
    if "–" in mic:
        mic_range = mic.split("–")
        if contains_only_digits(mic_range[0]) and contains_only_digits(mic_range[1]):
            if (float(mic_range[1]) - float(mic_range[0])) > range_threshold:
                return False
            print("Mic has ok range\t\t" + mic)
            return True
        return False
    return False
