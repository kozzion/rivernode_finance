
import json
import csv

with open('list_result.json', 'r') as file:
    list_result = json.load(file)

list_line = []
list_line.append(['username', 'audience_size', 'engagement_precent', 'count_post', 'quality'])
print(len(list_result))
for result in list_result[1:]:
    username = result['payload']['user']['username']
    audience_size = result['payload']['count_followed_by']
    engagement_precent = round(result['payload']['mean_fraction_history_like'] * 100, 2)
    count_post = result['payload']['count_post']
    quality = round(1 - result['distance'], 2)
    list_line.append([username, audience_size, engagement_precent, count_post, quality])


writer = csv.writer(open('list_result.csv', 'w', newline=''))
for line in list_line:
    writer.writerow(line)


      # "distance": 0.6797161102294922,
    #     "id_item": "1531318532",
    #     "payload": {
    #         "count_followed_by": 4780671,
    #         "count_following": 263,
    #         "count_post": 2564,
    #         "mean_fraction_history_comment": 6.008779939050397e-05,
    #         "mean_fraction_history_like": 0.01953691856226877,
    #         "size_history": 50,
    #         "user": {
    #             "id": "1531318532",
    #             "username": "portugal"
    #         }
    #     }
    # },