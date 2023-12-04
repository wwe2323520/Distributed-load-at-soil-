# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:40:11 2023

@author: User
"""
import numpy as np
import os
import cv2
import imageio
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess

# 指定包含圖片的資料夾
FileName = ['LeftColumn', 'CenterColumn', 'RightColumn', 'SurfaceVel']
a_cofficient = np.arange(0.0, 2.0+0.2, 0.2)
b_cofficient = np.arange(0.0, 2.0+0.2, 0.2)

for akz in a_cofficient:
    for bkz in b_cofficient:
        a = round(akz, 2)
        b = round(bkz, 2)
        
        output_folder1 = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/Video/a{a}b{b}'
        os.makedirs(output_folder1, exist_ok=True)

        for Name in FileName:
            image_folder = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a{a}b{b}/{Name}'
        
            # 設置輸出的動畫檔案名稱
            video_name = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/Video/a{a}b{b}/{Name}.mp4'
            
            # 取得文件夾中所有以 "fig" 開頭的圖片
            images = [img for img in os.listdir(image_folder) if img.startswith("fig")]
            images.sort(key=lambda x: int(x.replace("fig", "").replace(".png", "")))  # 使用數字進行排序
            
            # 設置動畫的尺寸和幀率
            frame = cv2.imread(os.path.join(image_folder, images[0]))
            height, width, layers = frame.shape
            # video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))
        
            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
            
            # 將所有圖片添加到動畫中
            for image in images:
                video.write(cv2.imread(os.path.join(image_folder, image)))
            
            cv2.destroyAllWindows()
            video.release()
            
            print(f'Animation saved as {video_name}')

# # ==========================#
# # 'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a0.0b0.0/SurfaceVel'
# def create_video_from_images(input_folder, output_file, file_prefix):
#     image_files = [f for f in os.listdir(input_folder) if f.startswith(file_prefix) and f.endswith(('.png', '.jpg', '.jpeg'))]

#     if not image_files:
#         print(f"No {file_prefix} images found in the folder.")
#         return

#     image_files.sort(key=lambda x: int(x[len(file_prefix):-4]))

#     first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
#     height, width, layers = first_image.shape

#     video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

#     for image_file in image_files:
#         image_path = os.path.join(input_folder, image_file)
#         img = cv2.imread(image_path)
#         video.write(img)

#     cv2.destroyAllWindows()
#     video.release()

# if __name__ == "__main__":
#     input_folder = "E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a0.0b0.0/SurfaceVel"
#     output_file = "E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a0.0b0.0/SurfaceVel/output.mp4"
#     file_prefix = "fig"  # Change this to match your file prefix

#     create_video_from_images(input_folder, output_file, file_prefix)
