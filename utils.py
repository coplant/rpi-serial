from collections import defaultdict
import math


def handle_duplicate_columns(string: str) -> str:
    column_counts = defaultdict(int)
    processed_columns = []

    for column in string.split():
        column_counts[column] += 1
        if column_counts[column] > 1:
            processed_columns.append(f"{column}_{column_counts[column] - 1}")
        else:
            processed_columns.append(column)

    return "\t".join(processed_columns)


def cint(s: int | float | str, default: int = 0) -> int:
    try:
        return int(float(s))
    except Exception:
        return default


def flt(s: int | float | str, precision: int | None = None, rounding_method: str | None = None) -> float:
    if isinstance(s, str):
        s = s.replace(",", "")

    try:
        num = float(s)
        if precision is not None:
            num = rounded(num, precision, rounding_method)
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        num = 0.0

    return num


def rounded(num, precision=0, rounding_method=None):
    precision = cint(precision)
    rounding_method = rounding_method or "Banker's Rounding"

    if rounding_method == "Banker's Rounding":
        return _bankers_rounding(num, precision)
    elif rounding_method == "Commercial Rounding":
        return _round_away_from_zero(num, precision)
    else:
        raise ValueError(("Unknown Rounding Method: {}").format(rounding_method))


def _round_away_from_zero(num, precision):
    if num == 0:
        return 0.0

    epsilon = 2.0 ** (math.log(abs(num), 2) - 52.0)

    return round(num + math.copysign(epsilon, num), precision)


def _bankers_rounding(num, precision):
    multiplier = 10**precision
    num = round(num * multiplier, 12)

    if num == 0:
        return 0.0

    floor_num = math.floor(num)
    decimal_part = num - floor_num

    epsilon = 2.0 ** (math.log(abs(num), 2) - 52.0)
    if abs(decimal_part - 0.5) < epsilon:
        num = floor_num if (floor_num % 2 == 0) else floor_num + 1
    else:
        num = round(num)

    return num / multiplier
