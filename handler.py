import re

import utils


def output(string: str):
    template = "RFlvl    Max    Min    State    C/N    Max    Min    CRCs    Q-quit"
    template = utils.handle_duplicate_columns(template)
    return list(map(utils.flt, _get_values(template, string, ["State", "C/N", "Max_1", "Min_1"])))


def _get_values(template, string, column_names):
    if isinstance(template, str):
        template = template.split()

    parsed_data = re.split(r"\s{2,}", string.strip())

    result = []
    for column_name in column_names:
        column_index = template.index(column_name)
        value = parsed_data[column_index]
        result.append(value)
    return result