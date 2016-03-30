#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
<pre>	Su Mo Tu We Th Fr Sa
Feb	                   1
	 2  3  <font color="red"><b>4</b></font>  5  6  7  8	first class
	 9 10 11 12 13 <font color="red"><b>14</b></font> 15	assignment 1 due
	16 17 18 19 20 <font color="red"><b>21</b></font> 22	assignment 2 due
	23 24 25 26 27 <font color="red"><b>28</b></font>	assignment 3 due
Mar	                   1
	 2  3  4  5  6  <font color="red"><b>7</b></font>  8	assignment 4 due
	 9 10 11 12 13 <font color="red"><b>14</b></font> 15	design doc due
	<font color="green"><b>16 17 18 19 20 21 22</b></font>	spring break
	23 24 <font color="red"><b>25</b></font> 26 27 28 29	assignment 5 due; weekly TA meetings start this week
	30 31
Apr	       1  2  3  4  5
	 6  7  8  9 10 <font color="red"><b>11</b></font> 12	project prototype
	13 14 15 16 17 18 19
	20 21 22 23 24 <font color="red"><b>25</b></font> 26	alpha test
	27 28 29 30
May	             <font color="red"><b>1  2</b></font>  3	last class; beta test
	 4  5  <font color="red"><b>6  7  8  9</b></font> 10	demo days
	11 12 <font color="red"><b>13</b></font> 14 15 16 17	Dean's date: projects due by 5pm
	18 19 20 21 22 23 24
	25 26 27 28 29 30 31
</pre>
"""

# 3-step pipeline program
# generate | attach events | display

import datetime
from calendar import monthrange
from collections import defaultdict
import codecs, os
import pprint
# try:
#     from html import escape  # py3
# except ImportError:
#     from cgi import escape  # py2
        
# font-family: monospace;
START = 0
END = 1
SUNDAY_INDEX = 6
DAY_HEADERS = ["Su", "Mo" ,"Tu", "We", "Th", "Fr", "Sa"]
MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", \
        "Aug", "Sep", "Oct", "Nov", "Dec"]

HEADERS = {}

class Day:
    def __init__(self, day):
        self.day = day
        self.events = []

    def __str__(self):
        return str(self.day)
        
    def __repr__(self):
        return self.__str__()

class Week:
    def __init__(self, days):
        self.days = days
        self.events = []
    
    def __str__(self):
        return str(self.days)
    
    def __repr__(self):
        return self.__str__()

def write_into_html_file(filename, calendar_str):
    """
    ### Encode & Decode of HTML

    ### HTML Escape

    try:
        from html import escape  # py3
    except ImportError:
        from cgi import escape  # py2

    print(escape("<"))

    ### HTML Unescape

    try:
        from html.parser import HTMLParser  # py3
    except ImportError:
        from HTMLParser import HTMLParser  # py2

    unescape = HTMLParser().unescape

    print(unescape("&gt;"))
    """

    print "write into html file."
    
    with codecs.open(filename, "wb", "utf-8") as writer:
        
        writer.write("<html>\n")
        writer.write("<body>\n")
        writer.write('<head><meta charset="UTF-8"></head>\n')
        writer.write(calendar_str)
        writer.write("</body>\n")
        writer.write("</html>\n")
        

def read_events(filename):
    global HEADERS
    events = []
    
    with codecs.open(filename, "rb", "utf-8") as reader:
        # ignore head line
        line = reader.readline().strip()
        items = line.split(",")
        
        for i in range(len(items)):
            HEADERS[items[i].upper()] = i
        
        # print HEADERS
        
        for line in reader.readlines():
            items = line.strip().split(",")
            
            color = items[HEADERS['COLOR']]
            start_day = items[HEADERS['START_DAY']]
            end_day = items[HEADERS['END_DAY']]
            note = items[HEADERS['NOTE']]
            
            # add the event to the event list
            events.append([color, start_day, end_day, note])
    
    return events

def generate(year, mth):
    """
    Generate the month calendar. 
    """
    first_day_in_week, num_of_days = monthrange(year, mth)
    
    # when the first is not Sunday, ...
    month_calendar = []
    first_padding_days = [Day(0) for i in range((first_day_in_week+1) % len(DAY_HEADERS))]
    first_week = Week(first_padding_days)
    month_calendar.append(first_week)
    
    for i in range(num_of_days):
        day_in_a_week = datetime.date(year, mth, i+1).weekday()
        
        if day_in_a_week == SUNDAY_INDEX and i != 0:
            # create new week
            month_calendar.append(Week([Day(i+1)]))
        else:
            month_calendar[-1].days.append(Day(i+1))
    
    # complement the remaining empty spaces
    for i in range(len(DAY_HEADERS) - len(month_calendar[-1].days)):
        month_calendar[-1].days.append(Day(0))
    
    return month_calendar

def attach(month_calendars, events, year):
    """
    Link the events to days and weeks
    
    Mo  Tu  We  Th  Fr  Sa  Su
    0   1   2   3   4   5   6 
    
    """
    for i in range(len(events)):
        event = events[i]
        
        items = event[HEADERS['START_DAY']].split('-')
        
        d_num, m_num, y_num = map(int, items)
        
        if y_num != year:
            continue
        
        # first day of the month is which day in the week, 0 is Monday 
        # and 6 is Sunday. 
        first_day_in_week, num_of_days = monthrange(y_num, m_num)
        
        month_cal = month_calendars[m_num-1]
        
        pprint.pprint(month_cal)
        
        # find out the week
        
        """
        [[0, 0, 0, 1, 2, 3, 4],
         [5, 6, 7, 8, 9, 10, 11],
         [12, 13, 14, 15, 16, 17, 18],
         [19, 20, 21, 22, 23, 24, 25],
         [26, 27, 28, 29, 30, 0, 0]]
        
        first_day_in_week = 2
        prefix_days = (2+1)%7 = 3
        
        [[1, 2, 3, 4, 5, 6, 7],
         [8, 9, 10, 11, 12, 13, 14],
         [15, 16, 17, 18, 19, 20, 21],
         [22, 23, 24, 25, 26, 27, 28],
         [29, 30, 31, 0, 0, 0, 0]]
        
        first_day_in_week = 6
        prefix_days = (6+1)%7 = 0
        
        """
        prefix_days = (first_day_in_week + 1) % len(DAY_HEADERS)
        week_ind = (prefix_days + d_num) / len(DAY_HEADERS)
        
        print d_num, m_num, y_num
        print first_day_in_week, "week_ind:", week_ind
        
        event_week = month_cal[week_ind]
        # 0 means Sunday
        day_ind_in_week = (datetime.date(y_num, m_num, d_num).weekday() + 1) % 7
        event_day = event_week.days[day_ind_in_week]
        
        event_week.events.append(i)
        event_day.events.append(i)


def display_month(mth, mth_calendar, events):
    """
    Generate a string that displays a month's calendar. 
    """
    output = u""
    
    for i in range(len(mth_calendar)):
        week = mth_calendar[i]
        note_for_week = ""
        
        if len(week.events) > 0:
            events_for_week = [events[e] for e in week.events]
            
            note_for_week = "\t" \
                + "; ".join([ e[HEADERS['NOTE']] for e in events_for_week ])
        
        # only the first week add "month" row header
        if i == 0:  output += MONTH[mth-1]
        
        output += '\t'
        for d in week.days:
            if len(d.events) > 0:
                # assume there is only one event for this day
                event = events[d.events[0]]
                event_color = event[HEADERS['COLOR']]
                
                output += '<font color="%s"><b>' % event_color
                output += "%3s" % str(d.day if d.day != 0 else "")
                output += '</b></font>'
                
            else:
                output += "%3s" % str(d.day if d.day != 0 else "")
        
        output += note_for_week
        output += "\n"
    
    return output

def main():
    import sys, getopt
    
    (opts, args) = getopt.getopt(sys.argv[1:],"s:e:y:f:h")
    
    filename = "calendar.html"
    start_month = 1
    end_month = 12
    y = 2016
    
    for o,a in opts:
        if o == "-s":
            start_month = int(a)
        if o == "-e":
            end_month = int(a)
        if o == "-y":
            y = int(a)
        if o == "-f":
            filename = a
        if o == "-h":
            print "Usage: python textcalendar.py [-s <start_month>] [-e <end_month>] [-y <year>] [-f <filename>] [-h]\n"
            exit()
    
    calendar_str = u""
    blockquote = ["<blockquote>","</blockquote>"]
    pre = ["<pre>","</pre>"]
    
    col_headers = "\n\t" + "".join(["%3s" % d for d in DAY_HEADERS]) + "\n"
    
    
    # # read the events
    events = read_events('events.txt')
    
    # step 1: generate
    month_calendars = []
    for m in range(len(MONTH)):
        month_calendars.append(generate(y, m+1))
    
    # print month_calendars
    
    # step 2: attach
    attach(month_calendars, events, y)
    
    calendar_str += blockquote[START]
    calendar_str += pre[START]
    calendar_str += col_headers
    
    # step 3: display
    for m in range(start_month-1, end_month):
        month_calendar = month_calendars[m]
        calendar_str += display_month(m+1, month_calendar, events)
    calendar_str += pre[END]
    calendar_str += blockquote[END]
    
    
    write_into_html_file(filename, calendar_str)
    # print calendar_str

if __name__ == '__main__':
    main()