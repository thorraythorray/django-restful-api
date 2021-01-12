import requests
import json
import time
import traceback
from io import StringIO
from base.exception import ParamsError, AuthError
from django.http import HttpResponse
from base.log4 import log4app
from django.views.decorators.csrf import csrf_exempt,csrf_protect

class ApiAccessBase:
    _support_req_method = None
    _handler_util = None

    def __init__(self):
        self.request = ""
        self.__headers = ""

    @classmethod
    def as_api(cls):
        def func_exe(request):
            self = cls()
            self.request = request
            self.__headers = request.headers
            return self.req_logic_handler()
        return csrf_exempt(func_exe)

    @property
    def headers(self):
        return self.__headers
        
    @headers.setter
    def headers(self, new):
        if isinstance(new, dict):
            self.__headers = new

    def __get_req_body_params(self):
        req_args = {}
        body = self.request.body
        if body:
            params = body.decode("UTF-8").split("&")
            for p in params:
                key, value = p.split("=")
                if key == "data":
                    try:
                        value = json.loads(value)
                    except ValueError as e:
                        value = {}
                req_args[key] = value

    def req_logic_handler(self):
        if self.request.method == "POST":
            log4app.info("request data:{}".format(self.request.POST))
            self._handler_util.init_env(self.request)
            try:
                self._handler_util.check_workflow(self._support_req_method)

                target_func = getattr(self._handler_util, self._handler_util._method)
                func_params = self._handler_util._req_params
                flag, res = target_func(func_params)
                if flag:
                    resp_dict = self._handler_util._result_render(res)
                else:
                    resp_dict = self._handler_util._error_render("Api handler error!")
            except ParamsError as e :
                resp_dict = self._handler_util._error_render(e.error_msg, e.error_code)
            except AuthError as e :
                resp_dict = self._handler_util._error_render(e.error_msg, e.error_code)
            except Exception as e:
                except_trace = StringIO()
                traceback.print_exc(file=except_trace)
                log4app.error("Wrong access base api with exception.\nError: %s" % except_trace.getvalue())
                except_trace.close()
                resp_dict = self._handler_util._error_render("Api handler error")
            return HttpResponse(json.dumps(resp_dict), content_type="application/json")
        else:
            log4app.error("request method must be post!")
            return HttpResponse('did not get the attribute of data from request')
    

class ApiHandlerBase:
    _req_params = ""
    _method = ""
    _auth_user = ""
    _auth_token = ""

    def init_env(self, request):
        self._req_params = request.POST.get("data")
        self._method = request.POST.get("method")
        self._auth_user = request.POST.get("user")
        self._auth_token = request.POST.get("token")
    
    def __get_version(self):
        return "1.0"
    
    def __get_tiemstamp(self):
        return time.time()    
    
    def init_resp_content(self):
        return {
            "res": "",
            "data": {},
            "user": "",
            "method": "",
            "timestamp": self.__get_tiemstamp(),
            "version": self.__get_version()
        }

    def __fill_env(self):
        pass

    def _get_auth_obj(self):
        return ""

    def _auth_req(self):
        
        return True, ""
    
    def check_workflow(self, support_methods):
        if self._method in support_methods:
            per = support_methods.get("method")
            if per not in ["N"]:
                flag, user_obj = self._auth_req()
                if not flag:
                    raise AuthError("authenticated failed.")                
        else:
            raise ParamsError("method is not defined.")

    def _result_render(self, data):
        resp_dict = self.init_resp_content()
        resp_dict["res"] = "ok"
        resp_dict["data"] = data
        resp_dict["user"] = self._get_auth_obj()
        resp_dict["method"] = self._method
        return resp_dict
          
    def _error_render(self, err_msg, err_code=400, data=None):
        resp_dict = self.init_resp_content()
        resp_dict["res"] = "err"
        resp_dict["user"] = self._get_auth_obj()
        resp_dict["method"] = self._method
        resp_dict["err_msg"] = err_msg
        resp_dict["err_code"] = err_code
        if data:
            resp_dict["data"] = data
        return resp_dict
    






        


        










        


        


        


