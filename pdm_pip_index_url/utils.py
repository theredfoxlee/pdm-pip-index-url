import urllib.parse
from typing import Iterable, Mapping, NamedTuple, Optional, cast


def find_env(envs: Mapping[str, str], keys: Iterable[str]) -> Optional[tuple[str, str]]:
    """Return `(key, value)` pair for first `key` from `keys` that exists in `envs`."""
    for key in keys:
        if (value := envs.get(key)) is not None:
            return key, value
    return None


class BaseAuth(NamedTuple):
    username: str
    password: str


class ParsedUrl(NamedTuple):
    url: str
    auth: Optional[BaseAuth]


def parse_url(url: str) -> ParsedUrl:
    parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(url)

    url_without_auth: str = cast(
        str,
        urllib.parse.urlunparse(
            parsed_url._replace(netloc=cast(str, parsed_url.hostname))
        ),
    )
    auth: Optional[BaseAuth] = None

    # Checking the authentication components
    if parsed_url.username and parsed_url.password:
        # Case 1: username and password are provided
        auth = BaseAuth(username=parsed_url.username, password=parsed_url.password)
    elif parsed_url.username:
        # Case 2: only key is provided
        auth = BaseAuth(username="foo", password=parsed_url.username)

    return ParsedUrl(url=url_without_auth, auth=auth)
