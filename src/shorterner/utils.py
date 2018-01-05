
from .models import ErrorDetail, Error, Period, PeriodDetail, Url

import requests
import json

API_KEY = 'AIzaSyCl52P8Tw1VoGD6EDw7dAZgmtalmVStQcs'

def google_url_shorten(url):
   req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + API_KEY
   payload = {'longUrl': url}
   headers = {'content-type': 'application/json'}
   r = requests.post(req_url, data=json.dumps(payload), headers=headers)
   resp = json.loads(r.text)
   return resp

def google_url_expand(url):
    req_url = 'https://www.googleapis.com/urlshortener/v1/url' 
    payload = {'key': API_KEY, 'shortUrl': url, 'projection': 'full'}
    r = requests.get(req_url, params=payload)
    resp = json.loads(r.text)
    return resp

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def create_period_detail(obj_dict, *keys):
    return_list = []
    obj_count = 0
    if keys_exists(obj_dict, *keys):
        obj_list = obj_dict.get(keys[0]).get(keys[1]).get(keys[2])
        print(f"Period: {keys[1]} | Metric Type: {keys[2]}")
        for item in obj_list:
            new_item = PeriodDetail(
                count = int(item.get('count')),
                source_id = item.get('id')
                )
            new_item.save() #Requires the object to be saved before it can be added as part of another object
            obj_count= obj_count + 1
            print(f"Entry Count: {obj_count} | Source id: {new_item.source_id} | Click Count: {new_item.count}")
            return_list.append(new_item)
    return return_list


def create_period(obj_dict, obj_list, *keys):
    obj_total = 0
    output = Period(
        short_url_clicks = int(obj_dict.get(keys[0]).get(keys[1]).get(keys[2])),
        long_url_clicks = int(obj_dict.get(keys[0]).get(keys[1]).get(keys[3]))
    )
    for index, list in enumerate(obj_list):
        print(f"List Index: {index} | List: {list}")
        if index is 0:
            obj_count = 0
            for item in list:
                output.referrer = item
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Referrers added {obj_count} objects")
        elif index is 1:
            obj_count = 0
            for item in list:
                output.country = item
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Countries added {obj_count} objects")
        elif index is 2:
            obj_count = 0
            for item in list:
                output.browser = item
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Browsers added {obj_count} objects")
        elif index is 3:
            obj_count = 0
            for item in list:
                output.platforms = item
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Platforms added {obj_count} objects")
    output.save()
    # print(f"The total number of object(s) added is {obj_total}")
    return output
    
def create_url(obj_json, input_url):
    # Retrieving values from JSON > Creating 
    # Tier 3
    # All Time
    alltime_list = []
    alltime_list.append(create_period_detail(obj_json, 'analytics', 'allTime', 'referrers'))
    alltime_list.append(create_period_detail(obj_json, 'analytics', 'allTime', 'countries'))
    alltime_list.append(create_period_detail(obj_json, 'analytics', 'allTime', 'browsers'))
    alltime_list.append(create_period_detail(obj_json, 'analytics', 'allTime', 'platforms'))
    
    # Month
    month_list = []
    month_list.append(create_period_detail(obj_json, 'analytics', 'month', 'referrers'))
    month_list.append(create_period_detail(obj_json, 'analytics', 'month', 'countries'))
    month_list.append(create_period_detail(obj_json, 'analytics', 'month', 'browsers'))
    month_list.append(create_period_detail(obj_json, 'analytics', 'month', 'platforms'))

    # Week
    week_list = []
    week_list.append(create_period_detail(obj_json, 'analytics', 'week', 'referrers'))
    week_list.append(create_period_detail(obj_json, 'analytics', 'week', 'countries'))
    week_list.append(create_period_detail(obj_json, 'analytics', 'week', 'browsers'))
    week_list.append(create_period_detail(obj_json, 'analytics', 'week', 'platforms'))
    
    # Day
    day_list = []
    day_list.append(create_period_detail(obj_json, 'analytics', 'day', 'referrers'))
    day_list.append(create_period_detail(obj_json, 'analytics', 'day', 'countries'))
    day_list.append(create_period_detail(obj_json, 'analytics', 'day', 'browsers'))
    day_list.append(create_period_detail(obj_json, 'analytics', 'day', 'platforms'))

    # twoHours
    twoHour_list = []
    twoHour_list.append(create_period_detail(obj_json, 'analytics', 'twoHours', 'referrers'))
    twoHour_list.append(create_period_detail(obj_json, 'analytics', 'twoHours', 'countries'))
    twoHour_list.append(create_period_detail(obj_json, 'analytics', 'twoHours', 'browsers'))
    twoHour_list.append(create_period_detail(obj_json, 'analytics', 'twoHours', 'platforms'))

    # Tier 2
    alltime = create_period(obj_json, alltime_list, 'analytics', 'allTime', 'shortUrlClicks', 'longUrlClicks')
    month = create_period(obj_json, month_list, 'analytics', 'month', 'shortUrlClicks', 'longUrlClicks')
    week = create_period(obj_json, week_list, 'analytics', 'week', 'shortUrlClicks', 'longUrlClicks')
    day = create_period(obj_json, day_list, 'analytics', 'day', 'shortUrlClicks', 'longUrlClicks')
    twoHour = create_period(obj_json, twoHour_list, 'analytics', 'twoHours', 'shortUrlClicks', 'longUrlClicks')

    # Tier 1
    # Create Url
    new_url = Url.objects.create(
        short_url = obj_json.get('id'),
        input_url = input_url,
        status = obj_json.get('status'),
        created = obj_json.get('created'),
        alltime = alltime,
        month = month,
        week = week,
        day = day,
        twohour = twoHour                      
    )
    return new_url



            # for index, list in enumerate(obj_list):
            # print(f"List Index: {index} | List: {list}")
            # if index is 0:
            #     obj_count = 0
            #     for item in list:
            #         referrer = item
            #         obj_count = obj_count + 1
            #     obj_total = obj_total + obj_count
            #     print(f"Referrers added {obj_count} objects")
            # elif index is 1:
            #     obj_count = 0
            #     for item in list:
            #         output.country = item
            #         obj_count = obj_count + 1
            #     obj_total = obj_total + obj_count
            #     print(f"Countries added {obj_count} objects")
            # elif index is 2:
            #     obj_count = 0
            #     for item in list:
            #         output.browser = item
            #         obj_count = obj_count + 1
            #     obj_total = obj_total + obj_count
            #     print(f"Browsers added {obj_count} objects")
            # elif index is 3:
            #     obj_count = 0
            #     for item in list:
            #         output.platforms = item
            #         obj_count = obj_count + 1
            #     obj_total = obj_total + obj_count
            #     print(f"Platforms added {obj_count} objects")