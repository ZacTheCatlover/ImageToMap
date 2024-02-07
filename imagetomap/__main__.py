from typing import Any, Dict, Iterable

import argparse

from pathlib import Path
from PIL import Image as Img

from . import convert
from .consts import TILES_TUPLE
from .utils import json_loads
import json

# fmt: off
IMAGE_FORMATS = {".apng", ".blp", ".bmp", ".bufr", ".bw", ".dds", ".dib", ".emf", ".eps", ".gif", ".grib", ".h5", ".hdf", ".icb", ".icns", ".ico", ".im", ".j2c", ".j2k", ".jfif", ".jp2", ".jpc", ".jpe", ".jpeg", ".jpf", ".jpg", ".jpx", ".msp", ".pbm", ".pcx", ".pgm", ".png", ".pnm", ".ppm", ".ps", ".rgb", ".rgba", ".sgi", ".tga", ".tif", ".tiff", ".vda", ".vst", ".webp", ".wmf", ".xbm"}
# fmt: on
parser = argparse.ArgumentParser(
    prog="ImageToMap",
    description="Convert images to WorldBox maps",
    epilog="",
)
parser.add_argument(
    "images",
    help="Image files to convert to maps. If this option is supplied with folders, the program will search for images inside them",
    nargs="*",
    type=Path,
)
parser.add_argument(
    "--no-config",
    help="Ignore the config file",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--generate-config",
    help="Generate a config file in the current directory",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-D",
    "--dither",
    help="Enable dithering for smoother colour transitions. Not recommended for maps designed to actually be played with",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-W",
    "--width",
    help="Target width of the map(s). Default to auto",
    type=int,
    default=0,
)
parser.add_argument(
    "-H",
    "--height",
    help="Target height of the map(s). Default to auto",
    type=int,
    default=0,
)
parser.add_argument(
    "-R",
    "--recursive",
    help="Enable recursive searching inside folders",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-O",
    "--output",
    help="Where to save the converted maps and previews. Default to the current directory",
    type=Path,
    default="./",
)


def process_args() -> Dict[str, Any]:
    args = {}
    parsed_args = parser.parse_args()

    if parsed_args.generate_config:
        with open("itm_config.json", "w+") as config_file:
            default_config = {
                "output": "./",
                "tiles": {tile: True for tile in TILES_TUPLE},
            }
            json.dump(default_config, config_file, indent=4)

    for arg in ("images", "dither", "width", "height", "recursive", "output"):
        args[arg] = getattr(parsed_args, arg)

    config_path = Path("itm_config.json")
    if not parsed_args.no_config and config_path.exists():
        config = json_loads(config_path.read_bytes())

        args["output"] = Path(config.get("output", "./"))
        args["tiles"] = [
            tile for tile, val in config.get("tiles", {}).items() if val is True
        ]

    else:
        args["tiles"] = TILES_TUPLE

    return args


def process_image(image_path: Path, args: Dict[str, Any], tiles: Iterable[str]) -> None:
    image = Img.open(image_path)
    output_path = args["output"] / image_path.stem

    converted_map = convert(
        image=image,
        dither=args["dither"],
        width=args["width"],
        height=args["height"],
        tiles=tiles,
    )
    output_path.mkdir(exist_ok=True, parents=True)
    with open(output_path / "map.wbox", "w+b") as map_file:
        map_file.write(converted_map.data)
    converted_map.preview.save(output_path / "preview.png", optimize=True)

    print("Converted", image_path)


def main() -> None:
    args = process_args()
    tiles = args["tiles"]

    for path in args["images"]:
        if not path.exists():
            print(f"Error: '{path}' does not exist")
            continue

        if path.is_dir():
            for glob_path in path.glob("**/*" if args["recursive"] else "*"):
                if glob_path.is_file() and glob_path.suffix.lower() in IMAGE_FORMATS:
                    process_image(glob_path, args, tiles)

        elif path.is_file() and path.suffix.lower() in IMAGE_FORMATS:
            process_image(path, args, tiles)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        pass
