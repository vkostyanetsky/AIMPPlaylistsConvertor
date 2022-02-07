import os
import argparse

def get_args():

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--input',
        type = str,
        help = 'input directory with source data',
        required = True
    )

    args_parser.add_argument(
        '--output',
        type = str,
        help = 'output directory with result data',
        required = True
    )

    return args_parser.parse_args()
    
def convert_playlist(aimp_playlist_filename):

    def get_m3u8_playlist_lines():

        def get_relative_audiofile_path(audiofile_path):
            
            paths = {audiofile_path, args.output}
            common_path = os.path.commonpath(paths)

            if common_path != '':
                result = os.path.relpath(audiofile_path, start = common_path)
            else:
                result = audiofile_path

            return result

        result = []
        result.append('#EXTM3U')

        is_content = False

        for (index, line) in enumerate(aimp_playlist_lines):

            if line == '#-----CONTENT-----#':
                is_content = True
                continue

            if not is_content:
                continue

            if line.startswith('-'):
                continue

            line_parts = line.split('|')

            audiofile_path = get_relative_audiofile_path(line_parts[0])

            result.append('#EXTINF:')
            result.append(audiofile_path)

        return result

    def write_m3u8_playlist():

        def get_m3u8_playlist_path():

            aimp_playlist_filename_without_extension    = os.path.splitext(aimp_playlist_filename)[0]
            m3u8_playlist_filename                      = '{}.m3u8'.format(aimp_playlist_filename_without_extension)

            return os.path.join(args.output, m3u8_playlist_filename)

        playlist_path = get_m3u8_playlist_path()
        playlist_data = '\n'.join(m3u8_playlist_lines)
        
        with open(playlist_path, "w", encoding = 'utf-8-sig') as m3u8file:
            m3u8file.write(playlist_data)

    file_path = os.path.join(args.input, aimp_playlist_filename)
            
    with open(file_path, encoding = 'utf_16_le') as handle:

        aimp_playlist_lines = handle.read().splitlines()        
        m3u8_playlist_lines = get_m3u8_playlist_lines()

        write_m3u8_playlist()

args = get_args()

files = os.walk(args.input)

for root, dirs, filenames in files:
    
    for filename in filenames:        

        filename_extension = os.path.splitext(filename)[1]

        if filename_extension == '.aimppl4':
            convert_playlist(filename)
