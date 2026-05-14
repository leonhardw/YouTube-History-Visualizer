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
from datetime import datetime

from dateutil import parser


def get_order_by_locale():
    try:
        loc = locale.getlocale()[0] or "en_US"
    except:
        loc = "en_US"
    return 'MDY' if "US" in loc.upper() else 'DMY'


def parse_date(date_str):
    return parser.parse(date_str, ignoretz=True, dayfirst=True if get_order_by_locale() == 'DMY' else False)


def parse_date_yt_api(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')


def format_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f'{hours}:{minutes:02} h'
    elif minutes > 0:
        return f'{minutes}:{secs:02} min'
    else:
        return f'{secs} s'


if __name__ == '__main__':
    tests = [
        'May 13, 2026, 02:00:00 PM UTC+08:00',  # China
        '13.05.2026 14:00:00 MESZ',  # Germany
        '13/5/26 14:00',
        'May 13, 2026, 2:00:00 PM PT',  # USA
        '06/07/08 12:30:00 AM',  # DD/MM/YYYY or MM/DD/YYYY?
    ]
    for date in tests:
        print(parse_date(date))
