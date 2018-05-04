# -*- coding: utf-8 -*-

################################################################################
#
#
# Copyright(c) 2017, WeSmart Artificial Intelligent Co.Ltd, All rights reserved.
# 
#
# Description: 
#   run app
# Author: Fu adon
# Versions: 
#     Created by Fu adon on 2017/12/14 下午10:13 for version 1.0
#     Modified by Fu adon on 2017/12/14 下午10:13 form version 1.0
#
################################################################################

import settings
from werkzeug.wrappers import Response
from flask.views import View
from flask import Flask, url_for, request, redirect, render_template, make_response, jsonify

from application import user


"""
创建实例app，接收包或模块的名字作为参数，一般都传递__name__;
可以让flask.helpers.get_root_path函数通过传入这个名字确定程序的根目录，
以便获得静态文件和模板文件的目录。
Flask类实现了一个wsgi应用
"""
app = Flask(__name__, template_folder='templates')
app.register_blueprint(user.user_bp)

"""
配置管理
app.config['DEBUG'] = True
app.config.update(DEBUG=True, SECRET_KEY='...')
app.config.from_object('settings')  # 通过字符串的模块名字
# 默认配置文件不存在时会抛异常，使用silent=True只返回False，但不抛异常
app.config.from_pyfile('settings.py', silent=True)
# > export SETTINGS='settings.py'
app.config.from_envvar('SETTINGS')  # 通过环境变量加载，获取路径后调用from_pyfile方式加载
"""
app.config.from_object(settings)        # 引用模块，然后导入模块对象


"""
app.route装饰器会將URL和执行的视图函数的关系保存到app.url_map属性上;
处理URL和视图函数的关系的程序就是路由;
wesmart就是视图函数;
"""


@app.route('/')
def wesmart():
    return {'message': "we smart!"}


# 响应response: (response, status, headers)
@app.route('/custom_headers')
def headers():
    return {'headers': [1, 2, 3]}, 201, [('X-Request-Id', '100')]


# 动态URL规则
@app.route('/article/<iid>')
def article(iid):
    return "Item:{}".format(iid)


# /article?page_name=1 or /blog?page_name=1
@app.route('/<any(article, blog):page_name>')
def item(url_path):
    print type(url_path), url_path
    return url_path


@app.route('/people/', methods={'POST', 'GET'})
def people():
    name = request.args.get('name')
    if not name:
        return redirect(url_for('login'))
    user_agent = request.headers.get('User-Agent')
    return 'Name: {0}; UA: {1}'.format(name, user_agent)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return 'User: {} login'.format(user_id)
    else:
        return 'Open Login page'


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    return resp


with app.test_request_context():
    print "use url_for to build url>>>"
    print url_for('article', iid='1')


class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)


class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != 'GET':
            return 'UNSUPPORTED!'

        context = {'users': self.get_users()}
        return self.render_template(context)


class UserView(BaseView):
    def get_template_name(self):
        return 'users.html'

    def get_users(self):
        return [{
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
        }]

app.add_url_rule('/users', view_func=UserView.as_view('userview'))

"""
if 语句可以保证当其他文件引用此文件时不会执行这个判断内的代码;
比如from app_server import app，不会执行app.run函数;
"""
if __name__ == '__main__':
    """
    app.run(debug=True),run时开启调试模式
    或者
    app.debug = True
    不能用于生产环境中
    """
    app.debug = app.config.get('DEBUG', False)  # 开启调试模式

    app.response_class = JSONResponse

    """
    app.run启动服务;
    默认Flask只监听本地IP：127.0.0.1,端口为5000;若指定转发端口8788,需要指定host和port参数;
    0.0.0.0表示监听所有地址;
    服务启动后会调用werkzeug.serving.run_simple进入轮询，
    默认使用单进程单线程的werkzeug.serving.BaseWSGIServer处理请求，
    实际使用标准库BaseHTTPServer.HTTPServer,通过select.select做0.5秒的'while True'的事件轮询。

    当访问‘http://0.0.0.0:8788/’，通过app.url_map找到注册的'/'这个URL模式,
    找到对应的wesmart函数执行，状态码200;若找不到对应的模式，状态码为404。

    默认的app.run的启动方式只适合调试，不要在生产环境中使用;
    生产环境应该使用Gunicorn或uWSGI。
    """
    app.run(host='0.0.0.0', port=8788)
