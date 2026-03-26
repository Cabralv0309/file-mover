"""Creates a test enviorement with empty files"""

import os

starter_dir = os.getcwd()

def create_test_env(base_path = starter_dir):
    """Creates folders for testing the desktop_cleaner.py"""
    for dir_name in ['env_downloads','env_docs','env_vids','env_songs','env_img']:
        path = os.path.join(base_path, dir_name)
        os.makedirs(path, exist_ok=True)
    print('Test folders created')


def populate_folder(folder_path):
    """Fills a folder with empty files"""
    fake_files = ['fake1.txt', 'texst.txt','fake2.mp3',
                  'photo.jpg', 'wllpr.jpg', 'animation.gif',
                  'clip.mov', 'song.mp3', 'raw_image.tiff',
                  'archive.zip', 'styles.css', 'manual.pdf']
    for file in fake_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'w') as f:
            pass
    print(f'Folder {folder_path} was filled with fake files')

create_test_env()
populate_folder(os.path.join('env_downloads'))