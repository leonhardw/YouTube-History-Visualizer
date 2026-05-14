#  Copyright (C) 2026  leonhardw
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import locale
import re
from datetime import time

locale.setlocale(locale.LC_ALL, '')
int_to_weekdays = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}


def secs_to_time(secs):
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(hours % 24, minutes, seconds)


def date_to_str(date, date_range=None):
    min_, max_ = date
    min_str = min_.strftime('%x')
    max_str = max_.strftime('%x')
    
    if date_range:
        if min_ == date_range[0].date():
            min_ = 0
        if max_ == date_range[1].date():
            max_ = 0
    else:
        min_str, max_str = f'{min_:n}', f'{max_:n}'
    if min_ == max_ == 0:
        return f'on any date'
    if min_ == 0:
        return f'earlier than {max_str}'
    if max_ == 0:
        return f'later than {min_str}'
    if min_ == max_:
        return f'on {min_str}'
    else:
        return f'in date range {min_str}-{max_str}'


def range_to_str(range_, to_time=False, no_format=False):
    min_, max_ = range_
    if to_time:
        min_str, max_str = secs_to_time(min_), secs_to_time(max_)
        
    elif no_format:
        min_str, max_str = min_, max_
    else:
        min_str, max_str = f'{min_:n}', f'{max_:n}'
    if min_ == 0:
        return f'max. {max_str}'
    if max_ == 0:
        return f'min. {min_str}'
    else:
        return f'{min_str}-{max_str}'


def filter_to_str(filter_, view_date_range=None, upload_date_range=None):
    filter_strs = []
    if filter_:
        available = filter_['availability']['available']
        deleted = filter_['availability']['deleted']
        if available and deleted:
            availability = 'All'
        elif available and not deleted:
            availability = 'Available'
        elif not available and deleted:
            availability = 'Deleted'
        else:
            availability = ''
        
        # ---------- Platform filters ---------- #
        yt = filter_['platform']['youtube']
        yt_music = filter_['platform']['music']
        if yt and yt_music:
            platform = ''
        elif yt and not yt_music:
            platform = 'YouTube videos'
        elif not yt and yt_music:
            platform = 'YouTube Music songs'
        else:
            platform = ''
        if platform:
            filter_strs.append(f'{availability} {platform}')
        else:
            filter_strs.append(availability)
        for key, value in filter_.items():
            include = '' if value['include'] else 'not '
            match key:
                case 'title':
                    filter_strs.append(f'Title: {include}"{value['value']}"')
                case 'channel':
                    filter_strs.append(f'Channel: {include}"{value['value']}"')
                case 'languages':
                    filter_strs.append(f'Languages: {include}"{value['values']}"')
                case 'total_views':
                    filter_strs.append(f'Total views: {include}{range_to_str(value['range'])}')
                case 'user_views':
                    filter_strs.append(f'My views: {include}{range_to_str(value['range'])}')
                case 'user_channel_views':
                    filter_strs.append(f'My views per channel: {include}{range_to_str(value['range'])}')
                case 'duration':
                    filter_strs.append(f'Duration: {include}{range_to_str(value['range'], to_time=True)}')
                
                # ---------- Watched time filters ---------- #
                case 'date_watched':
                    filter_strs.append(f'Watched: {include}{date_to_str(value['range'], date_range=view_date_range)}')
                case 'time_watched':
                    filter_strs.append(f'Watched in time range: {include}{range_to_str(value['range'], no_format=True)}')
                case 'days_of_month_watched':
                    filter_strs.append(f'Watched on days of month: {include}{value['values']}')
                case 'months_watched':
                    filter_strs.append(f'Watched in months: {include}{value['values']}')
                case 'weekdays_watched':
                    weekdays = tuple(int_to_weekdays[i] for i in value['values'])
                    filter_strs.append(f'Watched on weekdays: {include}{weekdays}')
                
                # ---------- Uploaded time filters ---------- #
                case 'date_uploaded':
                    filter_strs.append(f'Uploaded: {include}{date_to_str(value['range'], date_range=upload_date_range)}')
                case 'time_uploaded':
                    filter_strs.append(f'Uploaded in time range: {include}{range_to_str(value['range'], no_format=True)}')
                case 'days_of_month_uploaded':
                    filter_strs.append(f'Uploaded on days of month: {include}{value['values']}')
                case 'months_uploaded':
                    filter_strs.append(f'Uploaded in months: {include}{value['values']}')
                case 'weekdays_uploaded':
                    weekdays = tuple(int_to_weekdays[i] for i in value['values'])
                    filter_strs.append(f'Uploaded on weekdays: {include}{weekdays}')
        
        return '; '.join(filter_strs)
    else:
        return 'No filters'


def advanced_filters(watch_data, filters_list):
    all_matching_items = []
    for filters in filters_list:
        all_matching_items.extend(process_filter(watch_data, filters))
    
    all_matching_items = remove_duplicates(all_matching_items)
    return all_matching_items


def remove_duplicates(dict_list):
    seen = set()
    unique_data = []
    
    for d in dict_list:
        fingerprint = frozenset(d.items())
        
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_data.append(d)
    
    return unique_data


def process_filter(watch_data, filters):
    matching_items = []
    for item in watch_data:
        filters_to_check = []
        for key, value in filters.items():
            include = value['include']
            match key:
                case 'title':
                    use_regex = value['regex']
                    if include:
                        if use_regex:
                            filters_to_check.append(re.search(value['value'], item['title'], re.IGNORECASE))
                        else:
                            filters_to_check.append(value['value'].lower() in item['title'].lower())
                    else:
                        if use_regex:
                            filters_to_check.append(not re.search(value['value'], item['title'], re.IGNORECASE))
                        else:
                            filters_to_check.append(value['value'].lower() not in item['title'].lower())
                
                case 'channel':
                    use_regex = value['regex']
                    if item['channel'] is None:
                        filters_to_check.append(not include)  # if channel not available: ignore item unless excluding channel
                    else:
                        if include:
                            if use_regex:
                                filters_to_check.append(re.search(value['value'], item['channel'], re.IGNORECASE))
                            else:
                                filters_to_check.append(value['value'].lower() in item['channel'].lower())
                        else:
                            if use_regex:
                                filters_to_check.append(not re.search(value['value'], item['channel'], re.IGNORECASE))
                            else:
                                filters_to_check.append(value['value'].lower() not in item['channel'].lower())
                
                case 'languages':
                    languages = {i.strip().lower() for i in value['values'].split(',')}
                    if include:
                        filters_to_check.append(item['language'] in languages)
                    else:
                        filters_to_check.append(not item['language'] in languages)
                
                case 'user_views':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_range(min_, max_, item['total_occurences']))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'total_views':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_range(min_, max_, item['views']))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'user_channel_views':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_range(min_, max_, item['channel_occurences']))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'duration':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_range(min_, max_, item['duration_sec']))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'platform':
                    # ignore 'include' for now
                    if value['youtube']:
                        if value['music']:
                            filters_to_check.append(True)  # include all
                        else:
                            filters_to_check.append(not item['music'])
                    else:
                        if value['music']:
                            filters_to_check.append(item['music'])
                        else:
                            filters_to_check.append(False)
                
                case 'availability':
                    # ignore 'include' for now
                    if value['available']:
                        if value['deleted']:
                            filters_to_check.append(True)  # include all
                        else:
                            filters_to_check.append(not item['deleted'])
                    else:
                        if value['deleted']:
                            filters_to_check.append(item['deleted'])
                        else:
                            filters_to_check.append(False)
                
                case 'date_watched':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_date_range(min_, max_, item['time_watched'].date()))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'time_watched':
                    min_, max_ = value['range']
                    filters_to_check.append(check_in_date_range(min_, max_, item['time_watched'].time(), only_time=True))
                    
                    if not include:
                        filters_to_check[-1] = not filters_to_check[-1]
                
                case 'days_of_month_watched':
                    all_days = str_to_list(value['values'])
                    day_of_view = item['time_watched'].day
                    
                    filters_to_check.append(check_in_sequence(day_of_view, all_days, include))
                
                case 'months_watched':
                    all_months = str_to_list(value['values'])
                    month_of_view = item['time_watched'].month
                    
                    filters_to_check.append(check_in_sequence(month_of_view, all_months, include))
                
                case 'weekdays_watched':
                    # monday=0, sunday=6
                    all_weekdays = value['values']
                    weekday_of_view = item['time_watched'].weekday()
                    
                    filters_to_check.append(check_in_sequence(weekday_of_view, all_weekdays, include))
                
                case 'date_uploaded':
                    min_, max_ = value['range']
                    upload_date = item['upload_date']
                    if upload_date:
                        filters_to_check.append(check_in_date_range(min_, max_, upload_date.date()))
                        
                        if not include:
                            filters_to_check[-1] = not filters_to_check[-1]
                    else:
                        filters_to_check.append(not include)
                
                case 'time_uploaded':
                    upload_date = item['upload_date']
                    if upload_date:
                        min_, max_ = value['range']
                        filters_to_check.append(check_in_date_range(min_, max_, upload_date.time(), only_time=True))
                        
                        if not include:
                            filters_to_check[-1] = not filters_to_check[-1]
                    else:
                        filters_to_check.append(not include)
                
                case 'days_of_month_uploaded':
                    all_days = str_to_list(value['values'])
                    day_of_upload = item['upload_date']
                    
                    if day_of_upload:
                        filters_to_check.append(check_in_sequence(day_of_upload.day, all_days, include))
                    else:
                        filters_to_check.append(not include)  # data unavailable -> only match filter if excluded
                
                case 'months_uploaded':
                    all_months = str_to_list(value['values'])
                    month_of_upload = item['upload_date']
                    
                    if month_of_upload:
                        filters_to_check.append(check_in_sequence(month_of_upload.month, all_months, include))
                    else:
                        filters_to_check.append(not include)
                
                case 'weekdays_uploaded':
                    # monday=0, sunday=6
                    all_weekdays = value['values']
                    weekday_of_upload = item['time_watched'].weekday()
                    
                    if weekday_of_upload:
                        filters_to_check.append(check_in_sequence(weekday_of_upload, all_weekdays, include))
                    else:
                        filters_to_check.append(not include)
            
            if False in filters_to_check:
                break
        
        if all(filters_to_check):
            matching_items.append(item)
    
    return matching_items


def check_in_range(min_, max_, value):
    if value is None:
        return False
    if min_ > 0:
        if max_ > 0:
            return min_ <= value <= max_
        else:
            return min_ <= value
    else:
        return value <= max_


def check_in_date_range(min_, max_, value, only_time=False):
    if value is None:
        return False
    
    if only_time:
        value = value.replace(microsecond=0)
    return min_ <= value <= max_


def str_to_list(value, check_day=False, check_month=False):
    numbers_list = []
    try:
        numbers = (i.strip().lower() for i in value.split(','))
        for number in numbers:
            if check_day:
                if not 1 <= int(number) <= 31:
                    return False
            if check_month:
                if not 1 <= int(number) <= 12:
                    return False
            if '-' in number:
                start, end = (int(i.strip()) for i in number.split('-'))
                numbers_list.extend(range(start, end + 1))
            else:
                numbers_list.append(int(number))
    except:
        return False
    
    return numbers_list


def check_in_sequence(value, sequence, include):
    if include:
        return value in sequence
    else:
        return value not in sequence
