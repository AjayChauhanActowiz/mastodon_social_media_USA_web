from curl_cffi import requests
# import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


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

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# token = "token"
# proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)
## proxyModeUrl = "http://{}:super=true@proxy.scrape.do:8080".format(token)
## proxyModeUrl = "http://{}:super=true&geoCode=us@proxy.scrape.do:8080".format(token)
# proxies = {
#     "http": proxyModeUrl,
#     "https": proxyModeUrl,
# }

# proxy_url = "http://user-spqf6yqq8t-country-in:aQuQe050b3rmtbxD+V@dc.decodo.com:10001"
# proxies = {
#     "http": proxy_url,
#     "https": proxy_url,
# }

# scraper_api_token = 'token'
# proxies = {
#     "http": f"http://scraperapi:{scraper_api_token}@proxy-server.scraperapi.com:8001",
#     "https": f"http://scraperapi:{scraper_api_token}@proxy-server.scraperapi.com:8001"
# }

def response_check(start_iteration, num_requests):
    """Perform multiple requests inside one thread to reduce overhead."""
    batch_results = []
    for i in range(num_requests):
        iteration = start_iteration + i
        st = time.time()
        try:
            response = requests.get(
                'https://mastodon.social/api/v1/trends/statuses',
                params=params,
                # headers=headers,
                # cookies=cookies,
                impersonate='chrome120',
                # proxies=proxies,
                # verify=False,
                timeout=120
            )
            if fr'@blogdiva' and '110641555278107926' in response.text:
                return_dict = {
                    'iteration': iteration,
                    'status': response.status_code,
                    'response': 'good',
                    'time_taken': time.time()-st
                }
                batch_results.append(return_dict)
                print(return_dict)
            else:
                return_dict = {
                    'iteration': iteration,
                    'status': response.status_code,
                    'response': 'bad',
                    'time_taken': time.time() - st
                }
                batch_results.append(return_dict)
                print(return_dict)
        except Exception as e:
            return_dict = {
                'iteration': iteration,
                'status': None,
                'response': f'error: {e}',
                'time_taken': time.time() - st
            }
            batch_results.append(return_dict)
            print(return_dict)
    return batch_results

results = []
thread_count = 20
total_requests = 3000
requests_per_thread = 1  # Each worker handles 10 requests

with ThreadPoolExecutor(max_workers=thread_count) as executor:
    futures = []
    for start in range(1, total_requests + 1, requests_per_thread):
        futures.append(executor.submit(response_check, start, requests_per_thread))

    for future in as_completed(futures):
        batch = future.result()
        for result in batch:
            # print(result)
            results.append(result)

# Save results to Excel
file_name = 'mastodon_trends_feasibility_test'
df = pd.DataFrame(results)
df.to_excel(f'{file_name}.xlsx', index=False)
print(f"Results saved to {file_name}.xlsx")


