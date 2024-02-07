from typing import Iterable, Tuple

from decimal import ROUND_CEILING as CEILING, ROUND_HALF_EVEN as HALF_EVEN, Decimal

from itertools import groupby
import zlib

from PIL import Image as Img
from PIL.Image import Image

from .consts import CHUNK_SIZE, MAP_TEMPLATE, TILES_TUPLE
from .models import Map
from .utils import batched, json_dumps, make_palette


def quantize(
    image: Image,
    palette: Image,
    dither: bool,
    width: int,
    height: int,
) -> Tuple[Image, Tuple[int, int]]:
    """Quantize the input image using the WorldBox tile colour palette.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to be quantized
    palette : PIL.Image.Image
        The palette to be quantized with the image
    dither : bool
        Enable dithering for smoother colour transitions
    width : int
        Target width of the map. Set to 0 for automatic sizing
    height : int
        Target height of the map. Set to 0 for automatic sizing

    Returns
    -------
    Tuple[PIL.Image.Image, Tuple[int, int]]
        A tuple containing two values:
            1. The quantized image
            2. The width and height of the map

    Raises
    ------
    ValueError
        If width or height is lower than 0
    """
    if width < 0 or height < 0:
        raise ValueError("width and height cannot be lower than 0")

    # Precision
    width_dcm = Decimal(width)
    height_dcm = Decimal(height)

    temp_width = Decimal(max(round(image.size[0] / CHUNK_SIZE), 1))
    temp_height = Decimal(max(round(image.size[1] / CHUNK_SIZE), 1))
    ratio = temp_height / temp_width

    if width_dcm == 0:
        if height_dcm == 0:
            width_dcm, height_dcm = temp_width, temp_height
        else:
            width_dcm = (height / ratio).to_integral_exact(rounding=HALF_EVEN)
    elif height_dcm == 0:
        height_dcm = (width * ratio).to_integral_exact(rounding=HALF_EVEN)

    size = (
        int(width_dcm * CHUNK_SIZE),
        int(
            ((height_dcm / width_dcm) * width_dcm * CHUNK_SIZE).to_integral_exact(
                rounding=CEILING,
            ),
        ),
    )
    image = image.resize(size=size, resample=Img.Resampling.NEAREST).convert("RGB")

    return (
        image.quantize(palette=palette, dither=int(dither)),
        (int(width_dcm), int(height_dcm)),
    )


def convert(
    image: Image,
    dither: bool = False,
    width: int = 0,
    height: int = 0,
    tiles: Iterable[str] = TILES_TUPLE,
) -> Map:
    """Convert an image to a WorldBox map.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to be converted
    dither : bool, default: False
        Enable dithering for smoother colour transitions
    width : int, default: 0
        Target width of the map. Set to 0 for automatic sizing
    height : int, default: 0
        Target height of the map. Set to 0 for automatic sizing
    tiles : iterable of str, default: imagetomap.consts.TILES_TUPLE
        An iterable object that yields tile names that will be used

    Returns
    -------
    imagetomap.models.Map
        The converted map
    """
    tiles = tiles if isinstance(tiles, (tuple, list)) else tuple(tiles)
    palette = make_palette(tiles=tiles)
    quantized_image, (width, height) = quantize(
        image=image,
        palette=palette,
        dither=dither,
        width=width,
        height=height,
    )

    flipped_image = quantized_image.transpose(Img.Transpose.FLIP_TOP_BOTTOM)
    tile_array, tile_amounts = [], []

    for batch in batched(flipped_image.getdata(), width * 64):
        array, amounts = zip(
            *((key, sum(1 for _ in group)) for key, group in groupby(batch))
        )

        tile_array.append(array)
        tile_amounts.append(amounts)

    map_data = MAP_TEMPLATE.copy()
    map_data["width"] = width
    map_data["height"] = height
    map_data["tileMap"] = tiles
    map_data["tileArray"] = tile_array
    map_data["tileAmounts"] = tile_amounts

    return Map(
        data=zlib.compress(json_dumps(map_data), 9),
        width=width,
        height=height,
        preview=quantized_image,
    )
