import requests

response = requests.post("https://www.baidu.com/s", data={'wd': 'david%20lynch', 'ie': 'utf-8'})

print(response.status_code)
print(response.text)
