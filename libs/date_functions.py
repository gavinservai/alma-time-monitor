'''Contains general date-related functions'''

import datetime
from dateutil.relativedelta import relativedelta

'''
Description: Convert milliseconds to hours. Useful in converting the users time tracked to hours.
Parameter: A number, in milliseconds
Returns: The hours-conversion of the milliseconds
Usage: Useful when tracking the time a user worked, as the default unit of the data is in milliseconds
'''
def convert_milliseconds_to_hours(ms):
    x = ms / float(1000) / 60 / 60
    return x

'''
Description: Gets the day of the date of the given weekday, that occurred last week. Example: If 3 is entered, the Thursday that occurred last week will be used.
Parameter: The day of the week. 0 = Monday. 1 = Tuesday. etc.
Usage: A week is defined as being from Monday to Sunday. Useful in the generation of the last-week time period for reporting
'''
def get_day_previous_week(day=0):
    now_datetime = datetime.datetime.now()
    weekday_num = now_datetime.weekday()
    weekday_num_difference = -abs(weekday_num)
    last_weekday_datetime = now_datetime + relativedelta(days=weekday_num_difference, weeks=-1, weekday=day)
    return last_weekday_datetime

'''
Description: Converts integer day of the month to ordinal day. Example: 5 becomes 5th
Parameter: An integer, representing the current day of the month.
Usage: Useful when generating the e-mail template - for aesthetic purposes.
'''
def ordinal(n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")