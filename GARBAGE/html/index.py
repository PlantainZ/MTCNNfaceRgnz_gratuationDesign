import sys
sys.path.append('./cherrypy')
import json
import cherrypy
import serverConf as conf


class HelloWorld(object):
    def __init__(self):
        self.web_dir=r'C:\XXXX_CodeRepository\facenet_facerecognition\html\page'

    @cherrypy.expose
    def index(self):
        return '多多多和TensorFlow永结同心！！'

    @cherrypy.expose
    def home(self):        #注意这个open()函数是有缺陷的，后边必须是'rb'否则报错
        fo=open(self.web_dir + r'\home.html','rb')
        try:
            html=fo.read()
        finally:
            fo.close()
        return html

    @cherrypy.expose
    def register(self):  # 注意这个open()函数是有缺陷的，后边必须是'rb'否则报错
        fo = open(self.web_dir + r'\register.html', 'rb')
        try:
            html = fo.read()
        finally:
            fo.close()
        return html

    # 转接人员显示界面
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def showClerkManage(self, json_str):
        print(" json test!!:")
        json_obj = json.loads(json_str)
        if json_obj['userName']=='吞日月里洗澡':
            fo = open(self.web_dir + r'\clerkManage.html', 'rb')
            try:
                html = fo.read()
            finally:
                fo.close()
            return html
        else:
            print("失败！userName=%s" % (json_obj['userName']))
            print("jsonEnd!!!!")
            resp = {'status': 'false'}
            resp['user_id'] = 8000
        return resp

    @cherrypy.expose
    def login(self):  # 注意这个open()函数是有缺陷的，后边必须是'rb'否则报错
        fo = open(self.web_dir + r'\login.html', 'rb')
        try:
            html = fo.read()
        finally:
            fo.close()
        return html






    @cherrypy.expose
    def regist(self):  # 注意这个open()函数是有缺陷的，后边必须是'rb'否则报错
        fo = open(self.web_dir + r'\register.html', 'rb')
        try:
            html = fo.read()
        finally:
            fo.close()
        return html

    #登陆按钮的反应
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def loginClick(self,json_str):
        print(" json test!!:")
        json_obj=json.loads(json_str)
        print("保存用户！userName=%s,pwd=%s" %(json_obj['userName'],json_obj['pwd']))
        print("jsonEnd!!!!")
        resp={'status':'ok'}
        resp['user_id']=8008
        return resp

if __name__=='__main__':
    cherrypy.config.update({
        'server.socket_host':'127.0.0.1',
        'server.socket_port':8090,
    })
    cherrypy.quickstart(HelloWorld(),'/','statiConf.conf')