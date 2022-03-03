import os
import random
trainval_percent = 0.1
train_percent = 0.9
xml_file_path = '../label'
txt_save_path = '../image'
total_xml = os.listdir(xml_file_path)
num = len(total_xml)
list = range(num)
# 0.1*num
tv = int(num * trainval_percent)  #验证

#0.1*num*0.9
tr = int(tv * train_percent)

trainval = random.sample(list, tv)  # 0.1
train = random.sample(trainval, tr)  

ftrainval = open('../ImageSets/trainval.txt', 'w')
ftest = open('../ImageSets/test.txt', 'w')
ftrain = open('../ImageSets/train.txt', 'w')
fval = open('../ImageSets/val.txt', 'w')
for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval: #总数0.1
        ftrainval.write(name)
        if i in train:
            ftest.write(name)  #num*0.1*0.9
        else:
            fval.write(name)   #0.1
    else:
        ftrain.write(name)
        
ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
print("ok")