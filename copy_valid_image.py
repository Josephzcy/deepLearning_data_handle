
import shutil

if __name__=='__main__':
	# valid_txt_path="../ImagePath/val.txt"
	# valid_image_folder="../validImage/"
	# with open(valid_txt_path) as file_valid:
	#     valid_file_path=file_valid.read().split()
	#     for file_path in valid_file_path:
	#         file_name=file_path.split("\\")[-1]
	#         shutil.copyfile(file_path,valid_image_folder+file_name)
	# file_valid.close()

	train_valid_image_folder="../train_valid_image/"
	train_valid_txt_path="../sample_divided/trainval.txt"
	with open(train_valid_txt_path) as file_valid:
		valid_file_path=file_valid.read().split()
		for file_path in valid_file_path:
			file_name=file_path.split("\\")[-1]
			label_file_name=file_name.split(".")[0]+".txt"
			label_file_path=file_path.split(".")[0]+".txt"
			shutil.copyfile(file_path,train_valid_image_folder+file_name)
			# shutil.copyfile(file_path,train_valid_image_folder+label_file_name)

	file_valid.close()