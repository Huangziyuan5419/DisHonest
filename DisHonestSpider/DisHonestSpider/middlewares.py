import random
import requests
from DisHonestSpider.settings import USER_AGENTS


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS)

        return None

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        '''设置代理 ip'''
        # 获取协议头
        protocol = request.url.split('://')[0]
        # 构建代理ip的请求url
        proxy_url = 'http://localhost:16888/random?protocol={}'.format(protocol)
        # 获取ip代理
        response = requests.get(proxy_url)
        # 设置成代理ip
        request.meta['proxy'] = response.content.decode()

        return None