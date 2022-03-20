def approximate(values: list) -> list:
    results = []
    for v in values:
        if v > 0.75:
            results.append(1.0)
        elif v > 0.25:
            results.append(0.5)
        elif v > -0.25:
            results.append(0.0)
        elif v > -0.75:
            results.append(-0.5)
        else:
            results.append(-1.0)
    return results


def calculate_avg(values: list) -> float:
    if len(values) == 0:
        return 0.0
    return sum(values) / len(values)