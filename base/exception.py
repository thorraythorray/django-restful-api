class ParamsError(Exception):
    def __init__(self, error_msg="Params error", error_code=400):
        self.error_code = error_code
        self.error_msg = error_msg  
    def __str__(self):
        return "err_code is {}, err_msg is {}".format(self.error_code, self.error_msg)

class AuthError(Exception):
    def __init__(self, error_msg, error_code=401):
        self.error_code = error_code
        self.error_msg = error_msg  
    def __str__(self):
        return "err_code is {}, err_msg is {}".format(self.error_code, self.error_msg)