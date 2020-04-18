from django.http.response import HttpResponseForbidden
from rest_framework.response import Response
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object
from django.core.cache import cache
from utils.ReturnCode import ReturnCode
from school.settings import MAX_IP_FREQUENT, BLOCK_IP_TIME


class AntiSpider(MiddlewareMixin):

    # 验证User-Agent方法
    def verificationUserAgent(self, request):
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        http_user_agent = str(http_user_agent).lower()
        if "py" in http_user_agent or "ssl" in http_user_agent:
            return True
        return False

    # 添加进IP黑名单
    def _add_to_ip_blacklist(self, ip_address):
        cache.set(ip_address, 'block', timeout=BLOCK_IP_TIME)
        # print(cache.get(ip_address))

    # 验证ip是否在ip黑名单中
    def _verification_ip_in_blacklist(self, ip_address):
        info = cache.get(ip_address)
        # print(info)
        return True if info == 'block' else False

    # 设置IP访问频率
    def ip_frequent_limit(self, ip_address):
        cache.get_or_set(ip_address, 0, 1)
        # 原子化操作，不用担心加锁不加锁的问题，redis是单线程，运行在内存，采用IO多路复用技术
        ip_frequent = cache.incr(ip_address)
        if ip_frequent >= MAX_IP_FREQUENT:
            self._add_to_ip_blacklist(ip_address)
            return True
        return False

    # 检测到爬虫处理方式
    def _blocking_strategy(self, code=None):
        return HttpResponseForbidden()

    def process_request(self, request):
            # 验证User-Agent
            result = self.verificationUserAgent(request)
            ip_address = request.META.get('REMOTE_ADDR')
            '''
            1.验证user-agent
            2.验证是否在IP黑名单中
            3.验证访问频率是否超限
            '''
            if result:
                return self._blocking_strategy()
            elif self._verification_ip_in_blacklist(ip_address):
                return self._blocking_strategy()
            elif self.ip_frequent_limit(ip_address):
                return self._blocking_strategy()
            return None

    def process_response(self, request, response):
        return response