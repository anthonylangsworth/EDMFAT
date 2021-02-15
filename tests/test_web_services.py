import pytest
import logging
import functools
from typing import Callable, Dict, Tuple

from web_services import resolve_star_system_via_edsm, split_tag, get_newer_release
from edmfs.state import StarSystem
from edmfs.tracker import _get_dummy_logger

#@pytest.mark.skip(reason="Potentially long-running or external test")
@pytest.mark.parametrize(
    "system_address, expected_name",
    [
        (5070074488225, "Kamchaa"),
        (11666338948537, "Oluf")
    ]
)
def test_resolve_star_system_via_edsm(system_address: int, expected_name: StarSystem) -> None:
    assert resolve_star_system_via_edsm(_get_dummy_logger(), system_address).name == expected_name

@pytest.mark.parametrize(
    "tag, expected_result",
    [
        ("v1.0", (1, 0)),
        ("v1.1.2", (1, 1, 2)),
        ("v0.15", (0, 15)),
        ("v9", (9,))
    ]
)
def test_split_tag(tag:str, expected_result:Tuple[int]):
    assert split_tag(tag) == expected_result

#@pytest.mark.skip(reason="Potentially long-running or external test")
def test_get_newer_release():
    assert get_newer_release(_get_dummy_logger(), "anthonylangsworth", "EDMFAT", (0, 14))
