from django.http import HttpResponse
import json
import functools

def APIFunction(func, *args, **kwargs):
    @functools.wraps(func, *args, **kwargs)
    def function(request, *args, **kwargs):
        params = {}
        if request.method == 'POST':
            params = request.POST
        elif request.method == 'GET':
            params = request.GET
        if 'args' not in func.__code__.co_varnames and 'kwargs' not in func.__code__.co_varnames:
            for var in func.__code__.co_varnames:
                if not params.__contains__(var):
                    return APIResponse(code=102, msg=RETCode[102])
        try:
            res = func(**params)
            return APIResponse(content=res, code=0)
        except Exception as e:
            print('error', e)
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
    102: '请求参数不匹配'
}
@APIFunction
def Hello(id):
    print(id)
    return 'Hello world'