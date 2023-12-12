import requests

proxies = {
    # "http": "http://117.160.250.163:8828",
}
li_hua = requests.Session()
li_hua.proxies = proxies
a = li_hua.get(url='http://httpbin.org/ip')
print(a.text)
