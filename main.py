# -*- coding: utf-8 -*-
"""main

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18dbTnkJsdWSlI9IqAvKFQfdXcsxq9CwU
"""

import os
import numpy as np
import json

def json2txt(path_json, path_txt):
    with open(path_json, 'r', encoding='gb18030') as json_file:
        json_data = json.load(json_file)

        # image_width = json_data['imageWidth']
        # image_height = json_data['imageHeight']
        image_width = 3072
        image_height = 3072

        with open(path_txt, 'w') as txt_file:
            for shape in json_data['shapes']:
                xy = np.array(shape['points'])
                label = str(shape['label'])

                # Convert labels: "1" -> "0", "2" -> "1"
                if label == '1':
                    label = '0'
                elif label == '2':
                    label = '1'

                # Normalize
                normalized_xy = [(x / image_width, y / image_height) for x, y in xy]

                line = label + ' ' + ' '.join([f"{x:.6f} {y:.6f}" for x, y in normalized_xy]) + "\n"
                txt_file.write(line)

def process_directory(dir_json, dir_txt):
    if not os.path.exists(dir_txt):
        os.makedirs(dir_txt)

    list_json = os.listdir(dir_json)
    for cnt, json_name in enumerate(list_json):
        if json_name.endswith('.json'):
            print(f'Processing file {cnt + 1}/{len(list_json)}: {json_name}')
            path_json = os.path.join(dir_json, json_name)
            path_txt = os.path.join(dir_txt, json_name.replace('.json', '.txt'))
            json2txt(path_json, path_txt)

dir_json = r'D:\work\DATA\slide_data\train_data'
dir_txt = r'D:\work\DATA\slide_data\train_data_txt'

process_directory(dir_json, dir_txt)