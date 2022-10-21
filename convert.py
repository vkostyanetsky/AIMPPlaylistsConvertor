"""Converts AIMP playlists to the universal M3U8 format."""

import argparse
import os


def get_args() -> argparse.Namespace:
    """
    Defines and parses the script's arguments.
    """

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        "--input-dir", type=str, help="input directory with source data", required=False
    )

    args_parser.add_argument(
        "--input-file", type=str, help="input file with source data", required=False
    )

    args_parser.add_argument(
        "--output-dir", type=str, help="output directory", required=True
    )

    return args_parser.parse_args()


def get_relative_audiofile_path(audiofile_path: str) -> str:
    """
    Returns relative path if the playlist & an audiofile
    are stored in the same folder.
    """

    paths = [audiofile_path, args.output_dir]
    common_path = os.path.commonpath(paths)

    if common_path != "":
        result = os.path.relpath(audiofile_path, start=common_path)
    else:
        result = audiofile_path

    return result


def get_result_playlist_lines(source_file_lines: list[str]) -> list[str]:
    """
    Makes lines of a M3U8 playlist file.
    """

    result = ["#EXTM3U"]

    is_content = False

    for (_, line) in enumerate(source_file_lines):

        if line == "#-----CONTENT-----#":
            is_content = True
            continue

        if not is_content:
            continue

        if line.startswith("#-----"):
            is_content = False
            continue

        if line.startswith("-"):
            continue

        line_parts = line.split("|")

        audiofile_path = get_relative_audiofile_path(line_parts[0])

        result.append("#EXTINF:")
        result.append(audiofile_path)

    return result


def get_result_playlist_path(source_file_name: str) -> str:
    """
    Makes a full path to a M3U8 playlist file.
    """

    source_file_name_without_extension = os.path.splitext(source_file_name)[0]
    result_file_name = f"{source_file_name_without_extension}.m3u8"

    return os.path.join(args.output_dir, result_file_name)


def write_result_playlist(source_file_name: str, result_file_lines: list[str]) -> None:
    """
    Writes a M3U8 playlist file.
    """

    playlist_path = get_result_playlist_path(source_file_name)
    playlist_data = "\n".join(result_file_lines)

    with open(playlist_path, "w", encoding="utf-8-sig") as result_file:
        result_file.write(playlist_data)


def convert_playlist(source_file_directory: str, source_file_name: str) -> None:
    """
    Converts the specified AIMP playlist to the M3U8 format.
    """

    file_path = os.path.join(source_file_directory, source_file_name)

    with open(file_path, encoding="utf_16_le") as handle:

        source_playlist_lines = handle.read().splitlines()
        result_playlist_lines = get_result_playlist_lines(source_playlist_lines)

        write_result_playlist(source_file_name, result_playlist_lines)


args = get_args()

if args.input_file is not None:

    directory_name = os.path.dirname(args.input_file)
    basename = os.path.basename(args.input_file)

    convert_playlist(directory_name, basename)

elif args.input_dir is not None:

    files = os.walk(args.input_dir)

    for root, dirs, filenames in files:

        for filename in filenames:

            filename_extension = os.path.splitext(filename)[1]

            if filename_extension == ".aimppl4":
                convert_playlist(args.input_dir, filename)
