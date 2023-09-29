import re
from typing import List

from lasso_sennin.utils.address_mapping_utilities import test_address_mappings


def replace_with_index(string: str, pattern: str, replacement_list: List[str]):
    for match in re.finditer(pattern, string):
        index = int(match.group(1)) - 1
        string = string.replace(match.group(0), replacement_list[index])
    return string


def replace_without_index(string: str, pattern: str, replacement: str):
    return string.replace(pattern, replacement)


def replace_addresses_with_test_addresses(string: str):
    for key, value in test_address_mappings.items():
        pattern_base = re.escape(
            key[:-1],
        )
        string = replace_with_index(
            string,
            pattern_base + r"_(\d+)>",
            value,
        )
        string = replace_without_index(
            string,
            pattern_base + r">",
            value[0],
        )
    return string
