# 导入pymysql模块
import pymysql
import datetime
import check_record

dt=datetime.datetime.now()
dt_now=dt.strftime('%Y-%m-%d %H:%M:%S')
# 创建数据库操作类

# pplChangeFile=r"C:\XXXX_CodeRepository\GraduationDesign_exe\wxpy_exe\reference\example\clerkRecord.txt"
pplChangeFile=r'.\clerkRecord.txt'
class Sql_operation(object):
    '''
    数据库操作
    '''

    # 用构造函数实现数据库连接，并引入mydb参数，实现调用不同的数据库
    def __init__(self):
        # 实例变量, mydb
        # self.mydb = mydb
        # 打开数据库连接
        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='971221',
            db='face_rgnz',
            charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()
        self.writer=check_record.writeRecord()

    # 定义查看数据表信息函数，并引入table_field、table_name参数，实现查看不同数据表的建表语句
    def FindAll(self, table_name):
        # 实例变量
        self.table_name = table_name
        # 定义SQL语句
        sql = "select * from %s" % (self.table_name)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            data = self.cursor.fetchall()
            return data
        except Exception as err:
            print("SQL执行错误，原因：", err)

    # 定义添加表数据函数
    def Insert(self, icon,name,account,pwd,classid,note):
        # 实例变量
        self.user_icon = icon
        self.user_name = name
        self.account = account
        self.pwd = pwd
        self.classid = classid
        self.note = note
        # 定义SQL语句
        sql = "insert into original_web_user(user_icon,user_name,account,password,u_rgst_time,uc_class_id,note)" \
              " values('%s','%s','%s','%s','%s','%s','%s')" % (
        self.user_icon, self.user_name, self.account, self.pwd, dt, self.classid,self.note)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.writer.addRecord(pplChangeFile,r"注册___【%s】:账户【%s】,用户名【%s】注册成功。" %(dt,self.account,self.user_name))
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def Update(self,usr_name,usr_acc,usr_pwd,usr_class):
        sql = "update original_web_user set user_name = '"+usr_name+"' "+\
              ",password='"+usr_pwd+"' "+\
                ",uc_class_id='"+usr_class+"' "+\
                "where account='"+usr_acc+"'"
        effect_row = self.cursor.execute(sql)
        self.writer.addRecord(pplChangeFile, r"更新___【%s】:账户【%s】,用户名【%s】进行了更新。" % (dt, usr_acc,usr_name))
        print(effect_row)
        self.db.commit()

    def Search(self,usr_acc):
        sql="select * from original_web_user where account='"+usr_acc+"'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.db.commit()
        # print(result)
        return result



    # 定义删除表数据函数
    def Del(self, user_acc):
        # 实例变量
        self.user_acc = user_acc
        # 定义SQL语句
        # sql="DELETE FROM original_web_user WHERE account='" + user_acc + "'"
        sql = "delete from original_web_user where account='" + user_acc + "'"
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.writer.addRecord(pplChangeFile, r"删除___【%s】:账户【%s】,用户已删除。" % (dt, user_acc))
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 用析构函数实现数据库关闭
    def __del__(self):
        # 关闭数据库连接
        self.db.close()

if __name__=='__main__':
    db=Sql_operation()
    #插入测试
    # db.Insert('test.jpg','testName','testACC','testPWD','4','test_img_path')

    # 枚举测试
    # data=db.FindAll('original_web_user')
    # for i in data:
    #     print(i[3],i[4])

    # 删除测试
    db.Del('zhexingchen')

    #更新测试
    #self,usr_name,usr_acc,usr_pwd,usr_class
    # db.Update('折星辰','zhexingchen','zhexingchenNNN','11')

    #指定字段：account，查询测试
    # tmp=db.Search('rufengfeng')
    # print(tmp)