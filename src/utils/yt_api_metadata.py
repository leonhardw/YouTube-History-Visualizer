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

import isodate
from googleapiclient.discovery import build

from utils import date_parser


def add_video_details(video_ids, watch_data, yt_api_key, progress_callback=None):
    youtube = build('youtube', 'v3', developerKey=yt_api_key)
    all_stats = []
    
    for i in range(0, len(video_ids), 50):
        if progress_callback:
            progress_callback(i, len(video_ids))
        batch = video_ids[i:i + 50]
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(batch)
        )
        response = request.execute()
        if 'items' not in response:
            pass
        for j, item in enumerate(response.get('items', [])):
            duration_raw = item['contentDetails']['duration']
            # Converts ISO 8601 (PT10M30S) into seconds
            duration_seconds = isodate.parse_duration(duration_raw).total_seconds()
            video_id = item['id']
            data = {
                'upload_date': date_parser.parse_date_yt_api(item['snippet']['publishedAt']),
                'language': item['snippet']['defaultLanguage'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'comments': int(item['statistics'].get('commentCount', 0)),
                'duration_sec': duration_seconds
            }
            for video in watch_data:
                if video['id'] == video_id:
                    video.update(data)
