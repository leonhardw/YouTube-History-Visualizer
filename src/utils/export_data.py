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

import csv
import pickle

from utils import advanced_filters


def save_as_csv(filename, data):
    if isinstance(data, list):
        fieldnames = data[0]
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(data)
    
    elif isinstance(data, dict):
        fieldnames = data[0].keys()
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)


def save_watch_data(filename, data, remove_duplicates=True, metadata_included=False):
    if remove_duplicates:
        data = advanced_filters.remove_duplicates(data)
    with open(filename, 'wb') as f:
        pickle.dump([metadata_included] + data, f)
