import pymysql.cursors
import datetime

dt=datetime.datetime.now()
dt_now=dt.strftime('%Y-%m-%d %H:%M:%S')
# date_now=dt.strftime('%Y-%m-%d')
# time_now=time.strftime('%H:%M:%S',time.localtime())

class rgnz_db():
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='971221',
            db='face_rgnz',
            charset='utf8'
        )

        # 获取游标
        self.cursor = self.connect.cursor()

    # 插入数据
    def insertUser(self,icon,name,acc,pwd):#,clas
        sql = "INSERT INTO original_web_user (user_icon, user_name, account,password,u_rgst_time,uc_class_id)" \
              " VALUES ( '%s', '%s', '%s','%s','%s','%s')"

        data = (icon, name, acc,pwd,dt,'4')
        self.cursor.execute(sql % data)
        self.connect.commit()
        print('成功插入', self.cursor.rowcount, '条数据')

    # 查询数据
    def acquireUser(self,acc):
        sql = "SELECT user_name,password FROM original_web_user WHERE account = '%s' "
        data = (acc)
        self.cursor.execute(sql % data)
        for row in self.cursor.fetchall():
            print("user_name:%s\tpassword:%s" % row)
        print('共查找出', self.cursor.rowcount, '条数据')



if __name__=='__main__':
    a=rgnz_db()
    # a.insertUser('test.icon','test1','acc1','pwd1')
    a.acquireUser('testAccount')

#     # 修改数据
#     def updateUser(self):
#         sql = "UPDATE trade SET saving = %.2f WHERE account = '%s' "
#         data = (8888, '13512345678')
#         self.cursor.execute(sql % data)
#         self.connect.commit()
#         print('成功修改', self.cursor.rowcount, '条数据')
#

#
# # 删除数据
#     def deleteUser(self):
#         sql = "DELETE FROM trade WHERE account = '%s' LIMIT %d"
#         data = ('13512345678', 1)
#         self.cursor.execute(sql % data)
#         self.connect.commit()
#         print('成功删除', self.cursor.rowcount, '条数据')



# # 事务处理
# sql_1 = "UPDATE trade SET saving = saving + 1000 WHERE account = '18012345678' "
# sql_2 = "UPDATE trade SET expend = expend + 1000 WHERE account = '18012345678' "
# sql_3 = "UPDATE trade SET income = income + 2000 WHERE account = '18012345678' "
#
# try:
#     cursor.execute(sql_1)  # 储蓄增加1000
#     cursor.execute(sql_2)  # 支出增加1000
#     cursor.execute(sql_3)  # 收入增加2000
# except Exception as e:
#     connect.rollback()  # 事务回滚
#     print('事务处理失败', e)
# else:
#     connect.commit()  # 事务提交
#     print('事务处理成功', cursor.rowcount)
#
# # 关闭连接
# cursor.close()
# connect.close()