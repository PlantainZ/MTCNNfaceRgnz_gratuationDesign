import shutil
#移除目录下所有文件
path=r'C:\XXXX_CodeRepository\GraduationDesign_exe\core_Rgnz\train_dir\usr_luzheng'
shutil.rmtree(path)


import os
# 选择相对路径
for i in os.listdir('..\..\..\core_Rgnz'):
    print(i)