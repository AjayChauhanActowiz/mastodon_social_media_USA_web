import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
    'if-none-match': 'W/"c0a0988f3a52cd5ac26f3a80f7165942"',
    'priority': 'u=1, i',
    'referer': 'https://mastodon.social/@randahl/with_replies',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

params = {
    # "pinned": "false",
    'exclude_replies': 'true',
    # 'exclude_reblogs': 'true',
    'exclude_reblogs': 'false',
}

response = requests.get('https://mastodon.social/api/v1/accounts/108197900630052143/statuses', params=params, headers=headers)
print(response.status_code)
print(response.text)