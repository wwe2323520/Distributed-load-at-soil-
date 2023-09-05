# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 00:30:17 2023

@author: User
"""


import os
import fileinput

def replace_text_in_files(folder_path, old_text, new_text):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".vtu"):
                file_path = os.path.join(root, file)
                with fileinput.FileInput(file_path, inplace=True) as f:
                    for line in f:
                        print(line.replace(old_text, new_text), end='')

if __name__ == "__main__":
    folder_path = "soil10m_SideMidDash_Pwave"
    old_text = "Float32"
    new_text = "Float64"
    replace_text_in_files(folder_path, old_text, new_text)
    
print("Change file ok")
