import pytest
import logging
import functools
from typing import Callable, Dict

from edmfs.resolvers import resolve_star_system_via_edsm #, ResolvingDict
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

# @pytest.mark.parametrize(
#     "inner_dict, resolver, key, expected_value",
#     [
#         (5070074488225, "Kamchaa"),
#         (11666338948537, "Oluf"),
#         (16064117220777, "LHS 3836")
#     ]
# )
# def test_resolving_dict_init(inner_dict:Dict, resolver:Callable, key, expected_value):
#     resolving_dict = ResolvingDict(lambda x:None)
#     assert len(resolving_dict) == 0
#     # assert resolving_dict.
#     # TODO: Test    

