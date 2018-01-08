
from .models import Error, Period, PeriodDetail, Url

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

def create_period_detail(obj, *keys):
    return_list = []
    obj_count = 0
    if keys_exists(obj, *keys):
        obj_list = obj.get(keys[0]).get(keys[1]).get(keys[2])
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


def create_period(obj, obj_list, *keys):
    obj_total = 0
    output = Period(
        short_url_clicks = int(obj.get(keys[0]).get(keys[1]).get(keys[2])),
        long_url_clicks = int(obj.get(keys[0]).get(keys[1]).get(keys[3]))
    )
    output.save()
    for index, list in enumerate(obj_list):
        print(f"List Index: {index} | List: {list}")
        if index is 0:
            obj_count = 0
            for item in list:
                output.referrer.add(item)
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Referrers added {obj_count} objects")
        elif index is 1:
            obj_count = 0
            for item in list:
                output.country.add(item)
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Countries added {obj_count} objects")
        elif index is 2:
            obj_count = 0
            for item in list:
                output.browser.add(item)
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Browsers added {obj_count} objects")
        elif index is 3:
            obj_count = 0
            for item in list:
                output.platform.add(item)
                obj_count = obj_count + 1
            obj_total = obj_total + obj_count
            print(f"Platforms added {obj_count} objects")
    output.save()
    print(f"The total number of object(s) added is {obj_total}")
    return output
    
def create_analytics(obj):
    # Retrieving values from JSON > Creating 
    # Tier 3
    # All Time
    alltime_list = []
    alltime_list.append(create_period_detail(obj, 'analytics', 'allTime', 'referrers'))
    alltime_list.append(create_period_detail(obj, 'analytics', 'allTime', 'countries'))
    alltime_list.append(create_period_detail(obj, 'analytics', 'allTime', 'browsers'))
    alltime_list.append(create_period_detail(obj, 'analytics', 'allTime', 'platforms'))
    
    # Month
    month_list = []
    month_list.append(create_period_detail(obj, 'analytics', 'month', 'referrers'))
    month_list.append(create_period_detail(obj, 'analytics', 'month', 'countries'))
    month_list.append(create_period_detail(obj, 'analytics', 'month', 'browsers'))
    month_list.append(create_period_detail(obj, 'analytics', 'month', 'platforms'))

    # Week
    week_list = []
    week_list.append(create_period_detail(obj, 'analytics', 'week', 'referrers'))
    week_list.append(create_period_detail(obj, 'analytics', 'week', 'countries'))
    week_list.append(create_period_detail(obj, 'analytics', 'week', 'browsers'))
    week_list.append(create_period_detail(obj, 'analytics', 'week', 'platforms'))
    
    # Day
    day_list = []
    day_list.append(create_period_detail(obj, 'analytics', 'day', 'referrers'))
    day_list.append(create_period_detail(obj, 'analytics', 'day', 'countries'))
    day_list.append(create_period_detail(obj, 'analytics', 'day', 'browsers'))
    day_list.append(create_period_detail(obj, 'analytics', 'day', 'platforms'))

    # twoHours
    twoHour_list = []
    twoHour_list.append(create_period_detail(obj, 'analytics', 'twoHours', 'referrers'))
    twoHour_list.append(create_period_detail(obj, 'analytics', 'twoHours', 'countries'))
    twoHour_list.append(create_period_detail(obj, 'analytics', 'twoHours', 'browsers'))
    twoHour_list.append(create_period_detail(obj, 'analytics', 'twoHours', 'platforms'))

    # Tier 2
    alltime = create_period(obj, alltime_list, 'analytics', 'allTime', 'shortUrlClicks', 'longUrlClicks')
    month = create_period(obj, month_list, 'analytics', 'month', 'shortUrlClicks', 'longUrlClicks')
    week = create_period(obj, week_list, 'analytics', 'week', 'shortUrlClicks', 'longUrlClicks')
    day = create_period(obj, day_list, 'analytics', 'day', 'shortUrlClicks', 'longUrlClicks')
    twoHour = create_period(obj, twoHour_list, 'analytics', 'twoHours', 'shortUrlClicks', 'longUrlClicks')

    analytics_list = []
    analytics_list.append(alltime)
    analytics_list.append(month)
    analytics_list.append(week)
    analytics_list.append(day)
    analytics_list.append(twoHour)

    return analytics_list

# Non default/optional arguments before default/optional arguments
def create_url(status, input_url, obj_list, obj=None):
    if status is 'Success':
        new_url = Url.objects.create(
            short_url = obj.get('id'),
            input_url = input_url,
            status = obj.get('status'),
            created = obj.get('created'),
            alltime = obj_list[0],
            month = obj_list[1],
            week = obj_list[2],
            day = obj_list[3],
            twohour = obj_list[4],
            errormessage = None                      
            )
    elif status is 'Unsuccessful':
        new_url = Url.objects.create(
            short_url = 'Unable to generate mini url',
            input_url = input_url,
            status = 'Error',
            created = None,
            alltime = None,
            month = None,
            week = None,
            day = None,
            twohour = None,
            errormessage = obj_list[0]                      
            )
    return new_url

# def create_error_detail(obj):
#     new_obj_count = 0
#     obj = obj.get('error').get('errors')
#     print("Retriving error message details")
#     for item in obj:
#         new_error_detail = ErrorDetail(
#             domain = item.get('domain'),
#             reason = item.get('reason'),
#             message = item.get('message'),
#             locationType = item.get('locationType'),
#             location = item.get('location')
#         )
#         new_error_detail.save()
#         new_obj_count = new_obj_count + 1
#         print(
#             f"""
#             Index: {new_obj_count} | 
#             Domain: {new_error_detail.domain} | 
#             Required: {new_error_detail.reason} |
#             Message: {new_error_detail.message} |
#             Location Type: {new_error_detail.locationType} |
#             Location: {new_error_detail.location}"""
#             )
#     return new_error_detail

def create_error(obj):
    new_obj_count = 0
    obj_list = obj.get('error').get('errors')

    for item in obj_list:
        new_error = Error(
        domain = item.get('domain'),
        reason = item.get('reason'),
        message = item.get('message'),
        locationType = item.get('locationType'),
        location = item.get('location'),
        code = int(obj.get('error').get('code'))
        )
    new_error.save()
    new_obj_count = new_obj_count + 1
    new_error_list = []
    new_error_list.append(new_error)
    print(
        f"""
        Entry Count: {new_obj_count} | 
        Domain: {new_error.domain} | 
        Reason: {new_error.reason} |
        Message: {new_error.message} |
        Location Type: {new_error.locationType} |
        Location: {new_error.location} | 
        Code: {new_error.code} | 
        Message: {new_error.message}
        """
        )
    return new_error_list


