import http.client, urllib.parse

conn = http.client.HTTPConnection('api.mediastack.com')

params = urllib.parse.urlencode({
    'access_key': 'ecc24351cf7da9ac4825577ea48b5710',
    'categories': '-general,-sports',
    'sort': 'published_desc',
    'limit': 10,
    })

conn.request('GET', '/v1/news?{}'.format(params))

res = conn.getresponse()
data = res.read()

data = data.decode('utf-8')
print(data)


# 示例 JSON 数据（包含数组的data字段）
# json_data = '''
# {
#     "pagination": {
#         "limit": 100,
#         "offset": 0,
#         "count": 100,
#         "total": 1311
#     },
#     "data": [
#         {
#             "author": "Dolat Capital",
#             "title": "SRF Q2 Results Review - Recovery Delayed As Uncertainties Persist: Dolat Capital",
#             "description": "SRF Q2 Results Review - Recovery Delayed As Uncertainties Persist: Dolat Capital",
#             "url": "https://www.ndtvprofit.com/research-reports/srf-q2-results-review-recovery-delayed-as-uncertainties-persist-dolat-capital",
#             "source": "Bloomberg | Latest And Live Business",
#             "image": null,
#             "category": "business",
#             "language": "en",
#             "country": "us",
#             "published_at": "2024-10-24T02:02:48+00:00"
#         },
#         {
#             "author": null,
#             "title": "Warning: NBTX is at high risk of performing badly",
#             "description": "Warning: NBTX is at high risk of performing badly",
#             "url": "https://seekingalpha.com/warnings/4197996-warning-nbtx-is-high-risk-of-performing-badly?utm_source=feed_news_all&utm_medium=referral&feed_item_type=news",
#             "source": "Seeking Alpha",
#             "image": null,
#             "category": "business",
#             "language": "en",
#             "country": "us",
#             "published_at": "2024-10-24T02:13:41+00:00"
#         }
#     ]
# }
# '''