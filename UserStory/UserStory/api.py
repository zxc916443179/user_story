from django.http import HttpResponse, HttpResponseBase
import json
import functools
from inspect import getargspec
from django.shortcuts import render
import traceback as tb
def APIFunction(func, *args, **kwargs):
    @functools.wraps(func, *args, **kwargs)
    def function(request, *args, **kwargs):
        params = {}
        if request.method == 'POST':
            if request.body != b'' :
                params = json.loads(request.body)
            
            session = request.session
            params = dict(params)
            params['session'] = session
            if not session.__contains__('user_session') and request.path not in ('/index/log_in/', '/index/log_up/', '/index/'):
                return APIResponse(code=203, msg=RETCode[203])
            else:
                params['session'] = request.session
            co_varnames = getargspec(func).args
            if 'args' not in co_varnames and 'kwargs' not in co_varnames:
                for var in co_varnames:
                    if not params.__contains__(var):
                        return APIResponse(code=102, msg=RETCode[102])
        elif request.method == 'GET':
            params = request
        try:
            if request.method == 'POST':
                res = func(**params)
                if params['session'].__contains__('user_session') and params['session']['user_session'] is not None:
                    request.session['user_session'] = params['session']['user_session']
                else:
                    request.session.clear()
            elif request.method == 'GET':
                res = func(params)
            

            if not isinstance(res, HttpResponseBase):
                try:
                    res_json = {}
                    res_json.update(res.__dict__)
                    res = res_json
                    del res['_state']
                except Exception as e:
                    pass
                return APIResponse(content=res, code=0)
            else:
                print(res)
                return res
        except Exception as e:
            print(tb.format_exc())
            if isinstance(e, APIError):
                return APIResponse(code=e.code, msg=e.desc)
            return APIResponse(code=101, msg=RETCode[101])
    return function

class APIResponse(HttpResponse):
    def __init__(self, content='', code=0, msg='', *args, **kwargs):
        super().__init__(content=content, content_type='application/json', *args, **kwargs)
        self.content = json.dumps({'body': content, 'code': code, 'msg': msg})

class APIError(Exception):
    def __init__(self, code=0, desc=None, *args, **kwargs):
        if desc is None:
            desc = RETCode[code]
        self.code = code
        self.desc = desc

RETCode = {
    100: '操作成功',

    101: '未知错误',
    102: '请求参数不匹配',

    201: '用户名不存在',
    202: '密码错误',
    203: '未登录'
}
@APIFunction
def Hello(id, session):
    print(id)
    return 'hello world'

def test_socket(request):
    return render(request, "test.html")