
#### 训练模型
.\darknet.exe detector train marking\data\voc.data marking\data\yolov4-custom.cfg marking\data\yolov4.conv.137 | tee training.log


#### 网络mAP

1. 

#### 生成网络预测结果
1. .\darknet.exe detector valid marking\data\voc.data marking\data\yolov4-custom.cfg marking\data\backup\yolov4-custom_last.weights -thresh 0.25
3. https://blog.csdn.net/qq_33193309/article/details/108453810
4. 
#### 评价网络

python reval_voc_py3.py 
参数：
devkit_path, year, image_set, classes, output_dir = 'results'

|   devkit_path   | year | image_set | classes | output_dir | 
|:---------------------:|:------:|------------:|----------:|-------------:|
|   xml       | 2007 |test.txt   | classes_path | output_dir | 