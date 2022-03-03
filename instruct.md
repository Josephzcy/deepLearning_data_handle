
#### win10 使用darknet,yolov4 训练防外破数据 并使用C++ 调用训练的模型

#### darknet环境依赖安装和编译

##### 显卡驱动、CUDA、cudnn版本
* 参考：https://blog.csdn.net/qq_40927867/article/details/114932095
1. 确定Cuda版本和显卡驱动的关系
2. 确定显卡确定支持的最大Cuda 版本
3. 安装Cuda和Cudnn 并进行验证
4. 安装opencv
5. 编译darknet.sln(release、X64)
6. 测试模型
    打开cmd进入\darknet-master\build\darknet\x64目录,输入以下命令：
```python
.\darknet.exe detector test data/coco.data cfg/yolov4.cfg backup/yolov4.weights
```
#### 数据处理
* 参考：https://blog.csdn.net/qq_28663849/article/details/107362445
* 原始数据路径
    1. image:4030
    2. label:intruder
* 样本划分--devided.py--数据的文件名列表，对应的是图片的编号==>ImageSets
    * 训练集—train.txt：num*90%
    * 训练测试集-test.txt：num*0.1*0.9
    * 验证集-val.txt：num*0.1*0.1

* 样本格式转化--labelorder==>ImagePath
    * xml 转化为 txt:每张图片包含的目标类别和目标的bbox
    * train.txt:训练集中每张图片的绝对路径
    * test.txt:训练测试集中每张图片的路径
    * val.txt:验证集中每张图片的路径

* 准备数据
    1. voc.data
    2. voc.names
    3. 修改cfg/yolov4-custom.cfg
    4. 将图片对应的xml和图片放在同一层目录下

#### 训练模型
```python
.\darknet.exe detector train data\voc.data cfg\yolov4-custom.cfg data\yolov4.conv.137
```
##### C++ 调用检测到的模型

1. 新建VS工程
2. 配置opencv路径
3. 将opencv_world345.dll、pthreadGC2.dll、pthreadVC2.dll以及编译darknet产生的yolo_cpp_dll.dll放在源文件同一级目录下
4. 加载训练的配置文件和训练好的权重文件(源文件文件夹中)
    example：config/voc.data、voc.names、yolov4-custom.cfg、yolov4-custom_last.weights
5. 源代码如下
`注意`:编译的时候可yolo_v2_class.hpp能会报错
* eg: error C4996: 'sprintf': This function or variable may be unsafe. Consider using sprintf_s instead. To disable deprecation, use _CRT_SECURE_NO_WARNINGS.
* 解决办法：
 * 在预编译出添加下面一行：#pragma warning(disable:4996)


```C++
#include <iostream>
#define OPENCV      // 启用opencv
#define GPU         // 启用GPU
#include "yolo_v2_class.hpp"
#include <opencv2/opencv.hpp>	
void draw_boxes(cv::Mat mat_img, std::vector<bbox_t> result_vec, std::vector<std::string> obj_names,
	int current_det_fps = -1, int current_cap_fps = -1)
{
	int const colors[6][3] = { { 1,0,1 },{ 0,0,1 },{ 0,1,1 },{ 0,1,0 },{ 1,1,0 },{ 1,0,0 } };
	for (auto &i : result_vec)
	{
		cv::Scalar color = obj_id_to_color(i.obj_id);
		cv::rectangle(mat_img, cv::Rect(i.x, i.y, i.w, i.h), color, 2);
		if (obj_names.size() > i.obj_id)
		{
			std::string obj_name = obj_names[i.obj_id];
			if (i.track_id > 0) obj_name += " - " + std::to_string(i.track_id);
			cv::Size const text_size = getTextSize(obj_name, cv::FONT_HERSHEY_COMPLEX_SMALL, 1.2, 2, 0);
			int const max_width = (text_size.width > i.w + 2) ? text_size.width : (i.w + 2);
			cv::rectangle(mat_img, cv::Point2f(std::max((int)i.x - 1, 0), std::max((int)i.y - 30, 0)),
				cv::Point2f(std::min((int)i.x + max_width, mat_img.cols - 1), std::min((int)i.y, mat_img.rows - 1)),
				color, CV_FILLED, 8, 0);
			putText(mat_img, obj_name, cv::Point2f(i.x, i.y - 10), cv::FONT_HERSHEY_COMPLEX_SMALL, 1.2, cv::Scalar(0, 0, 0), 2);
		}
	}
}

std::vector<std::string> objects_names_from_file(std::string const filename)
{
	std::ifstream file(filename);
	std::vector<std::string> file_lines;
	if (!file.is_open()) return file_lines;
	for (std::string line; getline(file, line);) file_lines.push_back(line);
	std::cout << "object names loaded \n";
	return file_lines;
}
#include <io.h>
void getFileNames(std::string path, std::vector<std::string>& files)
{
	//文件句柄
	//注意：我发现有些文章代码此处是long类型，实测运行中会报错访问异常
	intptr_t hFile = 0;
	//文件信息
	struct _finddata_t fileinfo;
	std::string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			//如果是目录,递归查找
			//如果不是,把文件绝对路径存入vector中
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFileNames(p.assign(path).append("\\").append(fileinfo.name), files);
			}
			else
			{
				files.push_back(p.assign(path).append("\\").append(fileinfo.name));
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}


int main()
{
	std::string  names_file = "./config/voc.names";
	std::string  cfg_file = "./config/yolov4-custom.cfg";
	std::string  weights_file = "./config/yolov4-custom_last.weights";

	
	Detector detector(cfg_file, weights_file);
	float thresh = 0.1;          //阈值过小可能导致目标检测不到
	std::string imagePath = "./testImage";
	std::vector<std::string> imageNames;
	getFileNames(imagePath, imageNames);

	for (auto& image_file : imageNames) {
	
		cv::Mat image = cv::imread(image_file);
		std::vector<bbox_t> result_vec = detector.detect(image_file, thresh);

		for (std::vector<bbox_t>::iterator iter = result_vec.begin();iter != result_vec.end();iter++){
			cv::Rect rect(iter->x, iter->y, iter->w, iter->h);
			cv::rectangle(image, rect, cv::Scalar(255, 0, 0), 2);
		}
		
		cv::imshow("result", image);
		cv::waitKey(0);

	}

	return 0;
}

```

##### C++ 模型检测效果评价
* 检测的准确率
* 检测的实时性