# This is mostly copied from [this answer on Stack Overflow](https://stackoverflow.com/a/49452109/3330552)
# (Thanks [Ryan Tuck](https://github.com/ryantuck)!)
# except that I've included the dependencies and set this up to be called from the command line.
#
# Example call from bash to split a single CSV into multiple 100 line CSVs:
#     python3 split_csv /path/to/my/file.csv /path/to/split_files my_split_file 100
#
# Warning: This doesn't have any validation! This will overwrite existing files if you're not careful.

import csv
import os
import sys
import shutil
import argparse

# if len(sys.argv) != 5:
#     raise Exception('Wrong number of arguments!')

# SOURCE_FILEPATH = sys.argv[1]
# DEST_PATH = sys.argv[2]
# FILENAME_PREFIX = sys.argv[3]
# ROW_LIMIT = int(sys.argv[4])

# args = data/yt_web_video_update_template_20190502.csv data bullyblock-update 150

parser = argparse.ArgumentParser(description='Split CSV into n directories.')
parser.add_argument('source_file', type=str, help='Master CSV file to split')
parser.add_argument('media_key', type=str, help='Mediakey of the show to process')
parser.add_argument('thumbnail', type=str, help='Thumbnail filename')

args = parser.parse_args()

SOURCE_FILEPATH = args.source_file
DEST_PATH = ''
FILENAME_PREFIX = args.media_key + '_upload'
ROW_LIMIT = 1
THUMB_FILE = args.thumbnail

def split_csv(source_filepath, dest_path, result_filename_prefix, row_limit, thumb):
    """
    Split a source CSV into multiple CSVs of equal numbers of records,
    except the last file.

    The initial file's header row will be included as a header row in each split
    file.

    Split files follow a zero-index sequential naming convention like so:

        `{result_filename_prefix}_0.csv`
        :param source_filepath {str}:
        File name (including full path) for the file to be split.
    :param dest_path {str}:
        Full path to the directory where the split files should be saved.
    :param result_filename_prefix {str}:
        File name to be used for the generated files.
        Example: If `my_split_file` is provided as the prefix, then a resulting
                 file might be named: `my_split_file_0.csv'
    :param row_limit {int}:
        Number of rows per file (header row is excluded from the row count).
    :return {NoneType}:
    """
    if row_limit <= 0:
        raise Exception('row_limit must be > 0')

    with open(source_filepath, 'r') as source:
        reader = csv.reader(source)
        headers = next(reader)

        file_number = 1
        records_exist = True

        while records_exist:

            i = 0
            # Create a subdirectory for every csv file (makes processing on YouTube easier)
            subdir = f'{result_filename_prefix}_{file_number}'
            dest_subdir = os.path.join(dest_path, subdir)
            try:
                os.stat(dest_subdir)
            except:
                os.mkdir(dest_subdir)

            target_filename = f'{result_filename_prefix}_{file_number}.csv'
            target_filepath = os.path.join(dest_subdir, target_filename)

            shutil.copy2(thumb, dest_subdir)

            with open(target_filepath, 'w', newline='') as target:
                writer = csv.writer(target)

                while i < row_limit:
                    if i == 0:
                        writer.writerow(headers)

                    try:
                        writer.writerow(next(reader))
                        i += 1
                    except:
                        records_exist = False
                        break

            if i == 0:
                # we only wrote the header, so delete that file
                os.remove(target_filepath)

            file_number += 1

split_csv(SOURCE_FILEPATH, DEST_PATH, FILENAME_PREFIX, ROW_LIMIT, THUMB_FILE)
