# AIMP Playlists Convertor

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

It is a simple script, which can convert playlists of [AIMP](https://www.aimp.ru/) to the M3U8 format.

## How to use it?

Можно указать либо путь к конкретному файлу aimppl4 в параметре `file`, либо путь к директории с файлами aimppl4 в параметре `directory`. Обратите внимание, что в последнем случае вложенные директории не сканируются.

В параметре `output` укажите путь к директории, куда нужно записать результат конвертации. 

Пример:

```
python convert.py --directory C:\Users\Username\AppData\Roaming\AIMP\PLS --output D:\Music
```

Обратите внимание, что:

1. Имена итоговых файлов будут соответствовать исходным (за исключением расширения — оно меняется на m3u8).
2. Метаданные (название трека, исполнитель, продолжительность и так далее) не конвертируются. Их точная конвертация невозможна, в то время как их отсутствие для плееров обычно не проблема. Так что я решил просто сделать скрипт предсказуемым.
3. Если путь к треку можно сделать относительным по отношению к директории с результатом конвертации, он будет сделан относительным. Например, если конвертация идёт в D:\Music, а аудиофайлы лежат в D:\Music\Collection, то пути к ним скрипт сделает относительными: не D:\Music\Collection\Track.mp3, а Collection\Track.mp3 и так далее.
