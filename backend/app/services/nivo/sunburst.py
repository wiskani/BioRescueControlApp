from typing import List


from app.schemas.nivo import (
        SunburstBase,
        ColorHSLBase,
        )


# Create SunburstBase children
def create_sunburst_base_children(
        name: str,
        children: List[str],
        color: str,
        ) -> SunburstBase:
    loc: int = 0
    for child in children:
        if child == name:
            loc += 1
        else:
            pass
    result = SunburstBase(
            name=name,
            color=color,
            loc=loc,
            children=None
            )
    return result


# Create sunburst data
def create_sunburst_data(
        flora_families: List[str],
        herpetofauna_families: List[str],
        mammals_families: List[str],
        ) -> SunburstBase:

    # create flora rescue set
    flora_families_set: set = set(flora_families)
    flora_families_sorted = sorted(flora_families_set)

    # create herpetofauna rescue set
    herpetofauna_families_set: set = set(herpetofauna_families)
    herpetofauna_families_sorted = sorted(herpetofauna_families_set)

    # create mammals rescue list set
    mammals_families_set: set = set(mammals_families)
    mammals_families_sorted = sorted(mammals_families_set)

    COLOR_FLORA: dict = {
            "h": 230,
            "s": 40,
            "l": 40
            }

    COLOR_HERPETOFAUNA: dict = {
            "h": 130,
            "s": 40,
            "l": 40
            }

    COLOR_MAMMALS: dict = {
            "h": 40,
            "s": 40,
            "l": 40
            }

    # make children of rescue flora
    flora_children: List[SunburstBase] = []
    addColor = 5
    for family in flora_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_FLORA["h"],
                s=COLOR_FLORA["s"]+addColor,
                l=COLOR_FLORA["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            addColor = 5
        # create children
        children = create_sunburst_base_children(
                family,
                flora_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        flora_children.append(children)

    # make children of rescue herpetofauna
    herpetofauna_children: List[SunburstBase] = []
    addColor = 5
    for family in herpetofauna_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_HERPETOFAUNA["h"],
                s=COLOR_HERPETOFAUNA["s"]+addColor,
                l=COLOR_HERPETOFAUNA["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            pass
        # create children
        children = create_sunburst_base_children(
                family,
                herpetofauna_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        herpetofauna_children.append(children)

    # make children of rescue mammals
    mammals_children: List[SunburstBase] = []
    addColor = 5
    for family in mammals_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_MAMMALS["h"],
                s=COLOR_MAMMALS["s"]+addColor,
                l=COLOR_MAMMALS["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            pass
        # create children
        children = create_sunburst_base_children(
                family,
                mammals_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        mammals_children.append(children)

    # make SuburstBase global
    sunburst_data: SunburstBase = SunburstBase(
            name="Rescates",
            color="hsl(0,0%,0%)",
            loc=None,
            children=[
                SunburstBase(
                    name="Flora",
                    color="hsl(230,40%,40%)",
                    loc=None,
                    children=flora_children
                    ),
                SunburstBase(
                    name="Herpetofauna",
                    color="hsl(130,40%,40%)",
                    loc=None,
                    children=herpetofauna_children
                    ),
                SunburstBase(
                    name="Mamíferos",
                    color="hsl(40,40%,40%)",
                    loc=None,
                    children=mammals_children
                    )
                ]
            )

    return sunburst_data
