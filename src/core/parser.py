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

import html
import pickle
import re
from collections import defaultdict

from utils import date_parser, export_data, yt_api_metadata


class WatchHistoryParser:
    def __init__(self, filename=None, data_file=None, watch_data=None, get_metadata=False, add_occurences=False,
                 yt_api_key=None, progress_callback=None, only_total_count=False):
        self.watch_data = []
        self.total_items = 0  # excludes deleted
        
        self.filename = filename
        self.yt_api_key = yt_api_key
        self.progress_callback = progress_callback
        self.metadata_included = get_metadata
        if self.filename:
            with open(self.filename, 'rb') as f:
                self.data = f.read()
            self.data = self.data.decode('utf-8')
            self.deleted_count = self.parse_body(get_metadata, add_occurences, only_total_count=only_total_count)
        elif data_file:
            with open(data_file, 'rb') as f:
                data = pickle.load(f)
                self.metadata_included, self.watch_data = data[0], data[1:]
        else:
            self.metadata_included, self.watch_data = watch_data[0], watch_data[1:]
    
    def parse_body(self, get_metadata=False, add_occurences=False, only_total_count=False):
        deleted_count = 0
        self.total_items = 0
        
        timezone_offset = {'MEZ': 1, 'MESZ': 2}
        
        body = re.search('<body><div class="mdl-grid">(.+)</div></body>', self.data, re.DOTALL).group(1)
        items = re.findall('<div class="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"><div class="mdl-grid">'
                           '<div class="header-cell mdl-cell mdl-cell--12-col"><p class="mdl-typography--title">(.+?)<br></p></div>'
                           '<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.+?)</div>'
                           '<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right"></div>'
                           '<div class="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption">'
                           '<b>.+?</b><br>&emsp;.+?<br><b>.+?</b>'
                           '<br>&emsp;.+?'
                           '<a href="https://myaccount.google.com/activitycontrols">.+?'
                           '</a>.*?</div></div></div>', body, re.DOTALL)
        for item in items:
            product, item = item
            music = True if 'YouTube Music' in product else False
            elements = re.search('<a href="(.+?)">(.+?)</a>.*?<br>'
                                 '<a href="(.+?)">(.+?)</a>'
                                 '<br>(.+?)<br>', item, re.DOTALL)
            if elements:
                elements = elements.groups()
                if elements[0].startswith('https://www.youtube.com/post/'):
                    continue
                self.total_items += 1
                if only_total_count:
                    continue
                video_id = re.search(r'^https://(?:music|www)\.youtube\.com/watch\?v=(.+)', elements[0]).group(1)
                wd_dict = {'link': elements[0], 'id': video_id, 'title': html.unescape(elements[1]), 'channel_link': elements[2],
                           'channel': html.unescape(elements[3]),
                           'time_watched': date_parser.parse_date(elements[4]), 'deleted': False, 'music': music}
                
            else:  # video is deleted
                if only_total_count:
                    continue
                elements = re.search('<a href="(.+?)">(.+?)</a>.*?'
                                     '<br>(.+?)<br>', item, re.DOTALL)
                if elements:
                    elements = elements.groups()
                    if elements[0].startswith('https://www.youtube.com/post/'):
                        continue
                    video_id = re.search(r'^https://(?:music|www)\.youtube\.com/watch\?v=(.+)', elements[0]).group(1)
                    wd_dict = {'link': elements[0], 'id': video_id, 'title': '', 'channel_link': None, 'channel': None,
                               'time_watched': date_parser.parse_date(elements[2]), 'deleted': True, 'music': music}
                    deleted_count += 1
                else:
                    continue
            
            metadata = {'upload_date': None, 'language': None, 'views': None, 'likes': None, 'comments': None, 'duration_sec': None}
            wd_dict.update(metadata)
            self.watch_data.append(wd_dict)
        
        # if get_metadata:
        #     links = self.get_all_ids()
        #     yt_api_metadata.add_video_details(links, self.watch_data, self.yt_api_key, progress_callback=self.progress_callback)
        
        if add_occurences:
            self.add_total_occurences()
        
        return deleted_count
    
    def add_metadata(self):
        links = self.get_all_ids()
        yt_api_metadata.add_video_details(links, self.watch_data, self.yt_api_key, progress_callback=self.progress_callback)
    
    def add_missing_metadata(self):
        links = []
        for item in self.watch_data:
            if not item['views'] and not item['deleted']:
                links.append(item['id'])
        yt_api_metadata.add_video_details(links, self.watch_data, self.yt_api_key, progress_callback=self.progress_callback)
    
    def get_missing_metadata_count(self):
        count = 0
        for item in self.watch_data:
            if not item['views'] and not item['deleted']:
                count += 1
        return count
    
    def save_as_txt(self):
        data = ''
        for item in self.watch_data:
            data += item['link'] + '\n'
        
        with open('watchhistory.txt', 'w') as f:
            f.write(data)
    
    def save_watch_data(self, filename, remove_duplicates=True):
        export_data.save_watch_data(filename, self.watch_data, remove_duplicates, metadata_included=self.metadata_included)
    
    def get_all_ids(self):
        video_ids = []
        for item in self.watch_data:
            if item['deleted']:
                continue
            video_id = item['id']
            video_ids.append(video_id)
        return video_ids
    
    def add_total_occurences(self):
        total_occurences = defaultdict(int)
        channel_occurences = defaultdict(int)
        for item in self.watch_data:
            total_occurences[item['link']] += 1
            channel_occurences[item['channel']] += 1
        
        for item in self.watch_data:
            item['total_occurences'] = total_occurences[item['link']]
            item['channel_occurences'] = channel_occurences[item['channel']]
