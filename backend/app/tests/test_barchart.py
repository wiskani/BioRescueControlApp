from app.services.nivo.barchart import count_families
from app.schemas.nivo import BarChartFamily

from app.services.nivo.barchart import (
        create_barchart_family_flora
        )


def test_count_families() -> None:
    """
    Test count_families function.
    """
    families = [
            "Acanthaceae",
            "Acanthaceae",
            "Acanthaceae",
            "Acanthaceae",
            "Bignoniaceae",
            "Bignoniaceae",
            "Acanthaceae",
            "Cactaceae",
            "Cactaceae",
            "Cactaceae",
            ]
    result = count_families(families)
    assert result == {
            "Acanthaceae": 5,
            "Bignoniaceae": 2,
            "Cactaceae": 3,
            }


def test_create_barchart_family_flora() -> None:
    """
    Test make_barchart function.
    """
    families_rescue = [
            "Acanthaceae",
            "Acanthaceae",
            "Acanthaceae",
            "Acanthaceae",
            "Bignoniaceae",
            "Bignoniaceae",
            "Acanthaceae",
            "Cactaceae",
            "Cactaceae",
            "Cactaceae",
            ]
    families_relocation = [
            "Acanthaceae",
            "Acanthaceae",
            "Acanthaceae",
            "Bignoniaceae",
            "Acanthaceae",
            "Cactaceae",
            "Cactaceae",
            ]

    result = create_barchart_family_flora(
            families_rescue, families_relocation
            )

    famili1 = BarChartFamily(
            family_name="Acanthaceae",
            rescue_count=5,
            rescue_color="hsl(230,45%,45%)",
            relocation_count=4,
            relocation_color="hsl(130,45%,45%)",
            )
    famili2 = BarChartFamily(
            family_name="Bignoniaceae",
            rescue_count=2,
            rescue_color="hsl(230,50%,50%)",
            relocation_count=1,
            relocation_color="hsl(130,50%,50%)",
            )
    famili3 = BarChartFamily(
            family_name="Cactaceae",
            rescue_count=3,
            rescue_color="hsl(230,55%,55%)",
            relocation_count=2,
            relocation_color="hsl(130,55%,55%)",
            )

    expected = [famili1, famili2, famili3]

    assert result == expected
