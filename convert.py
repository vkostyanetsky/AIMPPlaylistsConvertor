import argparse
import os


def get_args() -> argparse.Namespace:
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
    paths = [audiofile_path, args.output_dir]
    common_path = os.path.commonpath(paths)

    if common_path != "":
        result = os.path.relpath(audiofile_path, start=common_path)
    else:
        result = audiofile_path

    return result


def get_result_playlist_lines(source_playlist_lines: list) -> list:
    result = ["#EXTM3U"]

    is_content = False

    for (index, line) in enumerate(source_playlist_lines):

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


def get_result_playlist_path(source_playlist_filename) -> str:
    source_playlist_filename_without_extension = os.path.splitext(
        source_playlist_filename
    )[0]
    result_playlist_filename = f"{source_playlist_filename_without_extension}.m3u8"

    return os.path.join(args.output_dir, result_playlist_filename)


def write_result_playlist(
    source_playlist_filename: str, result_playlist_lines: list
) -> None:

    playlist_path = get_result_playlist_path()
    playlist_data = "\n".join(result_playlist_lines)

    with open(playlist_path, "w", encoding="utf-8-sig") as result_file:
        result_file.write(playlist_data)


def convert_playlist(
    source_playlist_directory: str, source_playlist_filename: str
) -> None:

    file_path = os.path.join(source_playlist_directory, source_playlist_filename)

    with open(file_path, encoding="utf_16_le") as handle:

        source_playlist_lines = handle.read().splitlines()
        result_playlist_lines = get_result_playlist_lines(source_playlist_lines)

        write_result_playlist(source_playlist_filename, result_playlist_lines)


args = get_args()

if args.input_file is not None:

    directory_name = os.path.dirname(args.input_file)
    basename = os.path.basename(args.input_file)

    convert_playlist(directory_name, basename)

elif args.input_dir is not None:

    # noinspection SpellCheckingInspection
    aimp_playlist_extension = ".aimppl4"

    files = os.walk(args.input_dir)

    for root, dirs, filenames in files:

        for filename in filenames:

            filename_extension = os.path.splitext(filename)[1]

            if filename_extension == aimp_playlist_extension:
                convert_playlist(args.input_dir, filename)
