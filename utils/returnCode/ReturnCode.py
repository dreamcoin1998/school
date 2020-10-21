"""
'修改状态码': '2020.04.15'
"""


class ResponseCode:

    code = 0
    msg = "ok."

    def __init__(self, data=None, msg=None, total=0, **kwargs):
        self.data = data
        if isinstance(data, list) or isinstance(data, tuple):
            self.total = len(self.data)
        else:
            self.total = total
        self.kwargs = kwargs
        self.msg = self.msg if msg is None else self.msg

    def __repr__(self):
        resp = {
            "code": self.code,
            "msg": self.msg,
            "data": self.data,
            "total": self.total,
        }
        resp.update(self.kwargs)
        return resp


class NotLoginResponse(ResponseCode):
    """未登录 没有token"""
    code = 1001
    msg = "not login."


class PermissionDeniedResponse(ResponseCode):
    """用户无权限"""
    code = 1002
    msg = "Permission denied."


class TokenInvalidResponse(ResponseCode):
    """token 不合法"""
    code = 1003
    msg = "Token invalid."


class TokenExpiredResponse(ResponseCode):
    """token 过期"""
    code = 1004
    msg = "Token expired,please refresh token."


class TokenRefreshExpiredResponse(ResponseCode):
    """token 刷新token失败"""
    code = 1005
    msg = "Token refresh fail."


class InternalErrorResponse(ResponseCode):
    """内部错误"""
    code = 5000
    msg = "Internal error."


class AuthenticateErrorResponse(ResponseCode):
    """身份验证失败"""
    code = 2001
    msg = "Authenticate error."


class ReAuthErrorResponse(ResponseCode):
    """重复进行身份验证"""
    code = 2002
    msg = "Repeat authentication."


class LoginFailResponse(ResponseCode):
    """登陆失败"""
    code = 2003
    msg = "login failed."
