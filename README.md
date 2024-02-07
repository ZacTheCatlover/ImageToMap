# ImageToMap
A command-line image-to-map tool for WorldBox written in Python.

## Table of contents
- [Key Features](#key-features)
- [Installation](#installation)
  - [PC](#pc)
  - [Android](#android)
- [Usage](#usage)
  - [Simple](#simple)
  - [Config File](#config-file)
  - [Parameters](#parameters)

## Key Features
1. Fast: highly optimized tile conversion.
2. Auto sizing: if only one size parameter is set (width or height), the tool will automatically calculate the other from it and the ratio of the image.
3. Configurable: tiles that will be used in the conversion can be configured.

## Installation
### PC
1. Download and install [Python](https://www.python.org/downloads/)  (Ver. 3.8+)
2. Install the tool:
```sh
pip install git+https://github.com/ZacTheCatlover/ImageToMap
```

### Android
1. Download and Install [Termux from F-Droid](https://f-droid.org/packages/com.termux/)
2.  Run the following commands to install Python and the tool's requirements:
```sh
pkg upgrade -y && pkg install python python-pillow git -y
```
3. Install the tool:
```sh
pip install git+https://github.com/ZacTheCatlover/ImageToMap
```

## Usage
### Simple
Every image format that [PIL (pillow) supports](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#image-file-formats) is supported by this tool. You can quickly convert an image with this command:
```sh
imagetomap image.png
```

> [!Note]
Please note that the WorldBox map's dimensions need to be a multiple of 64, so for some images' sizes that are not multiples of 64, resizing will be necessary. This can lead to the images having unintended artifacts.

The converted image will then be stored in a folder with the image's name in the current directory.

You can convert multiple images in one go by simply giving more to the program:
```sh
imagetomap image.png image_two.png
```

Or by giving the program a folder, of which it will search for images inside of it:
```sh
imagetomap folder/
```

There are some parameters that be set. See:
```sh
imagetomap --help
```

### Config File
You can configure tiles you want or do not want the program to use with the config file. Run the following command to generate one:
```sh
imagetomap --generate-config
```

After that, the program will create an `itm_config.json` file in the current directory. The file should look like this:
```json
{
    "output": "./",
    "tiles": {
        "deep_ocean": true,
        "close_ocean": true,
        "shallow_waters": true,
        "sand": true,
        "soil_low": true,
        "soil_high": true,
        "soil_low:grass_low": true,
        "soil_high:grass_high": true,
        "soil_low:mushroom_low": true,
        "soil_high:mushroom_high": true,
        "soil_low:corrupted_low": true,
        "soil_high:corrupted_high": true,
        "soil_low:infernal_low": true,
        "soil_high:infernal_high": true,
        "soil_low:candy_low": true,
        "soil_high:candy_high": true,
        "soil_low:crystal_low": true,
        "soil_high:crystal_high": true,
        "soil_low:permafrost_low": true,
        "soil_high:permafrost_high": true,
        "soil_low:savanna_low": true,
        "soil_high:savanna_high": true,
        "soil_low:enchanted_low": true,
        "soil_high:enchanted_high": true,
        "soil_low:swamp_low": true,
        "soil_high:swamp_high": true,
        "soil_low:jungle_low": true,
        "soil_high:jungle_high": true,
        "soil_low:desert_low": true,
        "soil_high:desert_high": true,
        "soil_low:lemon_low": true,
        "soil_high:lemon_high": true,
        "soil_low:waste_low": true,
        "soil_high:waste_high": true,
        "soil_low:tumor_low": true,
        "soil_high:tumor_high": true,
        "soil_low:biomass_low": true,
        "soil_high:biomass_high": true,
        "soil_low:pumpkin_low": true,
        "soil_high:pumpkin_high": true,
        "soil_low:cybertile_low": true,
        "soil_high:cybertile_high": true,
        "lava3": true,
        "lava2": true,
        "lava1": true,
        "lava0": true,
        "pit_deep_ocean:tnt": true,
        "pit_deep_ocean:water_bomb": true,
        "pit_deep_ocean:tnt_timed": true,
        "pit_deep_ocean:landmine": true,
        "pit_deep_ocean:fuse": true,
        "pit_deep_ocean:fireworks": true,
        "pit_deep_ocean:field": true,
        "pit_deep_ocean:road": true,
        "hills": true,
        "mountains": true,
        "grey_goo": true
    }
}
```

You can exclude tiles by changing their values to `false`.

The program will use the `itm_config.json` file in the current directory by default. But if you want to, you can make it ignore the file by adding the`--no-config` option:
```sh
imagetomap image.png --no-config
```

### Parameters
#### `images`
Image files to convert to maps. If this option is supplied with folders, the program will search for images inside them.
```sh
imagetomap image.png
imagetomap image.png image_two.png
imagetomap folder/
```

#### `--no-config`
Ignore the config file.
```sh
imagetomap image.png --no-config
```

#### `--generate-config`
Generate a config file in the current directory.
```sh
imagetomap --generate-config
```

#### `-D, --dither`
Enable dithering for smoother colour transitions. Not recommended for maps designed to actually be played with.
```sh
imagetomap image.png --dither
```

#### `-W, --width`
Target width of the map(s). Default to auto.
```sh
imagetomap image.png --width 8
```

#### `-H, --height`
Target height of the map(s). Default to auto.
```sh
imagetomap image.png --height 8
```

#### `-R, --recursive`
Enable recursive searching inside folders.
```sh
imagetomap folder/ --recursive
```

#### `-O, --output`
Where to save the converted maps and previews. Default to the current directory.
```sh
imagetomap image.png --output Converted/
```
