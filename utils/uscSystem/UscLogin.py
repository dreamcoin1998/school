from utils.uscSystem.UniversityLogin import UniversityLogin
import logging


class UscLogin(UniversityLogin):
    '''
    登录南华大学教务在线，需要encode,username,password
    1.首先解析encode
    2.登录
    '''
    def UscLoginNew(self):
        try:
            # 登录校园网，首先获取传输参数encode
            res = self.s.post('http://61.187.179.66:8924/Logon.do?method=logon&flag=sess', headers=self.headers)
            dataStr = res.text
            if dataStr == 'no':
                return False
            else:
                scode = dataStr.split('#')[0]
                sxh = dataStr.split('#')[1]
                code = self.UserName + '%%%' + self.Password
                encoded = ''
                i = 0
                while i < len(code):
                    if i < 20:
                        encoded = encoded + code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
                        scode = scode[int(sxh[i:i + 1]):len(scode)]
                    else:
                        encoded = encoded + code[i:len(code)]
                        i = len(code)
                    i += 1
                print(encoded)
                # 校园网登录
                data = {
                    'userAccount': self.UserName,
                    'userPassword': self.Password,
                    'encoded': encoded
                }
                res = self.s.post('http://61.187.179.66:8924/Logon.do?method=logon', headers=self.headers, data=data)
                print(res.headers.get('cache-control'))
                # 登陆成功则为200
                if res.headers.get('cache-control') is None:
                    return True
                else:
                    return False
        except Exception as e:
            logging.debug(e)
            print(e)
            return False