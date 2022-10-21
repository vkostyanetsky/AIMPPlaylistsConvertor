# 🎶 🎙️ 🔊 AIMP Playlists Convertor

[![pylint](https://github.com/vkostyanetsky/AIMPPlaylistsConvertor/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/AIMPPlaylistsConvertor/actions/workflows/pylint.yml) [![flake8](https://github.com/vkostyanetsky/AIMPPlaylistsConvertor/actions/workflows/flake8.yml/badge.svg)](https://github.com/vkostyanetsky/AIMPPlaylistsConvertor/actions/workflows/flake8.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

This script converts playlists of [AIMP](https://www.aimp.ru/) to the M3U8 format.

## 😎 How to use it?

You can specify the path to a specific aimppl4 file in the `input-file` parameter, or the path to the directory with the aimppl4 files in the `input-dir` parameter. Note that nested directories will not be scanned.

In the `output-dir` parameter, specify the path to the directory where you want to see the result of the conversion. 

Example:

```commandline
python convert.py --input-dir C:\Users\Username\AppData\Roaming\AIMP\PLS --output-dir D:\Music
```

Please note that:

1. The names of the resulting files will match the original ones (except for the extension, which changes to m3u8).
2. Metadata (track title, artist, duration, etc.) are not converted. Their exact conversion is impossible, while their absence is usually not a problem for players (they simply read the metadata themselves).
3. If the path to the track can be made relative to the directory with the result of the conversion, it will be made relative. For example, if the conversion goes to `D:\Music`, and the audio files are in `D:\Music\Collection`, then the script will make the paths to them relative: not `D:\Music\Collection\Track.mp3`, but `Collection\Track.mp3` and so on further.