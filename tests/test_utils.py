"""Tests for utils.py module."""


from typing import Dict, List, Optional, Tuple

import pytest

from pdm_pip_index_url.utils import BaseAuth, StrippedUrl, find_env, strip_url


@pytest.mark.parametrize(
    "envs,keys,expected_pair",
    [
        ({}, [], None),
        ({}, ["foo"], None),
        ({"key1": "value1"}, ["key1"], ("key1", "value1")),
        ({"key1": "value1", "key2": "value2"}, ["key1", "key2"], ("key1", "value1")),
        ({"key1": "value1", "key2": "value2"}, ["key2", "key1"], ("key2", "value2")),
        ({"key1": "value1", "key2": "value2"}, ["key3"], None),
    ],
)
def test_find_env(
    envs: Dict[str, str], keys: List[str], expected_pair: Optional[Tuple[str, str]]
) -> None:
    """Check if env pair is found as expected."""
    assert find_env(envs=envs, keys=keys) == expected_pair


@pytest.mark.parametrize(
    "url,expected_stripped_url",
    [
        ("url.com", StrippedUrl(url="url.com", auth=None)),
        ("http://url.com", StrippedUrl(url="http://url.com", auth=None)),
        (
            "http://secret@url.com",
            StrippedUrl(
                url="http://url.com", auth=BaseAuth(username="foo", password="secret")
            ),
        ),
        (
            "https://john:secret@url.com",
            StrippedUrl(
                url="https://url.com", auth=BaseAuth(username="john", password="secret")
            ),
        ),
    ],
)
def test_strip_url(url: str, expected_stripped_url: StrippedUrl) -> None:
    """Check if url is stripped as expected."""
    assert strip_url(url=url) == expected_stripped_url
