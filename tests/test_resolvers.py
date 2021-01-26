import pytest

from edmfs.resolvers import resolve_star_system_via_edsm
from edmfs.state import StarSystem

@pytest.mark.parametrize(
    "system_address, expected_star_system",
    [
        (5070074488225, StarSystem("Kamchaa", 5070074488225, []))
    ]
)
def test_resolve_star_system_via_edsm(system_address: int, expected_star_system: StarSystem) -> None:
    assert resolve_star_system_via_edsm(5070074488225) == expected_star_system