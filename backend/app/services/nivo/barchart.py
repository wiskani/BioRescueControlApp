from typing import List, Dict
from collections import Counter

from app.schemas.nivo import (
        BarChartFamily,
        ColorHSLBase,
        )


def count_families(families: List[str]) -> Dict[str, int]:
    """
    Count the number of families in flora.
    """
    families_dic = Counter()
    for family in families:
        families_dic[family] += 1
    return families_dic


def create_barchart_family_flora(
        flora_families_rescues: List[str],
        flora_families_relocation: List[str],
        ) -> List[BarChartFamily]:
    """
    Create bar chart data for families.
    """

    families_rescues = count_families(flora_families_rescues)
    families_relocation = count_families(flora_families_relocation)

    COLOR_FLORA_RESCUE: dict = {
            "h": 230,
            "s": 40,
            "l": 40
            }
    COLOR_FLORA_RELOCATION: dict = {
            "h": 130,
            "s": 40,
            "l": 40
            }
    addColor1 = 5
    addColor2 = 5

    families = []
    for family in families_rescues:
        rescue_count = families_rescues[family]
        relocation_count = families_relocation[family]

        # create color rescue
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_FLORA_RESCUE["h"],
                s=COLOR_FLORA_RESCUE["s"]+addColor1,
                l=COLOR_FLORA_RESCUE["l"]+addColor1
                )
        if addColor1 < 80:
            addColor1 += 5
        else:
            addColor1 = 5

        # create color relocation
        color_hsl2: ColorHSLBase = ColorHSLBase(
                h=COLOR_FLORA_RELOCATION["h"],
                s=COLOR_FLORA_RELOCATION["s"]+addColor2,
                l=COLOR_FLORA_RELOCATION["l"]+addColor2
                )
        if addColor2 < 80:
            addColor2 += 5
        else:
            addColor2 = 5

        color_rescue = f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
        color_relocation = f"hsl({color_hsl2.h},{color_hsl2.s}%,{color_hsl2.l}%)"

        families.append(
                BarChartFamily(
                    family_name=family,
                    rescue_count=rescue_count,
                    rescue_color=color_rescue,
                    relocation_count=relocation_count,
                    relocation_color=color_relocation
                    )
                )
    return families
