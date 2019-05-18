clerkRecord=r'.\clerkRecord.txt'
nowRecord=r'.\nowRecord.txt'

class writeRecord():

    def __init__(self):
        print('文件读写实例启动。')

    def readAllRecord(self,fileName):
        f = open(fileName)
        record=[]
        for line in f:
            record.append(line)
            print(line)
        return record

    def addRecord(self,fileName,recordStr):
        with open(fileName, 'a+') as f:
            f.write(recordStr + '\n')
            print("写入"+recordStr+"成功~")




# 测试部分

# with open(clerkRecord,'w+') as f1, open(nowRecord,'w+') as f2:
#   f1.write('123')
#   f2.write('456')
# test=writeRecord()
# test.addRecord()
# test.readAllRecord()

