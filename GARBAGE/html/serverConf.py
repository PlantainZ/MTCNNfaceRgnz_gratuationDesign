import sys
sys.path.append('./cherrypy')
import cherrypy
from cherrypy.lib import auth_digest

g_users={'join':'123456'}

root_conf={'/':{
    'tools.staticdir.root':r'C:\XXXX_CodeRepository\facenet_facerecognition',
    'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
},

'/htmlSource':{
    'tools.staticdir.on':True,
    'tools.staticdir.dir':'htmlSource',
},

'/':{
    'tools.auth_digest.on':True,
    'tools.auth_digest.realm':'172.0.0.1',
    'tools.auth_digest.get_ha1':auth_digest.get_ha1_dict_plain(g_users),
    'tools.auth_digest.key':'a565c27146791cfb'
}#设置访问这个地址的时候，需要身份验证,账号密码就是g_users
    #是一个叫digest认证的东西，不需要我们做额外工作就能实现对资源的保护/


}