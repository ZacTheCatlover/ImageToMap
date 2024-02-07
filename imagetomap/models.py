from dataclasses import dataclass

from PIL.Image import Image


@dataclass(frozen=True, slots=True)  # type: ignore[call-overload]
class Map:
    data: bytes
    width: int
    height: int
    preview: Image
