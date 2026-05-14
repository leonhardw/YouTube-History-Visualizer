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

from datetime import datetime, timedelta
from typing import Literal

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta

from core.analyzer import UPLOAD, VIEW

plt.rcParams['figure.figsize'] = [14.0, 7.0]


def absolute_values(pct, allvals):
    absolute = int(round(pct / 100. * sum(allvals)))
    return f'{absolute}'


class WatchHistoryVisualizer:
    def __init__(self, watch_analyzer):
        self.watch_analyzer = watch_analyzer
        self.save_plots = False
        self.save_filename = None
    
    def handle_chart(self, filename=None):
        if self.save_plots:
            plt.savefig(self.save_filename if self.save_filename else filename)
            plt.close()
        else:
            plt.show()
    
    def get_videos_per_channel(self, min_videos_per_channel=50):
        videos_per_channel = self.watch_analyzer.get_videos_per_channel()
        x = tuple(channel[0] for channel in videos_per_channel.keys())
        y = tuple(videos_per_channel.values())
        pairs = list(zip(x, y))
        pairs.sort(key=lambda x: x[1], reverse=True)
        x, y = zip(*pairs)
        
        cleared_x = []
        cleared_y = []
        
        other_count = 0
        for i, count in enumerate(y):
            if count > min_videos_per_channel:
                cleared_x.append(x[i])
                cleared_y.append(y[i])
            else:
                other_count += 1
        
        cleared_x.append('Other')
        cleared_y.append(other_count)
        
        return cleared_x, cleared_y
    
    def visualize_videos_per_channel(self, min_videos_per_channel=50):
        x, y = self.get_videos_per_channel(min_videos_per_channel)
        plt.figure()
        plt.pie(y, labels=x, autopct=lambda pct: absolute_values(pct, y),
                pctdistance=0.8, labeldistance=1.025)
        plt.title(self.get_chart_title())
        self.handle_chart('channels.png')
    
    def get_videos_per_date_unit(self, unit: Literal['year', 'month', 'day', 'weekday'], mode=VIEW):
        match unit:
            case 'year':
                videos_per_unit = self.watch_analyzer.get_videos_per_year(mode=mode)
            case 'month':
                videos_per_unit = self.watch_analyzer.get_videos_per_month(True, mode=mode)
            case 'day':
                videos_per_unit = self.watch_analyzer.get_videos_per_day(True, mode=mode)
            case 'weekday':
                videos_per_unit = self.watch_analyzer.get_videos_per_weekday(mode=mode)
            case _:
                raise ValueError('Unrecognized unit')
        x = tuple(videos_per_unit.keys())
        y = tuple(videos_per_unit.values())
        
        return x, y
    
    def visualize_videos_per_date_unit(self, unit: Literal['year', 'month', 'day', 'weekday'], mode=VIEW):
        x, y = self.get_videos_per_date_unit(unit, mode)
        
        plt.figure()
        bars = plt.bar(x, y)
        plt.gca().bar_label(bars, padding=3)
        plt.xticks(x)
        plt.title(self.get_chart_title(mode))
        self.handle_chart(f'{unit}s_{mode}.png')
    
    def get_videos_per_time(self, accuracy=30, rotate=0, mode=VIEW):
        rotate //= accuracy
        videos_per_time = self.watch_analyzer.get_videos_per_time(accuracy, True, mode=mode)
        x = tuple(i.strftime('%H:%M') for i in videos_per_time.keys())
        y = tuple(videos_per_time.values())
        
        pairs = list(zip(x, y))
        pairs.sort(key=lambda x: x[0])
        x, y = zip(*pairs)
        x = x[rotate:] + x[:rotate]
        y = y[rotate:] + y[:rotate]
        
        return x, y
    
    def visualize_videos_per_time(self, accuracy=30, rotate=0, mode=VIEW):
        x, y = self.get_videos_per_time(accuracy, rotate, mode)
        plt.figure()
        bars = plt.bar(x, y)
        plt.gca().bar_label(bars, padding=3, rotation=90)
        plt.xticks(rotation=90)
        plt.title(self.get_chart_title(mode))
        self.handle_chart(f'time_{mode}.png')
    
    def get_time_per_year(self, accuracy=30, rotate=0, absolute=True, mode=VIEW, as_heatmap=True):
        rotate //= accuracy
        times_per_year = self.watch_analyzer.get_times_per_year(accuracy=accuracy, absolute=absolute, mode=mode)
        original_df = pd.DataFrame(times_per_year)
        df = pd.DataFrame(
            np.roll(original_df.values, rotate, axis=0),
            index=np.roll(original_df.index, rotate),
            columns=original_df.columns
        )
        df.index.name = 'Time'
        df.columns.name = 'Year'
        if as_heatmap:
            return df
        else:
            return [df.columns.tolist()] + df.reset_index().values.tolist()
    
    def visualize_time_per_year_heatmap(self, accuracy=30, rotate=0, absolute=True, mode=VIEW):
        df = self.get_time_per_year(accuracy, rotate, absolute, mode)
        yticks_labels = [str(label)[:5] if i % (60 / accuracy) == 0 else '' for i, label in enumerate(df.index)]
        plt.figure(figsize=(14, 7))
        ax = sns.heatmap(df, annot=False, fmt='d', cmap='coolwarm', yticklabels=yticks_labels, cbar_kws={'pad': 0.1})
        
        positions = [i for i, label in enumerate(df.index) if str(label).endswith(':00:00')]
        
        ax.hlines(positions, *ax.get_xlim(), colors='black', linewidth=.5)
        
        ax_right = ax.twinx()
        ax_right.set_ylim(ax.get_ylim())
        ax_right.set_yticks(ax.get_yticks())
        ax_right.set_yticklabels(yticks_labels)
        
        for axis in [ax, ax_right]:
            for i, tick in enumerate(axis.yaxis.get_major_ticks()):
                label_text = yticks_labels[i]
                
                if label_text.endswith(':00'):
                    tick.tick1line.set_markersize(7)
                    tick.tick1line.set_markeredgewidth(1.2)
                    tick.tick2line.set_markersize(7)
                    tick.tick2line.set_markeredgewidth(1.2)
        
        current_ticks = ax.get_yticks()
        
        new_ticks = current_ticks - 0.5
        
        ax.set_yticks(new_ticks)
        ax.set_yticklabels(yticks_labels)
        
        ax_right.set_yticks(new_ticks)
        ax_right.set_yticklabels(yticks_labels)
        
        plt.title(self.get_chart_title(mode))
        self.handle_chart(f'heatmap{'_percentages' if not absolute else ''}_{mode}.png')
    
    def get_videos_per_language(self, min_videos_per_language):
        videos_per_language = self.watch_analyzer.get_languages()
        x = tuple(videos_per_language.keys())
        y = tuple(videos_per_language.values())
        pairs = list(zip(x, y))
        pairs.sort(key=lambda x: x[1], reverse=True)
        x, y = zip(*pairs)
        
        cleared_x = []
        cleared_y = []
        
        other_count = 0
        for i, count in enumerate(y):
            if count > min_videos_per_language:
                cleared_x.append(x[i])
                cleared_y.append(y[i])
            else:
                other_count += 1
        
        cleared_x.append('Other')
        cleared_y.append(other_count)
        
        return cleared_x, cleared_y
    
    def visualize_videos_per_language(self, min_videos_per_language=50):
        x, y = self.get_videos_per_language(min_videos_per_language)
        
        plt.figure()
        plt.pie(y, labels=x, autopct=lambda pct: absolute_values(pct, y),
                pctdistance=0.8, labeldistance=1.025)
        plt.title(self.get_chart_title())
        self.handle_chart('languages.png')
    
    def get_videos_per_views(self):
        videos_per_views, suffixes = self.watch_analyzer.get_videos_per_views(True)
        unknown_views = videos_per_views['Unknown']
        del videos_per_views['Unknown']
        x = tuple(videos_per_views.keys())
        y = tuple(videos_per_views.values())
        
        pairs = list(zip(x, y))
        pairs.sort(key=lambda x: x[0])
        x, y = zip(*pairs)
        x, y = list(x), list(y)
        x_with_suffixes = []
        for view_count in x:
            x_with_suffixes.append(suffixes.get(view_count, view_count))
        x_with_suffixes.append('Unknown')
        y.append(unknown_views)
        
        return x_with_suffixes, y
    
    def visualize_videos_per_views(self):
        x, y = self.get_videos_per_views()
        
        plt.figure()
        bars = plt.bar(x, y)
        plt.gca().bar_label(bars, padding=3)
        # plt.xticks(rotation=90)
        plt.title(self.get_chart_title())
        self.handle_chart('views.png')
    
    def get_videos_per_duration(self):
        videos_per_duration, formatted_durations = self.watch_analyzer.get_videos_per_duration((0, 10, 30, 60, 120, 180, 240, 300, 600, 1800, 3600, 7200), True)
        unknown_durations = videos_per_duration['Unknown']
        del videos_per_duration['Unknown']
        x = tuple(videos_per_duration.keys())
        y = tuple(videos_per_duration.values())
        
        pairs = list(zip(x, y))
        pairs.sort(key=lambda x: x[0])
        x, y = zip(*pairs)
        x, y = list(x), list(y)
        x_as_time = []
        for duration_count in x:
            x_as_time.append(formatted_durations.get(duration_count, None))
        x_as_time.append('Unknown')
        y.append(unknown_durations)
        
        return x_as_time, y
    
    def visualize_videos_per_duration(self):
        x, y = self.get_videos_per_duration()
        
        plt.figure()
        bars = plt.bar(x, y)
        plt.gca().bar_label(bars, padding=3)
        # plt.xticks(rotation=90)
        plt.title(self.get_chart_title())
        self.handle_chart('durations.png')
    
    def get_all_months(self, mode=VIEW):
        all_months = self.watch_analyzer.get_all_months(mode=mode)
        if mode == VIEW:
            first_video = self.watch_analyzer.date_range[0].replace(hour=0, minute=0, second=0, microsecond=0)
        elif mode == UPLOAD:
            first_video = self.watch_analyzer.upload_date_range[0].replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError('Mode must be either VIEW or UPLOAD')
        x = tuple(first_video + relativedelta(months=month) for month in all_months.keys())
        y = tuple(all_months.values())
        
        return x, y
    
    def visualize_all_months(self, mode=VIEW):
        x, y = self.get_all_months(mode)
        
        plt.figure()
        bars = plt.plot(x, y)
        ax = plt.gca()
        if x[0].year == x[-1].year:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        else:
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.tick_params(which='minor', length=4, color='gray')
        ax.tick_params(which='major', length=7, width=1.2, color='gray')
        plt.xlim(min(x), max(x))
        plt.ylim(min(y), max(y) * 1.1)
        plt.title(self.get_chart_title(mode))
        self.handle_chart(f'all_months_{mode}.png')
    
    def get_days_per_year(self, year, mode=VIEW):
        days_per_year = self.watch_analyzer.get_days_per_year(year, mode=mode)
        x = tuple(datetime(year, 1, 1) + timedelta(days=day) for day in days_per_year.keys())
        y = tuple(days_per_year.values())
        
        return x, y
    
    def visualize_days_per_year(self, year, mode=VIEW):
        x, y = self.get_days_per_year(year, mode)
        
        plt.figure()
        bars = plt.plot(x, y)
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xlim(min(x), max(x))
        plt.ylim(min(y), max(y) * 1.1)
        self.watch_analyzer.set_date_range(datetime(year, 1, 1), datetime(year, 12, 12), mode=mode)
        plt.title(self.get_chart_title(mode))
        self.watch_analyzer.reset_date_range()
        self.handle_chart(f'days_per_year_{mode}.png')
    
    def get_chart_title(self, mode=None):
        if mode == UPLOAD:
            date_range = self.watch_analyzer.upload_date_range
        else:
            date_range = self.watch_analyzer.date_range
        start = date_range[0].strftime('%d.%m.%Y')
        end = date_range[1].strftime('%d.%m.%Y')
        if mode is None:
            return f'{start} - {end}'
        else:
            if mode == UPLOAD:
                mode = 'Uploaded'
            elif mode == VIEW:
                mode = 'Watched'
            return f' {mode} between {start} - {end}'
