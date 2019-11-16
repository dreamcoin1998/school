class Code:
    def __init__(self, code, msg=None):
        self.code = code
        self.msg = msg or self.set_msg()

    def set_msg(self):
        if self.code == 0:
            return 'request ok.'
        elif self.code == 1:
            return 'request error.'


def ReturnCode(code, msg=None):
    status = Code(code, msg=msg)
    return {'code': status.code, 'msg': status.msg}