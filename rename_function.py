from collections import deque
import os
from pathlib import Path
import shutil


def rename(old_path,old_name,new_name):
    new_path = old_path.replace(old_name,new_name)
    shutil.move(old_path,new_path)

def separation_type(list_all):
    folders, filies = [], []
    for any in list_all:
        if os.path.isfile(any):
            filies.append(any)
        elif os.path.isdir(any):
            folders.append(any)
    return folders, filies

def rename_file(folder_name, old_name,new_name):
    deq = deque([folder_name])
    used = {folder_name}
    while deq:
        new_folder = deq.popleft()
        list_all = os.listdir(new_folder)
        list_folder, list_file = separation_type(list_all)

        for file in list_file:
            rename(file,old_name,new_name)
        for folder in list_folder:
            if folder not in used:
                used.add(folder)
                deq.append(folder) 
    print('Файлы переименованы.')

        
if __name__=="__main__":
    name_image = 'фото'
    price = '5000 р'
    print(Path('C:\image_for_Alex',name_image+'.'+price+'.jpg'))