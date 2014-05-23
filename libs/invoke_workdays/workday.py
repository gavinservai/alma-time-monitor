from pytz import timezone
from datetime import datetime
from datetime import timedelta
import os
import urllib2

'''
Description: Handles all the logic pertaining to working days and holidays
Usage: Used to primarily calculate the minimum expected hours that all employees should have tracked
'''
class WorkDay:
    now = None
    holidays = None
    work_days = None

    '''
    Parameters:
        Example work_days:
            [1, 2, 3, 4, 5]
        Example holidays:
            {
                2014:
                    [
                        {
                            'date': datetime.date(2014, 1, 1),
                            'percent_used: 0.5
                        },
                        {
                            'date': datetime.date(2014, 2, 10)
                        }
                    ]
            }

    '''
    def __init__(self, holidays, work_days, datetime_now):
        self.__class__.now = datetime_now
        self.__class__.holidays = holidays
        self.__class__.work_days = work_days

    '''
    Description: Checks if today is a workday
    Return: True if today is a workday
    '''
    def is_today_workday(self):
        now = self.__class__.now
        return WorkDay.is_workday(now, self.__class__.holidays, self.__class__.work_days)

    '''
    Description: Calculates the minimum expected hours that employees should have worked, given the date range
    Parameters: working_hours (the amount of hours expected in a full work day)
        start_date [YYYY-MM-DD], end_date [YYYY-MM-DD] (The date range within which to calculate the hours)
    Return: A float representing the minimum expected hours that all employees should have worked
    '''
    def calculate_total_work_hours(self, working_hours, start_date, end_date):
        minimum_hours = 0
        for single_date in self.daterange(start_date, end_date):

            if self.is_weekday(single_date, self.work_days) is True:
                holiday_utilization = self.holiday_utilization(single_date, self.holidays)
                if holiday_utilization is False:
                    minimum_hours = minimum_hours + working_hours
                else:
                    minimum_hours = minimum_hours + (working_hours * (1 - holiday_utilization))


        return minimum_hours

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    @staticmethod
    def get_now(timezone_id='America/Vancouver'):
        now = datetime.now(timezone(timezone_id))
        return now

    @staticmethod
    def is_weekday(datetime_tocheck, work_days):
        today_day = int(datetime_tocheck.strftime('%w'))

        is_weekday_flag = today_day in work_days
        return is_weekday_flag

    '''
    Description: Checks if the given date is a holiday. Then checks what percent of the holiday is in effect (1 = 100% = Full day off) (.8 = 80% = 80% of the day off)
    Parameters: datetime_tocheck, holidays (the date to check, and the holidays to check it against)
    Return: If not a holiday: False. Otherwise, a float from 0 to 1, representing the percent of holiday utilization
    '''
    @staticmethod
    def holiday_utilization(datetime_tocheck, holidays):
        date_tocheck = datetime_tocheck.date()
        try:
            holidays_this_year = holidays[int(datetime_tocheck.strftime('%Y'))]
        except KeyError:
            holidays_this_year = {}

        holiday = next((item for item in holidays_this_year if item["date"] == date_tocheck), None)

        if holiday is None:
            holiday_percent_used = False
        else:
            try:
                holiday_percent_used = holiday["percent_used"]
            except KeyError:
                holiday_percent_used = 1

        return holiday_percent_used

    @staticmethod
    def is_holiday(datetime_tocheck, holidays):
        date_tocheck = datetime_tocheck.date()
        holidays_this_year = holidays[int(datetime_tocheck.strftime('%Y'))]
        holiday = next((item for item in holidays_this_year if item["date"] == date_tocheck), None)

        if holiday is None:
            return False
        else:
            return True


    @staticmethod
    def is_workday(datetime_tocheck, holidays, work_days):
        is_weekday_flag = WorkDay.is_weekday(datetime_tocheck, work_days)
        is_holiday_flag = WorkDay.is_holiday(datetime_tocheck, holidays)

        return is_weekday_flag and (is_holiday_flag is not True)

    '''
    Description: Returns the YAML stream for holidays. If HOLIDAY_CONFIG_PATH environment variable is a valid url, the stream will be loaded from the url. Else, it will be loaded from the file system
    '''
    @staticmethod
    def get_holidays_stream():
        holidays_location = os.environ['HOLIDAY_CONFIG_PATH']

        try:
            holidays_yml_stream = urllib2.urlopen(holidays_location)
        except ValueError:
            try:
                holidays_yml_stream = open(holidays_location, 'r')
            except IOError:
                print "Please configure HOLIDAY_CONFIG_PATH. System terminating."
                quit()

        return holidays_yml_stream
