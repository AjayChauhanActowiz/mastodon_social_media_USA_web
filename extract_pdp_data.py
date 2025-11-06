from curl_cffi import requests
from lxml import html
import json
import re
import accounts
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://mastodon.social/@blogdiva',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
}
def all_html_text(html_text):
    if html_text:
        tree = html.fromstring(html_text)
        text = ''.join(tree.xpath('//text()')).replace('&amp;','&').strip()
        return re.sub(r':[a-zA-Z0-9_-]+:', '', text).strip()
    return None
def get_details(json_data):
    fields = json_data.get('fields', [])
    result_fields = []
    for field in fields:
        field['value'] = all_html_text(field['value'])
        result_fields.append(field)
    return {
        'url': json_data.get('url', None),
        'id': json_data.get('id', None),
        'username': json_data.get('username', None),
        'acct': json_data.get('acct', None),
        'display_name': json_data.get('display_name', None),
        'created_at': json_data.get('created_at', None),
        'avatar': json_data.get('avatar', None),
        'header': json_data.get('header', None),
        'followers_count': json_data.get('followers_count', None),
        'following_count': json_data.get('following_count', None),
        'statuses_count': json_data.get('statuses_count', None),
        'last_status_at': json_data.get('last_status_at', None),
        'note': all_html_text(json_data.get('note', None)),
        # 'fields': json.dumps(result_fields) if result_fields else None
        'fields': result_fields if result_fields else []
    }
def get_post_details(json_data):
    media_attachments = json_data.get('media_attachments',[])
    result_media_attachments = []
    for media_attachment in media_attachments:
        result_media_attachments.append({
            'url': media_attachment.get('url', None),
            'id': media_attachment.get('id',None),
            'type': media_attachment.get('type',None),
            'description': all_html_text(media_attachment.get('description',None))
        })
    return {
        'url': json_data.get('url', None),
        'id': json_data.get('id',None),
        'created_at': json_data.get('created_at',None),
        'in_reply_to_id': json_data.get('in_reply_to_id',None),
        'in_reply_to_account_id': json_data.get('in_reply_to_account_id',None),
        'replies_count': json_data.get('replies_count',None),
        'reblogs_count': json_data.get('reblogs_count',None),
        'favourites_count': json_data.get('favourites_count',None),
        'quotes_count': json_data.get('quotes_count',None),
        'content': all_html_text(json_data.get('content',None)),
        'edited_at': json_data.get('edited_at',None),
        'mentions': json_data.get('mentions',[]),
        'tags': json_data.get('tags',[]),
        'media_attachments': result_media_attachments
    }
def following_data(acc_id):
    following_response = requests.get(f'https://mastodon.social/api/v1/accounts/{acc_id}/following', impersonate='chrome120')
    following_response_json_data = following_response.json()
    if len(following_response_json_data)<= 10 and len(following_response_json_data)!=0:
        limit = len(following_response_json_data)
    elif len(following_response_json_data) == 0:
        # return None
        return []
    else:
        limit = 10
    following_list_docu = []
    for following_json_data in following_response_json_data[:limit]:
        following_list_docu.append(get_details(following_json_data))
    # return json.dumps(following_list_docu) if following_list_docu else None
    return following_list_docu if following_list_docu else []
def followers_data(acc_id):
    followers_response = requests.get(f'https://mastodon.social/api/v1/accounts/{acc_id}/followers', impersonate='chrome120')
    followers_response_json_data = followers_response.json()
    if len(followers_response_json_data)<= 10 and len(followers_response_json_data)!=0:
        limit = len(followers_response_json_data)
    elif len(followers_response_json_data) == 0:
        # return None
        return []
    else:
        limit = 10
    followers_list_docu = []
    for followers_json_data in followers_response_json_data[:limit]:
        followers_list_docu.append(get_details(followers_json_data))
    # return json.dumps(followers_list_docu) if followers_list_docu else None
    return followers_list_docu if followers_list_docu else []
def post_detail_data(post_id):
    post_detail_response = requests.get(f'https://mastodon.social/api/v1/statuses/{post_id}/context', impersonate='chrome120')
    post_detail_json_data = post_detail_response.json().get('descendants',[])
    if post_detail_json_data:
        return_post_data = []
        for p in post_detail_json_data:
            return_post_data_docu = get_post_details(p)
            return_post_data_docu.update({'account': get_details(p.get('account',[]))})
            return_post_data.append(return_post_data_docu)
        return return_post_data
    return []

def post_pinned_data(acc_id):
    post_pin_params = {
        'pinned': 'true'
    }
    post_pin_response = requests.get(f'https://mastodon.social/api/v1/accounts/{acc_id}/statuses', params=post_pin_params,impersonate='chrome120')
    post_pin_response_json_data = post_pin_response.json()
    if len(post_pin_response_json_data) <= 10 and len(post_pin_response_json_data) != 0:
        limit = len(post_pin_response_json_data)
    elif len(post_pin_response_json_data) == 0:
        # return None
        return []
    else:
        limit = 10
    post_pin_list_docu = []
    for post_pin_json_data in post_pin_response_json_data[:limit]:
        post_pin_list_docu.append(get_post_details(post_pin_json_data))
    # return json.dumps(followers_list_docu) if followers_list_docu else None
    return post_pin_list_docu if post_pin_list_docu else []
def post_unpin_with_replies(acc_id):
    post_unpin_params = {
        'exclude_replies': 'true',
        'exclude_reblogs': 'true',
    }
    post_unpin_response = requests.get(f'https://mastodon.social/api/v1/accounts/{acc_id}/statuses',
                                     params=post_unpin_params, impersonate='chrome120')
    post_unpin_response_json_data = post_unpin_response.json()
    if len(post_unpin_response_json_data) <= 10 and len(post_unpin_response_json_data) != 0:
        limit = len(post_unpin_response_json_data)
    elif len(post_unpin_response_json_data) == 0:
        # return None
        return []
    else:
        limit = 10
    post_unpin_list_docu = []
    for post_unpin_json_data in post_unpin_response_json_data[:limit]:
        # post_unpin_list_docu.append(get_post_details(post_unpin_json_data))
        post = get_post_details(post_unpin_json_data)
        post_unpin_list_docu.append({
            'post': post,
            'comments_and_replies': post_detail_data(post['id'])
        })
    # return json.dumps(followers_list_docu) if followers_list_docu else None
    return post_unpin_list_docu if post_unpin_list_docu else []
def account_detail(acct):
    account_params = {
        'acct': acct
    }
    account_response = requests.get('https://mastodon.social/api/v1/accounts/lookup', params=account_params, impersonate='chrome120')
    # account_response_json_data = account_response.json()
    return get_details(account_response.json())
def username(acct):
    profile = account_detail(acct)
    return {
        'profile': profile,
        'post': post_unpin_with_replies(profile['id']),
        'followers': followers_data(profile['id']),
        'following': following_data(profile['id'])
    }
def hashtags(hashtag_search):
    if hashtag_search:
        hashtag_params = {
            'local': 'false',
        }

        hashtag_response = requests.get(f'https://mastodon.social/api/v1/timelines/tag/{hashtag_search}', params=hashtag_params, impersonate='chrome120')
        hashtag_json_data = hashtag_response.json()
        if len(hashtag_json_data) <= 10 and len(hashtag_json_data) != 0:
            limit = len(hashtag_json_data)
        elif len(hashtag_json_data) == 0:
            # return None
            return []
        else:
            limit = 10
        post_list = []
        for h in hashtag_json_data[:limit]:
            hashtag_post_detail = get_post_details(h)
            hashtag_post_detail.update({'account': get_details(h['account'])})
            comments_and_replies = post_detail_data(hashtag_post_detail['id'])
            post_list.append({
                'post': hashtag_post_detail,
                'comments_and_replies': comments_and_replies
            })
        # return{
        #     'hashtag_search': hashtag_search,
        #     'post': post_list
        # }
        return post_list
    return []
def search_word(search_text):
    search_word_params = {
        # 'q': 'morning',
        'q': search_text,
        'resolve': 'false',
        'limit': '11',
    }

    search_response = requests.get('https://mastodon.social/api/v2/search', params=search_word_params, impersonate='chrome120').json()
    hashtags_list = []
    for hashtag in search_response.get('hashtags',[]):
        hashtags_list.append({
            'hashtag_url': hashtag.get('url',None),
            'hashtag_name': hashtag.get('name',None),
            'hashtag_id': hashtag.get('id',None),
            'result': hashtags(hashtag.get('name',None))
        })
    return {
        'search_text': search_text,
        'hashtag_result': hashtags_list
    }
# with open('sample_data.json', 'w', encoding='utf-8') as f:
#     json.dump(total_data, f, ensure_ascii=False, indent=2)
# total_data = []
# for acc in accounts.accts[:1]:
#     detail = username(acc)
#     print(detail)
#     total_data.append(detail)
# with open('sample_data.json','w',encoding='utf-8') as f:
#     json.dump(total_data,f)

# total_data = []
#
# # Limit to first 5 accounts
# accounts_to_process = accounts.accts[:5]
#
# # Use ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=5) as executor:
#     # Submit all tasks
#     future_to_acc = {executor.submit(main, acc): acc for acc in accounts_to_process}
#
#     for future in as_completed(future_to_acc):
#         acc = future_to_acc[future]
#         try:
#             detail = future.result()
#             print(detail)
#             total_data.append(detail)
#         except Exception as e:
#             print(f"Error processing account {acc}: {e}")
#
# # Save to JSON file
# with open('sample_data.json', 'w', encoding='utf-8') as f:
#     json.dump(total_data, f, ensure_ascii=False, indent=2)

