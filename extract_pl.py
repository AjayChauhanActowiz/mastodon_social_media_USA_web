from curl_cffi import requests
import pydash as _

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://mastodon.social/explore',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
}
params = {
    # 'offset': '20',
    'offset': '0',
}
accts = []
for i in range(3):
    response = requests.get(
        'https://mastodon.social/api/v1/trends/statuses',
        params=params,
        # headers=headers,
        impersonate='chrome120'
    )
    print(response.status_code)

    json_data = response.json()
    for acc in json_data:
        accts.append(_.get(acc,"account.acct",None))
    params['offset'] = str(int(params['offset'])+20)
print(accts)