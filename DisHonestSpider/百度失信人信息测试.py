import requests


url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=20&rn=10&ie=utf-8&oe=utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Referer': 'https://www.baidu.com/s?wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&rsv_spt=1&rsv_iqid=0xc7799031000bb138&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&oq=ev4player%25E6%2592%25AD%25E6%2594%25BE%25E5%2599%25A8&rsv_t=d0cdpcWQ5%2F64muUzdoYD%2BnWBrUZc%2BAH4DBCrX3IuJ8mAglsU7zNpoTkrLmptygHRxVcP&inputT=5460&rsv_pq=ee40ff5c00282774&rsv_sug3=95&rsv_sug1=42&rsv_sug7=100&bs=ev4player%E6%92%AD%E6%94%BE%E5%99%A8',
}

response =  requests.get(url, headers=headers)
print(response.status_code)
print(response.text)