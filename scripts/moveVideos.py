import fnmatch
import os
import re
import shutil

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.mp4'):
        fileroot = re.search('\S+(\_)',file).group(0)
        episode = re.search('(\-)(\d{1,3})(\.)',file).group(2)
        # print(episode)
        # print(file)
        dest_subdir = fileroot + 'upload_' + episode
        print(f'\tMoving file {file} with episode {episode} into folder {dest_subdir}')
        shutil.move(file, dest_subdir)

