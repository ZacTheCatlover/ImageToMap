import itertools
from typing import Any, Dict, Generator, Iterable, Tuple, TypeVar

from PIL import Image

from .consts import TILES

__all__ = ("make_palette", "batched", "json_loads", "json_dumps")
T = TypeVar("T")


def make_palette(tiles: Iterable[str]) -> Image:
    palette = Image.new("P", (1, 1))
    palette.putpalette(c for tile in tiles for c in TILES[tile])
    return palette


try:
    from itertools import batched  # type: ignore[attr-defined]

except ImportError:
    # https://docs.python.org/3.12/library/itertools.html#itertools.batched
    def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
        iterator = iter(iterable)
        while batch := tuple(itertools.islice(iterator, n)):
            yield batch


try:
    from msgspec.json import Decoder, Encoder

    decoder = Decoder()
    json_loads = decoder.decode

    encoder = Encoder()
    json_dumps = encoder.encode

except ImportError:
    from json import loads, dumps

    json_loads = loads  # type: ignore[assignment]

    def json_dumps(obj: Dict[str, Any]) -> bytes:
        return dumps(obj, indent=None, separators=(",", ":")).encode()
