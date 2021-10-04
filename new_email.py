import requests
import json
import time

def getEmail():
    http_proxy = "http://jbfrwczo7g6lsyh:mZPUqOOdXMIbXsJv@hub.zenscrape.com:31112"
    proxyDict = {
        "http" : http_proxy,
        "https": http_proxy
    }
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'

    data = {'max_name_length': 10, 'min_name_length': 10}

    headers = {'accept': 'application/json, text/plain, */*', 
               'accept-encoding': 'gzip, deflate, br', 
               'accept-language': 'en-US,en;q=0.9', 
               'content-type': 'application/json;charset=UTF-8', 
               'cookie': '__cfduid=da31155b5fd8316c25a08a4a8c19e19f81613986205; _ga=GA1.2.971417850.1613986216; __gads=ID=5dd3cb6ce5b775c4-22d65d26d1a6006f:T=1613986224:RT=1613986224:S=ALNI_MZje0UFDBAyx0NIjFe57Td9r2j2og; _gid=GA1.2.1077178000.1614159286', 
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }

    res = requests.post(url, data=json.dumps(data), headers=headers, proxies=proxyDict)
    print(res.status_code)
    text = res.json()
    email = text['email']
    res.close()
    print(email)
    return email
#for i in range(0,5):
#    getEmail()    


def verifyLink(email):
    verify_api = 'https://api.internal.temp-mail.io/api/v3/email/' + email +'/messages'

    headers = {'accept': 'application/json, text/plain, */*', 
               'accept-encoding': 'gzip, deflate, br', 
               'accept-language': 'en-US,en;q=0.9', 
               'content-type': 'application/json;charset=UTF-8', 
               'cookie': '__cfduid=da31155b5fd8316c25a08a4a8c19e19f81613986205; _ga=GA1.2.971417850.1613986216; __gads=ID=5dd3cb6ce5b775c4-22d65d26d1a6006f:T=1613986224:RT=1613986224:S=ALNI_MZje0UFDBAyx0NIjFe57Td9r2j2og; _gid=GA1.2.1077178000.1614159286', 
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }


    while True:
        verify_res = requests.get(verify_api, headers=headers)
        if verify_res.status_code==200 and len(verify_res.json()) > 0:
            print(verify_res.status_code)
            verify_text = verify_res.json()
            verify_link = verify_text[0]['body_text'].split('\n')[10].replace('*Verify Email Address*', '').replace('(', '').replace(')', '').strip()
            print(verify_link)
            verify_res.close()
            break
        else:
            time.sleep(2)
            continue
    return verify_link

