from curl_cffi import requests

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://mastodon.social/explore',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
}
params = {
    'only_media': 'true',
    'limit': '40',
}
response = requests.get(
    'https://mastodon.social/api/v1/accounts/110641555278107926/statuses',
    params=params,
    # headers=headers,
    impersonate='chrome120'
)
print(response.status_code)
print('media_attachments/files/115/494/143/888/076/496/original/501bd8f774fa4ded.mp4' in response.text)
