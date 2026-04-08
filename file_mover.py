"""
File organizer that assigns new dowloads to an adequate folder.
(e.g., pdf to documents, jpeg to images.)

Currently: only works on Windows OS

Author: Victor Cabral
Date: 2026/03/24
""" 



import os
import pathlib
import datetime
import time
import mimetypes
import shutil
import tkinter as tk
import locale

original_script_dir = os.getcwd() #This is a safeguard so the script can return to it's starting place if needed
DEBUG = False
if DEBUG:
    workplace = original_script_dir
    target_path, doc_path, vids_path, musics_path, img_path = ['env_downloads','env_docs','env_vids','env_songs','env_img']
    print('!!! Running in DEBUG mode !!!')
else:
    workplace = os.path.expanduser('~')
    #target_dir, doc_dir, vids_dir, musics_dir, img_dir = ['Downloads','Documentos','Vídeos','Músicas','Imagens'] #TODO: update to take tk entry

def get_directory_path(folder_name, base_path = workplace):
    """Returns a string with the path to the downloads directory."""
    return os.path.join(base_path, folder_name)


def filter_file_age_from_target(age=int, unit=str, target_path=str): #age uses hours as it's arguments TODO: change it to handle hours or days or create another def
    """Returns a list containing files that are {age} hours/months old or less."""
    if unit=='Hours':
        initialization = datetime.timedelta(hours=age)
    elif unit=='Days':
        initialization = datetime.timedelta(days=age)
    max_age = initialization.total_seconds()
    files = [os.path.join(target_path, f) for f in os.listdir(target_path)
             if os.path.isfile(os.path.join(target_path, f))]
    def file_age(file):
        now = time.time()
        file_epoch_time = os.path.getctime(file)
        return now - file_epoch_time
    filtered_files = [file for file in files if file_age(file) <= max_age]
    return filtered_files

def sort_file_type(file_list=list):
    """Assigns every file to an adequate list based on the file type
       and returns them"""
    doc_files, img_files, music_files, vid_files, unhandled_files = list(), list(), list(), list(), list()
    doc_extension_backup = {
        '.pdf': 'doc',
        '.docx': 'doc',
        '.txt': 'doc',
        '.pptx': 'doc',
    }

    for file in file_list:
        _, extension = os.path.splitext(file.lower())
        file_type,_ = mimetypes.guess_type(file)
        if file_type:
            if file_type.startswith('text'):
                doc_files.append(file)
                continue
            elif file_type.startswith('image'):
                img_files.append(file)
                continue
            elif file_type.startswith('audio'):
                music_files.append(file)
                continue
            elif file_type.startswith('video'):
                vid_files.append(file)
                continue
        if extension in doc_extension_backup.keys():
            doc_files.append(file)
        else:
            unhandled_files.append(file)

    return doc_files, img_files, music_files, vid_files, unhandled_files


def report_unhandled_files(unhandled_files):
    text_box.config(state='normal')
    text_box.insert(tk.END, 'The following files weren\'t moved:')
    # print('Os seguintes arquivos não foram movidos,\nportanto continuam em Downloads:')
    for file in unhandled_files:
        text_box.insert(tk.END, f'{pathlib.Path(file).name}')
        # print(f'{pathlib.Path(file).name}')
# print('\n----------------------------------------------------------------\n')
    text_box.config(state='disabled')

def report_move(file, dir):
    text_box.config(state='normal')
    text_box.insert(tk.END, f'{pathlib.Path(file).name} was moved to {pathlib.Path(dir).name}')
    text_box.config(state='disabled')
    # print(f'{pathlib.Path(file).name} foi movido para {pathlib.Path(dir).name}')


def move(file_list, dir):
    """Moves files in a list to a especified directory"""
    for file in file_list:
        try:
            shutil.move(file, dir)
            report_move(file, dir)
        except FileExistsError as err:
            text_box.config(state='normal')
            text_box.insert(tk.END, f'{file} already is at {dir}')
            text_box.config(state='disabled')
            # print(f'{file} já está em {dir}')
        except FileNotFoundError as err:
            text_box.config(state='normal')
            text_box.insert(tk.END, f'Check if {file} exists')
            text_box.config(state='disabled')
            # print(f'Verifique se {file} existe')
        except PermissionError as err:
            text_box.config(state='normal')
            text_box.insert(tk.END, f'Check if {file} is open')
            text_box.insert(tk.END,'or if user has permission to access it.')
            text_box.config(state='disabled')
            # print(f'Confira se {file} não está aberto\nou se o Usuário possui permissão para movimentar o arquivo')
        finally:
            continue
    # print('\n----------------------------------------------------------------\n')
    


import tkinter as tk
from tkinter import messagebox

#Window init
ui = tk.Tk()
ui.title('File Mover')
ui.geometry("700x500")
ui.grid_columnconfigure(0, weight=1)
ui.grid_rowconfigure(0, weight=1)
ui.grid_rowconfigure(99, weight=1)

greeting_lbl = tk.Label(ui, text='Hi! The File Mover takes the files on a selected folder and move them accordingly.' \
'\nPlease be aware that File Mover do not create new folders, so check if they exist in advance!')
greeting_lbl.grid(row=0, column=0)

#File age selector
def on_age_entry_click(event):
    if age_entry.get() == placeholder_age_entry:
        age_entry.delete(0, tk.END)
        age_entry.config(fg='black')

def on_age_entry_focusout(event):
    if age_entry.get() == '':
        age_entry.insert(0, placeholder_age_entry)
        age_entry.config(fg='grey')

input_frame = tk.Frame(ui)
input_frame.grid(row=1, column=0, padx=10)

placeholder_age_entry = 'Since when do you wish to filter files (type only numbers)'
age_entry = tk.Entry(input_frame, fg='grey', width=51)
age_entry.insert(0, placeholder_age_entry)
age_entry.bind('<FocusIn>', on_age_entry_click)
age_entry.bind('<FocusOut>', on_age_entry_focusout)
age_entry.pack(side='left')

v = tk.StringVar(value='Days')
def get_radio():
    return v.get()

for param in ['Days', 'Hours']:
    rb = tk.Radiobutton(input_frame, text=param, variable=v, value=param, command=get_radio)
    rb.pack(side='left', padx=5)


#Folder selector and path extraction UI
entry_frame = tk.Frame(ui)
entry_frame.grid(row=2, column=0)

target_lbl = tk.Label(entry_frame, text='Select the folder you wish to filter:')
target_lbl.grid(row=1, column=0, padx=5)
target_entry = tk.Entry(entry_frame)
target_entry.grid(row=1, column=1, pady=2)


document_lbl = tk.Label(entry_frame, text='Select the folder for your documents:')
document_lbl.grid(row=2, column=0, padx=5)
document_entry = tk.Entry(entry_frame)
document_entry.grid(row=2, column=1, pady=2)

video_lbl = tk.Label(entry_frame, text='Select the folder for your videos:')
video_lbl.grid(row=3, column=0, padx=5)
video_entry = tk.Entry(entry_frame)
video_entry.grid(row=3, column=1, pady=2)

music_lbl = tk.Label(entry_frame, text='Select the folder for your music:')
music_lbl.grid(row=4, column=0, padx=5)
music_entry = tk.Entry(entry_frame)
music_entry.grid(row=4, column=1, pady=2)

image_lbl = tk.Label(entry_frame, text='Select the folder for your image:')
image_lbl.grid(row=5, column=0, padx=5)
image_entry = tk.Entry(entry_frame)
image_entry.grid(row=5, column=1, pady=2)


#Text report for user comprehension
text_box = tk.Listbox(ui)
text_box.grid(row=4, padx=10, pady=10)
text_box.config(state='disabled', width=70, height=12)

#Sets folder names
if DEBUG:
    target_entry.insert(0, 'env_downloads')
    document_entry.insert(0, 'env_docs')
    video_entry.insert(0, 'env_vids')
    music_entry.insert(0, 'env_songs')
    image_entry.insert(0, 'env_img')

def get_language():
    local_language, _ = locale.getlocale()
    if local_language:
        return local_language.split('_')[0]
    return 'pt'

translations = {
    'pt': {
        'target': 'Downloads',
        'doc': 'Documentos',
        'vid': 'Vídeos',
        'music': 'Músicas',
        'img': 'Imagens'
    },
    'en': {
       'target': 'Downloads',
        'doc': 'Documents',
        'vid': 'Videos',
        'music': 'Music',
        'img': 'Pictures' 
    }
}
language = get_language()
def t(word=str):
    return translations.get(language, translations['pt']).get(word, word)


target_entry.insert(0, t('target'))
document_entry.insert(0, t('doc'))
video_entry.insert(0, t('vid'))
music_entry.insert(0, t('music'))
image_entry.insert(0, t('img'))

#script run logic (by pressing the confirm button)
def Confirm_btn():

    def get_entry(target_frame = entry_frame):
        return [entry.get().strip() for entry in target_frame.winfo_children() if isinstance(entry, tk.Entry)] # 'env_downloads','env_docs','env_vids','env_songs','env_img'

    entry_list = get_entry()
    
    for entry in entry_list:
        if not entry:
            messagebox.showwarning('Empty folder detected','Folders must be specified so the File Mover'\
                                   '\nknows where to put your files.!')

    try:
        target_path = get_directory_path(entry_list[0])
        doc_path = get_directory_path(entry_list[1])
        vid_path = get_directory_path(entry_list[2])
        music_path = get_directory_path(entry_list[3])
        img_path = get_directory_path(entry_list[4])
        
        for i in [target_path, doc_path, vid_path, music_path, img_path]:
            if not os.path.exists(i):
                raise FileNotFoundError(f'The file in {i} doesn\'t exists')
            elif not os.path.isdir(i):
                raise NotADirectoryError(f'The path "{i}" is not a valid directory.')
    
    except FileNotFoundError as err:
        messagebox.showerror('Folder not found!', f'Check if your folder(s) exist.\nError details: {str(err)}')
        return
    except PermissionError as err:
        messagebox.showerror('Permission error!', f'Check if current user has permission to operate in all folders.\nError details: {str(err)}')
        return
    except NotADirectoryError as err:
        messagebox.showerror('Invalid folder', f'Please input a valid folder, and not a file.\nError details: {str(err)}')
        return


    #age logic
    age_input = age_entry.get().strip()
    if age_input == placeholder_age_entry:
        messagebox.showwarning('Empty filter detected', 'Please enter a number to tell the Mover' \
        '\nhow far back to look for files.')
    elif not age_input.isdigit():
        messagebox.showerror('Invalid number detected', 'Please type only digits for the filter\n(e.g., 10, 55, 100)')
    
    files = filter_file_age_from_target(age=int(age_input), unit=get_radio(), target_path=target_path)

    doc_files, img_files, music_files, vid_files, unhandled_files = sort_file_type(files)
    
    move(doc_files, doc_path)
    move(img_files, img_path)
    move(music_files, music_path)
    move(vid_files, vid_path)
    report_unhandled_files(unhandled_files)
             
confirm_btn = tk.Button(ui, text='Confirm', command=Confirm_btn)
confirm_btn.grid(row=3, column=1, padx=30, pady=10)




ui.mainloop()