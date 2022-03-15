import os
import numpy as np
import shutil
def read_file_list(file_folder):  
  file_list=[]
  if os.path.exists(file_folder):
    for file_name in os.listdir(file_folder):
        file_path = os.path.join(file_folder,file_name)    
        file_list.append(file_path) 
  return file_list


pre_info_folder="../results/0.5/"
pre_filter_info_folder="../results/filter/"
prob_thres=0.3

  
if __name__=='__main__':
  pre_file_list=read_file_list(pre_info_folder)
  for pre_file in pre_file_list:
    new_file_name=pre_file[pre_file.rfind("/"):]
    pre_filter_info=open(pre_filter_info_folder+new_file_name,"w")
    with open(pre_file)as pre_gt_f:
      pre_info=pre_gt_f.readlines()
      for pre_info_single in pre_info:
        pre_info_single_list=pre_info_single.split()
        probality=float(pre_info_single_list[1])
        if probality < prob_thres:
          continue
        pre_info_single_list.pop(1)
        print(pre_info_single_list)
        for item in pre_info_single_list:
          if item!=pre_info_single_list[len(pre_info_single_list)]:
            pre_filter_info.write(item+" ")
        # [pre_filter_info.write(item) for item in pre_info_single_list]
       
      pre_filter_info.close()
    break  
  pass