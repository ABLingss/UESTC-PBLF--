import os
import subprocess

# 获取当前目录下的所有文件
files = os.listdir('.')

# 遍历文件
for file in files:
    # 检查文件是否是.ui文件
    if file.endswith('.ui'):
        # 构建输出的.py文件名
        output_file = file[:-3] + '.py'

        # 调用pyuic命令行工具
        subprocess.run(['pyuic5', '-o', output_file, file], check=True)

print("转换完成。")