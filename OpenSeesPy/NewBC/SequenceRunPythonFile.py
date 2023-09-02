# import os
# ------ run 1 opensees then -> run 1 pvdfolat file ------------
# # os.system("python ./1.py")
# # os.system("python ./1pvd64.py")

# os.system("python ./1.py")
# os.system("python ./2.py")

# --------- ChatGPT Code (run 5 patch code)-----------------------
# import os
# import subprocess

# # 定義五組程式名稱和參數
# programs = [
#     "python first_program.py",   # 第一組程式
#     "python second_program.py",  # 第二組程式
#     "python third_program.py",   # 第三組程式
#     "python fourth_program.py",  # 第四組程式
#     "python fifth_program.py"    # 第五組程式
# ]

# # 偵測生成的資料夾
# output_folders = [
#     "output_folder_1",  # 替換成第一組程式生成的資料夾路徑
#     "output_folder_2",  # 替換成第二組程式生成的資料夾路徑
#     "output_folder_3",  # 替換成第三組程式生成的資料夾路徑
#     "output_folder_4",  # 替換成第四組程式生成的資料夾路徑
#     "output_folder_5"   # 替換成第五組程式生成的資料夾路徑
# ]

# # 替換的文字
# old_text = "float32"
# new_text = "float64"

# # 處理五組動作
# for i in range(5):
#     # 執行程式
#     subprocess.run(programs[i], shell=True)

#     # 檢查資料夾是否存在
#     if os.path.exists(output_folders[i]) and os.path.isdir(output_folders[i]):
#         # 列出資料夾中的所有txt檔案
#         txt_files = [f for f in os.listdir(output_folders[i]) if f.endswith(".txt")]

#         # 逐一處理txt檔案
#         for txt_file in txt_files:
#             file_path = os.path.join(output_folders[i], txt_file)

#             # 讀取檔案內容
#             with open(file_path, 'r') as f:
#                 content = f.read()

#             # 將float32替換為float64
#             modified_content = content.replace(old_text, new_text)

#             # 寫回修改後的內容
#             with open(file_path, 'w') as f:
#                 f.write(modified_content)

#         print(f"第 {i+1} 組動作完成。")
#     else:
#         print(f"第 {i+1} 組動作的資料夾不存在。")
