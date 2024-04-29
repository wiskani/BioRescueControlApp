from typing import List, Dict
from collections import Counter


def count_families(families: List[str]) -> Dict[str, int]:
    """
    Count the number of families in flora.
    """
    families_dic = Counter()
    for family in families:
        families_dic[family] += 1
    return families_dic
