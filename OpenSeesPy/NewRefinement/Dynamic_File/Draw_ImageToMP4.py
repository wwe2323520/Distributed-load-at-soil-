# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 18:12:13 2024

@author: User
"""

import cv2
import os
import re

# 自然排序的函數，處理小數格式
def natural_sort_key(s):
    return [float(text) if text.replace(".", "", 1).isdigit() else text for text in re.split(r'(\d+\.\d+)', s)]

def images_to_video(image_folder, output_video, fps):
    # 取得所有符合命名規則的圖片檔案
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    
    # 根據命名順序排序圖片 (例如: 1.0000, 1.0001, ..., 1.0999)
    images = sorted(images, key=natural_sort_key)

    # 確保有圖片
    if not images:
        print("No images found in the folder.")
        return

    # 讀取第一張圖片來獲取尺寸
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = first_image.shape

    # 設定影片寫入參數
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 格式
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # 將每張圖片加入影片中
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # 釋放 video 物件
    video.release()
    print(f"Video saved as {output_video}")

# 呼叫函數進行圖片轉換影片
if __name__ == "__main__":
    # 輸入圖片資料夾路徑
    image_folder = 'D:/shiang/opensees/20220330/OpenSeesPy/IMAGE/C5_W10_Rocking(Tie 40HZ)'
    
    # 輸入影片輸出路徑和名稱
    output_folder = 'D:/shiang/opensees/20220330/OpenSeesPy/IMAGE/Video' 
    output_video_name = 'output_video.mp4'
    output_video = os.path.join(output_folder, output_video_name)
    
    # 設置幀率
    fps = 5  # 可以調整幀率

    # 呼叫函數
    images_to_video(image_folder, output_video, fps)
