import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
from itertools import groupby
sets = ['train', 'trainval']
classes = ["arrow_left","arrow_right","arrow_straight","arrow_straight_left","arrow_straight_right","crosswalk_warning"]
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
def convert_annotation(image_id):
    
    in_file = open('../annotation/%s.xml' % (image_id),encoding='utf-8')
    out_file = open('../imageSets/%s.txt' % (image_id), 'w')
    # in_file = open('../2.xml' )

    tree = ET.parse(in_file)
    root = tree.getroot()
    file_name = root.find('path')
    # if str(image_id) not in file_name.text:
    #     print("error image_id, imagepath", image_id, file_name.text)
    if ".png" in file_name.text:
        a=file_name.text.rfind('\\')
        file_name.text = file_name.text[file_name.text.rfind('\\'):]
        file_name.text = "..\\image\\" + image_id + ".jpg"
        img = cv2.imread(file_name.text)
        w = (img.shape)[1]
        h = (img.shape)[0]
    else:
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        ss = [''.join(list(g)) for k, g in groupby(cls, key=lambda x: x.isdigit())][0]
        if ss.endswith("_"):
            cls=ss[0:-1]
        
        
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
wd = getcwd()
print(wd)

for image_set in sets:
    if not os.path.exists('C:\\yolov4\\darknet\\build\\darknet\\x64\\marking\\data\\imagePath\\'):
        os.makedirs('../imagePath\\')
    image_ids = open('../sample_divided/%s.txt' % (image_set)).read().strip().split()
    list_file = open('../ImagePath/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('C:\\yolov4\\darknet\\build\\darknet\\x64\\marking\\data\\imageSets\\%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
