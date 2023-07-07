import os
import requests
import base64
import time
import argparse

print('''
 _    _____                                     
| |__|___ / _ __   __ _ _   _  __ _ _ __   __ _ 
| '_ \ |_ \| '_ \ / _` | | | |/ _` | '_ \ / _` |
| |_) |__) | | | | (_| | |_| | (_| | | | | (_| |
|_.__/____/|_| |_|\__, |\__,_|\__,_|_| |_|\__, |
                  |___/                   |___/ 
脚本，启动！！！！
''')

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True, help='输入文件夹路径')
args = parser.parse_args()

# 设置 API 密钥
api_key = ''
api_secret = ''

# 遍历文件夹中的图像文件
for root, dirs, files in os.walk(args.f):
    for file_name in files:
        file_path = os.path.join(root, file_name)

        # 读取文件并进行处理
        with open(file_path, 'rb') as file:
            image_data = file.read()
            image_64_encode = base64.b64encode(image_data).decode("utf-8")

            data = {
                "parameter": {
                    "version": "1.0.0"
                },
                "extra": {},
                "media_info_list": [{
                    "media_data": image_64_encode,
                    "media_profiles": {
                        "media_data_type": "jpg"
                    }
                }]
            }

            target = f"https://openapi.mtlab.meitu.com/v1/hairclassifier?api_key={api_key}&api_secret={api_secret}"
            response = requests.post(url=target, json=data, timeout=5)
            result_json = response.json()
            name_value = result_json["media_info_list"][0]["media_extra"]["hairClassifier"][0]["hair_type"][0]["type"]

            if name_value == 6:
                print(f"File: {file_path}, 不错!")
            elif name_value == 5:
                print(f"File: {file_path}, 狂魔警告!")
            else:
                print(f"File: {file_path}, 退学吧!")

        #停止2秒
        time.sleep(2)
