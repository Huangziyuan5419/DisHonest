import requests

url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'
form_data = {
    'pageSize': '10',
    'pageNo': '4',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

response = requests.post(url, headers=headers, data=form_data)
print(response.text)
