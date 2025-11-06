import requests

cookies = {
    '_mastodon_session': 'tSaIiIn%2B2OCbbzKHAfgzdkkTyOG6a%2Fsy8n89EEIakDXyfCHEQTyNffNi1%2FQEXfJcu3sr9a%2BSJnpUs4Nw5ZLtu%2F%2BsE6Y7eFXxT9p7AB%2FWLX7PoKbWo7vEGSFmPCgrT4ULAaIJALNI5s%2FC1bmZPdwVlq4FVf2lrsGPMaEo7S2VJISX%2FcYXkVK6A18hF3X%2B9Ys9OW2SA94S4A4mfoddDdywBXn0hUNcKq8Q%2FTS8V5S2r5sj8jIvoOYbBvzpnQhsEekL4O9%2Bt%2F7PbZpYE7J8xrDyMoFyU2RYzXmd2Q%3D%3D--b2X5zwYaI1HPYKNs--xGHVfuD03oq6gfE1liWqQQ%3D%3D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://mastodon.social/search?q=morning',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_mastodon_session=tSaIiIn%2B2OCbbzKHAfgzdkkTyOG6a%2Fsy8n89EEIakDXyfCHEQTyNffNi1%2FQEXfJcu3sr9a%2BSJnpUs4Nw5ZLtu%2F%2BsE6Y7eFXxT9p7AB%2FWLX7PoKbWo7vEGSFmPCgrT4ULAaIJALNI5s%2FC1bmZPdwVlq4FVf2lrsGPMaEo7S2VJISX%2FcYXkVK6A18hF3X%2B9Ys9OW2SA94S4A4mfoddDdywBXn0hUNcKq8Q%2FTS8V5S2r5sj8jIvoOYbBvzpnQhsEekL4O9%2Bt%2F7PbZpYE7J8xrDyMoFyU2RYzXmd2Q%3D%3D--b2X5zwYaI1HPYKNs--xGHVfuD03oq6gfE1liWqQQ%3D%3D',
}

params = {
    'q': 'morning',
    'resolve': 'false',
    'limit': '11',
}

response = requests.get('https://mastodon.social/api/v2/search', params=params, headers=headers)
print(response.status_code)
print(response.json().get('hashtags',[]))