import pytest
import logging

from edmfs.resolvers import resolve_star_system_via_edsm
from edmfs.state import StarSystem
from edmfs.tracker import _get_dummy_logger

@pytest.mark.skip(reason="Potentially long-running or external test")
@pytest.mark.parametrize(
    "system_address, expected_name",
    [
        (5070074488225, "Kamchaa"),
        (11666338948537, "Oluf"),
        (16064117220777, "LHS 3836")
    ]
)
def test_resolve_star_system_via_edsm(system_address: int, expected_name: StarSystem) -> None:
    assert resolve_star_system_via_edsm(_get_dummy_logger(), system_address).name == expected_name

import functools

def test_partial():
    logger = _get_dummy_logger()
    partial_func = functools.partial(resolve_star_system_via_edsm, logger)
    assert partial_func(5070074488225)
