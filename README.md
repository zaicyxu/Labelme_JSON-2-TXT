# Labelme_JSON-2-TXT
Labelme_JSON 2 TXT
# Background

Image files annotated by the labeling software *labelme*. Each image corresponds to a json file with the same name. In order to convert it into data that can be used for YOLO training, special conversion is required. This conversion process is different from the conversion of **MaskRCNN**, so it needs to be recorded separately.

# Step 1

Use Labelme to label the data to be processed and store the corresponding json data, the labelme software as below:

[]()

# Step 2

Coding as below:

```python
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
```

Tips:

1. 必须要在处理.bmp图片并统一图片尺寸之后方能归一化操作。
2. 注意标签与YOLO数据标签之间的转换， yolo的标签是从0开始的。
3. .json2.txt并不是简单的把json信息写入txt而是需要把位置信息归一化操作，这样才能保证位置的绝对不变。
4. 归一化操作的时候，如果图片未进行统一尺寸，则在归一化阶段x, y轴坐标除以的是      #image_width = json_data['imageWidth']
#image_height = json_data['imageHeight']，反之如果统一尺寸了则需要除以一个规定的长宽数值。
