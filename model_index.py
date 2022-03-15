import os
if __name__=='__main__':
  pass
 
# txt_file为配置文件.data中的valid
txt_file = '/home/share/liubo/darknet/yanhuo/eval.txt'
f = open(txt_file)
lines = f.readlines()
for line in lines:
    line = line.split('/')[-1][0:-5]
    # test_out_file 为转换后保存的结果地址
    test_out_file = '/home/share/liubo/darknet-yolov3/results/test_acc_yanhuo'
    # 下面3个with需要自己的修改，修改成自己对应的类别
    with open(os.path.join(test_out_file , line + '.txt'), "a") as new_f:
        f1 = open('/home/share/liubo/darknet-yolov3/results/comp4_det_test_smoke.txt', 'r')
        f1_lines = f1.readlines()
        for f1_line in f1_lines:
            f1_line = f1_line.split()
            if line == f1_line[0]:
                new_f.write("%s %s %s %s %s %s\n" % ('smoke', f1_line[1], f1_line[2], f1_line[3], f1_line[4], f1_line[5]))
    with open(os.path.join(test_out_file , line + '.txt'), "a") as new_f:
        f1 = open('/home/share/liubo/darknet-yolov3/results/comp4_det_test_white.txt', 'r')
        f1_lines = f1.readlines()
        for f1_line in f1_lines:
            f1_line = f1_line.split()
            # print(line.split('.')[0] + ' ' + f1_line[0])
            if line == f1_line[0]:
                new_f.write("%s %s %s %s %s %s\n" % ('white', f1_line[1], f1_line[2], f1_line[3], f1_line[4], f1_line[5]))
    with open(os.path.join(test_out_file , line + '.txt'), "a") as new_f:
        f1 = open('/home/share/liubo/darknet-yolov3/results/comp4_det_test_red.txt', 'r')
        f1_lines = f1.readlines()
        for f1_line in f1_lines:
            f1_line = f1_line.split()
            if line == f1_line[0]:
                new_f.write("%s %s %s %s %s %s\n" % ('red', f1_line[1], f1_line[2], f1_line[3], f1_line[4], f1_line[5]))