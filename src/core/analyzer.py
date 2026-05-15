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

import calendar
import math
import pickle
from collections import defaultdict
from datetime import datetime, timedelta, time, date

import numpy as np

from utils import date_parser
from utils import export_data
from utils.advanced_filters import advanced_filters, int_to_weekdays

VIEW = 'time_watched'
UPLOAD = 'upload_date'


def filter_view_date_range(watch_data, start=None, end=None):
    matching_videos = []
    if start and isinstance(start, date):
        start = datetime.combine(start, time.min)
    if end and isinstance(end, date):
        end = datetime.combine(end, time.max)
    for video in watch_data:
        if (not start or video['time_watched'] >= start) and (not end or video['time_watched'] < end):
            matching_videos.append(video)
    return matching_videos


def filter_upload_date_range(watch_data, start=None, end=None):
    matching_videos = []
    if start and isinstance(start, date):
        start = datetime.combine(start, time.min)
    if end and isinstance(end, date):
        end = datetime.combine(end, time.max)
    for video in watch_data:
        upload_date = video.get('upload_date')
        if upload_date:
            if (not start or upload_date >= start) and (not end or upload_date < end):
                matching_videos.append(video)
    return matching_videos


def load_watch_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        return data[0], data[1:]


class WatchHistoryAnalyzer:
    def __init__(self, watch_data, metadata_included=False):
        self.watch_data = watch_data
        self.metadata_included = metadata_included
        self.total_videos = len(self.watch_data)
        self.original_data = self.watch_data.copy()
        self.filtered_data = self.watch_data.copy()
        
        self.update_date_range()
    
    def update_date_range(self):
        self.date_range = self._get_oldest_and_newest(mode=VIEW)
        if self.date_range:
            self.first_date, self.last_date = self.date_range
            self.date_range = list(self.date_range)
        self.upload_date_range = self._get_oldest_and_newest(mode=UPLOAD)
        if self.upload_date_range:
            self.first_upload_date, self.last_upload_date = self.upload_date_range
            self.upload_date_range = list(self.upload_date_range)
        else:
            self.first_upload_date, self.last_upload_date = datetime(1970, 1, 1), datetime(1970, 1, 1)
            self.upload_date_range = [self.first_upload_date, self.last_upload_date]
    
    def get_videos_per_channel(self):
        videos_per_channel = defaultdict(int)  # [('name', 'url'): counter, ...}
        for video in self.watch_data:
            if video['channel'] is None:
                channel_name = 'Deleted'
            else:
                if video['music']:
                    channel_name = video['channel'].removesuffix(' - Topic')
                else:
                    channel_name = video['channel']
            channel_tuple = (channel_name, video['channel_link'])
            videos_per_channel[channel_tuple] += 1
        
        return dict(videos_per_channel)
    
    def get_most_watched_videos(self):
        most_watched_videos = {}
        for video in self.watch_data:
            video_tuple = (video['title'], video['link'])
            if most_watched_videos.get(video_tuple) is None:
                most_watched_videos[video_tuple] = video['total_occurences']
            else:
                if most_watched_videos[video_tuple] != video['total_occurences']:
                    print(video_tuple, most_watched_videos[video_tuple], video['total_occurences'], video['channel'])

        return most_watched_videos
    
    def get_videos_per_year(self, mode=VIEW, include_unused=True):
        videos_per_year = defaultdict(int)
        if include_unused:
            first, last = self._get_oldest_and_newest(mode=mode)
            for year in range(first.year, last.year + 1):
                videos_per_year[year] = 0
        for video in self.watch_data:
            video_date = video.get(mode)
            if video_date:
                year = video_date.year
                videos_per_year[year] += 1
        return dict(videos_per_year)
    
    def get_videos_per_weekday(self, mode=VIEW):
        videos_per_weekday = {value: 0 for value in int_to_weekdays.values()}
        for video in self.watch_data:
            video_date = video.get(mode)
            if video_date:
                weekday = int_to_weekdays[video_date.weekday()]
                videos_per_weekday[weekday] += 1
        return dict(videos_per_weekday)
    
    def get_videos_per_time(self, accuracy=1, include_unused=False, mode=VIEW):
        videos_per_time = defaultdict(int)
        
        if include_unused:
            current = datetime.combine(datetime.today(), time(0, 0))
            end = datetime.combine(datetime.today(), time(23, 59))
            while current <= end:
                t = current.time()
                videos_per_time[t] = 0
                current += timedelta(minutes=accuracy)
        
        for video in self.watch_data:
            video_date = video.get(mode)
            if not video_date:
                continue
            if accuracy > 1:
                minutes = video_date.minute
                floored_minutes = math.floor(minutes / accuracy) * accuracy
                if floored_minutes >= 60:
                    video_date += timedelta(hours=1)
                    floored_minutes -= 60
                video_date = video_date.replace(minute=floored_minutes, second=0, microsecond=0)
            videos_per_time[video_date.time()] += 1
        return dict(videos_per_time)
    
    def get_videos_per_month(self, include_unused=False, mode=VIEW):
        videos_per_month = defaultdict(int)
        if include_unused:
            for i in range(1, 13):
                videos_per_month[i] = 0
        
        for video in self.watch_data:
            video_date = video.get(mode)
            if video_date:
                videos_per_month[video_date.month] += 1
        
        return dict(videos_per_month)
    
    def get_videos_per_day(self, include_unused=False, last_day_of_month=31, mode=VIEW):
        videos_per_day = defaultdict(int)
        if include_unused:
            for i in range(1, last_day_of_month + 1):
                videos_per_day[i] = 0
        
        for video in self.watch_data:
            video_date = video.get(mode)
            if video_date:
                videos_per_day[video_date.day] += 1
        
        return dict(videos_per_day)
    
    def get_times_per_year(self, accuracy=1, absolute=True, mode=VIEW):
        times_per_year = {}
        if mode == VIEW:
            first_year = self.first_date.year
            last_year = self.last_date.year
        elif mode == UPLOAD:
            first_year = self.first_upload_date.year
            last_year = self.last_upload_date.year
        else:
            raise ValueError('Invalid mode')
        for year in range(first_year, last_year + 1):
            self.set_date_range(date(year, 1, 1), date(year + 1, 1, 1), mode=mode)
            videos_per_time = self.get_videos_per_time(accuracy, True, mode=mode)
            total_videos_per_year = sum(videos_per_time.values())
            if absolute:
                times_per_year[year] = videos_per_time
            else:
                percentages = {}
                for key, value in videos_per_time.items():
                    percentages[key] = value / total_videos_per_year
                times_per_year[year] = percentages
            self.reset_date_range()
        return times_per_year
    
    def get_all_months(self, mode=VIEW):
        all_months = []
        if mode == VIEW:
            first_year = self.first_date.year
            last_year = self.last_date.year
        elif mode == UPLOAD:
            first_year = self.first_upload_date.year
            last_year = self.last_upload_date.year
        else:
            raise ValueError('Invalid mode')
        for year in range(first_year, last_year + 1):
            self.set_date_range(date(year, 1, 1), date(year + 1, 1, 1), mode=mode)
            all_months.extend(self.get_videos_per_month(True, mode=mode).values())
            self.reset_date_range()
        
        all_months = np.trim_zeros(all_months, 'fb')
        all_months_dict = {}
        for i, month in enumerate(all_months):
            all_months_dict[i] = month
        return all_months_dict
    
    def get_days_per_year(self, year, mode=VIEW):
        all_days = []
        for month in range(1, 13):
            if month == 12:
                self.set_date_range(date(year, month, 1), date(year + 1, 1, 1), mode=mode)
            else:
                self.set_date_range(date(year, month, 1), date(year, month + 1, 1), mode=mode)
            days_per_month = self.get_videos_per_day(True, calendar.monthrange(year, month)[1], mode=mode).values()
            all_days.extend(days_per_month)
            self.reset_date_range()
        all_days_dict = {}
        for i, day in enumerate(all_days):
            all_days_dict[i] = day
        return all_days_dict
    
    def get_languages(self):
        languages = defaultdict(int)
        for video in self.watch_data:
            language = video.get('language', None)
            if language is not None:
                language = language[:2]
            else:
                language = 'Unknown'
            languages[language] += 1
        return dict(languages)
    
    def get_videos_per_views(self, include_unused=False):
        views_per_video = defaultdict(int)
        suffixes = ['', 'k', 'M', 'B', 'T']
        if include_unused:
            max_views = self._get_most_video_views()
            i = 10
            while i < max_views:
                views_per_video[i] = 0
                i *= 10
            views_per_video['Unknown'] = 0
        
        for video in self.watch_data:
            views = video['views']
            if views is None:
                views_per_video['Unknown'] += 1
            else:
                if views < 1:
                    views = 1
                # prevent 2.99999999 from getting floored to 2
                exponent = math.floor(math.log(views, 10) + 1e-12)
                floored_views = 10 ** exponent
                views_per_video[floored_views] += 1
        
        suffixes_dict = {}
        for view_count in views_per_video.keys():
            if view_count == 'Unknown':
                continue
            exponent = math.floor(math.log(view_count, 10) + 1e-12)
            suffix_idx = exponent // 3
            short_val = 10 ** (exponent % 3)
            suffix = suffixes[suffix_idx]
            views_with_suffix = f'{short_val}{suffix}'
            suffixes_dict[view_count] = views_with_suffix
        
        return dict(views_per_video), suffixes_dict
    
    def get_videos_per_duration(self, steps=(0, 10, 30, 60, 120, 300, 600, 1800, 3600, 7200), include_unused=False):
        videos_per_duration = defaultdict(int)
        
        if include_unused:
            max_duration = self._get_longest_video()
            for step in steps:
                videos_per_duration[step] = 0
            videos_per_duration['Unknown'] = 0
        
        for video in self.watch_data:
            duration = video['duration_sec']
            if duration is None:
                videos_per_duration['Unknown'] += 1
            else:
                for step in steps[::-1]:
                    if duration >= step:
                        duration = step
                        break
                videos_per_duration[duration] += 1
        
        formatted_durations = {}
        for i in videos_per_duration.keys():
            if i == 'Unknown':
                continue
            formatted_durations[i] = date_parser.format_seconds(i)
        
        return dict(videos_per_duration), formatted_durations
    
    def get_own_views_per_video(self):
        own_views_per_video = set()
        for video in self.watch_data:
            own_views_per_video.add((video['id'], video['title'], video['total_occurences']))
        own_views_per_video = list(own_views_per_video)
        own_views_per_video.sort(key=lambda x: x[2], reverse=True)
        own_views_per_video = [i for i in own_views_per_video if i[2] > 1]
        return own_views_per_video
    
    def set_date_range(self, start=None, end=None, mode=VIEW):
        if start:
            if mode == VIEW:
                self.date_range[0] = start
            elif mode == UPLOAD:
                self.upload_date_range[0] = start
        if end:
            if mode == VIEW:
                self.date_range[1] = end
            elif mode == UPLOAD:
                self.upload_date_range[1] = end
        if mode == VIEW:
            self.watch_data = filter_view_date_range(self.watch_data, start, end)
        elif mode == UPLOAD:
            self.watch_data = filter_upload_date_range(self.watch_data, start, end)
    
    def reset_filters(self):
        self.watch_data = self.original_data
        self.date_range = self._get_oldest_and_newest()
    
    def reset_date_range(self):
        self.watch_data = self.filtered_data.copy()
        self.update_date_range()
    
    def apply_advanced_filters(self, filters):
        self.reset_filters()
        self.watch_data = advanced_filters(self.original_data, filters)
        self.filtered_data = self.watch_data.copy()
        self.update_date_range()
    
    def to_table(self):
        header_strings = {'link': 'Link', 'id': 'Video ID', 'title': 'Video title', 'channel': 'Channel',
                          'channel_link': 'Channel link', 'time_watched': 'Watched at', 'deleted': 'Deleted',
                          'music': 'YouTube Music', 'upload_date': 'Uploaded at', 'language': 'Language',
                          'views': 'Global views', 'likes': 'Likes', 'comments': 'Comments', 'duration_sec': 'Duration (in s)',
                          'total_occurences': 'My views', 'channel_occurences': 'My views per channel'}
        headers = tuple(header_strings.values())
        video_list = [headers]
        for video in self.watch_data:
            video_data = []
            for key in header_strings.keys():
                video_data.append(video[key])
            video_list.append(video_data)
        return video_list
    
    def save_watch_data(self, filename, remove_duplicates=True):
        export_data.save_watch_data(filename, self.watch_data, remove_duplicates, metadata_included=self.metadata_included)
    
    def save_as_csv(self, filename):
        export_data.save_as_csv(filename, self.watch_data)
    
    def _get_oldest_and_newest(self, original_data=False, mode=VIEW):
        dates = []
        watch_data = self.original_data if original_data else self.watch_data
        for video in watch_data:
            if video[mode] is not None:
                dates.append(video[mode])
        dates.sort()
        if len(dates) < 2:
            return None
        return dates[0], dates[-1]
    
    def _get_most_video_views(self):
        views = []
        for video in self.watch_data:
            if video['views'] is None:
                views.append(-1)
            else:
                views.append(video['views'])
        views.sort()
        return views[-1]
    
    def _get_longest_video(self):
        durations = []
        for video in self.watch_data:
            if video['duration_sec'] is not None:
                durations.append(video['duration_sec'])
        durations.sort()
        return durations[-1]
