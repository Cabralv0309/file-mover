import os

starter_dir = os.getcwd()

def clean_folder(folder):
    for file in folder:
        os.remove(file)

for dir in ['env_downloads','env_docs','env_vids','env_songs','env_img']:
    os.chdir(dir)
    clean_folder(os.listdir())
    os.chdir(starter_dir)