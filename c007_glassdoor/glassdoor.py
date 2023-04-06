import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

# url = 'https://www.glassdoor.com.hk/Reviews/Apple-Reviews-E1138.htm'
url = 'https://www.glassdoor.com/Overview/Working-at-Wells-Fargo-EI_IE8876.11,22.htm'

resp = requests.get(url, headers=headers)

with open('glassdoor.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)

print(resp.text)
print(resp.status_code)
