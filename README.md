# 🗺️ Minecraft Player Map Viewer

A lightweight web app to visualize player-created Minecraft map items (`map_#.dat` files). This tool parses the binary data of in-game map items and converts them into images for use with Leaflet.

> [!IMPORTANT]
> This'll work for at least Python 3.7 and up. Any lower versions are not guaranteed to work.
>
> This has only been tested on Minecraft versions above 1.20

## 🎯 Features

- 📄 Supports only player-created `map_#.dat` files
- 🧭 Renders handheld Minecraft maps as Leaflet tiles
- 🕒 Maps are sorted largest to smallest, oldest to youngest
- ⚡ Static and fast — runs locally with Python and JavaScript
- 🧱 Simple to use

## 📂 File Format

This tool works exclusively with the `map_#.dat` files found in your Minecraft world save directory:

```
.minecraft/saves/<world_name>/data/map_#.dat
```

These files are created when a player crafts and uses an in-game map item.

One thing to note is that files are only updated when the world saves.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PixlePixle/mc-maps2tiles.git
cd mc-maps2tiles
```

### 2. Install Python dependencies

You'll need the following libraries:
- Pillow
- tqdm
- watchdog if you'll use the included example fileWatcher script

### 3. Convert `.dat` files to image tiles

#### To generate the tiles only once, use mapCreator.py
```bash
python mapCreator.py <source_dir> <output_dir>
```

This will generate image tiles for use with Leaflet. An example `index.html` can be found in `./site/`

#### To watch a directory, use fileWatcher.py
```bash
python fileWatcher.py <source_dir> <output_dir>
```

This will call mapCreator.py every time there is an update in the source directory. Will run after a delay in order to batch file updates.

> [!IMPORTANT]
> You'll have to tell Leaflet to use tile sizes of 128x128 as the default is 256x256.
>
> Additionally, this generates only the minimum tiles needed so native zooms must be set as well.

## 🖼️ Screenshot

TODO: Include screenshot
<!-- ![screenshot](screenshot.png) -->

## 🧰 Built With

* Python (for parsing NBT and rendering image tiles)
* [Leaflet.js](https://leafletjs.com/) (for web map display)

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## Future
- [ ] Add player tracking for servers
- [ ] Add banner tracking
- [ ] Improve scripts

---

This was created for use on my personal Minecraft server and therefore what works for me may not work for you.
