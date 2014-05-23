import unittest
from libs.invoke_workdays.workday import WorkDay
from libs.invoke_users.invoke_users import User
from libs.date_functions import *


class HolidayTests(unittest.TestCase):

    def setUp(self):
        self.workdays = [1, 2, 3, 4, 5]
        self.hours_per_workday = 7.5
        self.hours_per_week = 37.5
        self.datetime_now = datetime.datetime.now()

    '''
    Scenario 1.0
    If a full holiday occurs on the same day the report is requested, the report required hours should not change.
    '''
    def test_full_holiday_report_day(self):
        holidays = {
                    2014:
                        [
                            {
                                'date': self.datetime_now.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 1.1
    If a partial-holiday occurs on the same day the report is requested, the report required hours should not change.
    '''
    def test_partial_holiday_report_day(self):
        holidays = {
                    2014:
                        [
                            {
                                'date': self.datetime_now.date(),
                                'percent_used': 0.3
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 2.0
    If a full holiday occurs mid-week before the report is requested, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_holiday_mid_last_week(self):

        last_wednesday = get_day_previous_week(2)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_wednesday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 2.1
    If a partial-holiday occurs mid-week before the report is requested, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_holiday_mid_last_week(self):

        last_wednesday = get_day_previous_week(2)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_wednesday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 3.0.0
    If a full holiday occurs on the last working day of the report range, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_holiday_end_last_week(self):

        last_friday = get_day_previous_week(4)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_friday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 3.0.1
    If a partial holiday occurs on the last working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_holiday_end_last_week(self):


        last_friday = get_day_previous_week(4)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_friday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 3.1.0
    If a full holiday occurs on the first working day of the report range, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_holiday_beginning_last_week(self):

        last_monday = get_day_previous_week(0)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_monday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 3.1.1
    If a partial holiday occurs on the first working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_holiday_beginning_last_week(self):

        last_monday = get_day_previous_week(0)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_monday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 4.0
    If a full holiday occurs on the weekend contained in the report range, the report required hours should not change (weekend is not a working day).
    '''
    def test_full_holiday_weekend(self):

        last_saturday = get_day_previous_week(5)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_saturday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 4.1
    If a partial-holiday occurs on the weekend contained in the report range, the report required hours should not change
    '''
    def test_partial_holiday_weekend(self):

        last_saturday = get_day_previous_week(5)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_saturday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 5.1.0
    If duplicate full holidays occur on the same day the report is requested, the report required hours should not change.
    '''
    def test_full_duplicate_holiday_report_day(self):
        holidays = {
                    2014:
                        [
                            {
                                'date': self.datetime_now.date()
                            },
                            {
                                'date': self.datetime_now.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 5.1.1
    If duplicate partial-holidays occur on the same day the report is requested, the report required hours should not change.
    '''
    def test_partial_duplicate_holiday_report_day(self):
        holidays = {
                    2014:
                        [
                            {
                                'date': self.datetime_now.date(),
                                'percent_used': 0.3
                            },
                            {
                                'date': self.datetime_now.date(),
                                'percent_used': 0.3
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 5.2.0
    If duplicate full holidays occur mid-week before the report is requested, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_duplicate_holiday_mid_last_week(self):

        last_wednesday = get_day_previous_week(2)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_wednesday.date()
                            },
                            {
                                'date': last_wednesday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 5.2.1
    If duplicate partial-holidays occur mid-week before the report is requested, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_duplicate_holiday_mid_last_week(self):

        last_wednesday = get_day_previous_week(2)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_wednesday.date(),
                                'percent_used': 0.8
                            },
                            {
                                'date': last_wednesday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 5.3.0.0
    If duplicate full holidays occur on the last working day of the report range, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_duplicate_holiday_end_last_week(self):

        last_friday = get_day_previous_week(4)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_friday.date()
                            },
                            {
                                'date': last_friday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 5.3.0.1
    If duplicate partial holidays occur on the last working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_duplicate_holiday_end_last_week(self):


        last_friday = get_day_previous_week(4)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_friday.date(),
                                'percent_used': 0.8
                            },
                            {
                                'date': last_friday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 5.3.1.0
    If duplicate full holidays occur on the first working day of the report range, the report required hours should be decreased by the working hours of a full day.
    '''
    def test_full_duplicate_holiday_beginning_last_week(self):

        last_monday = get_day_previous_week(0)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_monday.date()
                            },
                            {
                                'date': last_monday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 5.3.1.1
    If duplicate partial holidays occur on the first working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.
    '''
    def test_partial_duplicate_holiday_beginning_last_week(self):

        last_monday = get_day_previous_week(0)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_monday.date(),
                                'percent_used': 0.8
                            },
                            {
                                'date': last_monday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 5.4.0
    If duplicate full holidays occur on the weekend contained in the report range, the report required hours should not change (weekend is not a working day).
    '''
    def test_full_duplicate_holiday_weekend(self):

        last_saturday = get_day_previous_week(5)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_saturday.date()
                            },
                            {
                                'date': last_saturday.date()
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)



    '''
    Scenario 5.4.1
    If duplicate partial-holidays occur on the weekend contained in the report range, the report required hours should not change
    '''
    def test_partial_duplicate_holiday_weekend(self):

        last_saturday = get_day_previous_week(5)
        holidays = {
                    2014:
                        [
                            {
                                'date': last_saturday.date(),
                                'percent_used': 0.8
                            },
                            {
                                'date': last_saturday.date(),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)

        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 6.0.0
    If checking on the boundary of two different years, a full holiday on a weekday of the reporting period, in the previous year, must still decrease the reports required holiday by a full work day
    '''
    def test_full_holiday_mid_week_prev_year(self):

        holidays = {
                    2014:
                        [
                            {
                                'date': datetime.date(2014, 12, 31)
                            }
                        ]
                    }

        start_date = datetime.datetime(2014, 12, 29)
        end_date = datetime.datetime(2015, 1, 4)

        workday = WorkDay(holidays, self.workdays, datetime.datetime(2015, 1, 5))
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - self.hours_per_workday))

    '''
    Scenario 6.0.1
    If checking on the boundary of two different years, a partial holiday on a weekday of the reporting period, in the previous year, must still decrease the reports required holiday by a partial holiday utilization
    '''
    def test_partial_holiday_mid_week_prev_year(self):

        holidays = {
                    2014:
                        [
                            {
                                'date': datetime.date(2014, 12, 31),
                                'percent_used': 0.8
                            }
                        ]
                    }

        start_date = datetime.datetime(2014, 12, 29)
        end_date = datetime.datetime(2015, 1, 4)

        workday = WorkDay(holidays, self.workdays, datetime.datetime(2015, 1, 5))
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, (self.hours_per_week - (self.hours_per_workday * 0.8)))

    '''
    Scenario 6.1
    If checking on the boundary of two different years, if there is no holiday in the reporting period, the minimum required hours must be the same as if reporting on any other week of the year that contains no holiday
    '''
    def test_no_holiday_prev_year(self):

        holidays = {
                    2014:
                        [
                        ]
                    }

        start_date = datetime.datetime(2014, 12, 29)
        end_date = datetime.datetime(2015, 1, 4)

        workday = WorkDay(holidays, self.workdays, datetime.datetime(2015, 1, 5))
        hours_needed = workday.calculate_total_work_hours(self.hours_per_workday, start_date, end_date)

        self.assertEqual(hours_needed, self.hours_per_week)

    '''
    Scenario 7.0
    If a new employee is added to the system a month before he starts, he/she should not have required hours for the previous week (the week before they start work)
    '''
    def test_employee_added_month_early(self):
        month_ago = datetime.datetime.now() + relativedelta( months = -6 )
        month_ago = month_ago.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        holidays = {
                    2014:
                        [
                        ]
                    }
        user = {
                 'active': True,
                 'admin': True,
                 'at': month_ago,
                 'avatar_file_name': 'randomurl.txt',
                 'email': 'unit.test@invokelabs.com',
                 'id': 321,
                 'inactive': False,
                 'name': 'Unit Test',
                 'togglURL': 'randomurl',
                 'uid': 123,
                 'wid': 456
        }
        dummy_user = User(user, 37.5, 0)
        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)
        hours_reduction = dummy_user.hour_reduction(workday, self.hours_per_workday, start_date, end_date)
        required_hours = self.hours_per_week - hours_reduction

        self.assertEqual(0, required_hours)

    '''
    Scenario 7.1
    If a new employee joins part-way through the reporting week, the days that they did not work must not be included in their minimum hours calculation
    '''
    def test_employee_join_mid_last_week(self):
        last_wednesday = get_day_previous_week(2)
        last_wednesday = last_wednesday.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        holidays = {
                    2014:
                        [
                        ]
                    }
        user = {
                 'active': True,
                 'admin': True,
                 'at': last_wednesday,
                 'avatar_file_name': 'randomurl.txt',
                 'email': 'unit.test@invokelabs.com',
                 'id': 321,
                 'inactive': False,
                 'name': 'Unit Test',
                 'togglURL': 'randomurl',
                 'uid': 123,
                 'wid': 456
        }
        dummy_user = User(user, 37.5, 0)
        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)
        hours_reduction = dummy_user.hour_reduction(workday, self.hours_per_workday, start_date, end_date)
        required_hours = self.hours_per_week - hours_reduction

        self.assertEqual(3 * self.hours_per_workday, required_hours)


    '''
    Scenario 7.2
    If a new employee joins part-way through the reporting week, and works more hours than their minimum required, the percent they worked should exceed 100
    '''
    def test_employee_join_mid_last_week_work_more_hours(self):
        last_wednesday = get_day_previous_week(2)
        last_wednesday = last_wednesday.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        holidays = {
                    2014:
                        [
                        ]
                    }
        user = {
                 'active': True,
                 'admin': True,
                 'at': last_wednesday,
                 'avatar_file_name': 'randomurl.txt',
                 'email': 'unit.test@invokelabs.com',
                 'id': 321,
                 'inactive': False,
                 'name': 'Unit Test',
                 'togglURL': 'randomurl',
                 'uid': 123,
                 'wid': 456
        }
        users_to_contact = []
        dummy_user = User(user, 37.5, 0)
        dummy_user.new_flag = True
        workday = WorkDay(holidays, self.workdays, self.datetime_now)
        start_date = get_day_previous_week()
        end_date = get_day_previous_week(6)
        hours_reduction = dummy_user.hour_reduction(workday, self.hours_per_workday, start_date, end_date)
        dummy_user.setup_missing_hours((3 * self.hours_per_workday), users_to_contact, hours_reduction)


        self.assertGreater(100, dummy_user.percent_worked)

    '''
    Scenario 8.0
    If the user has not worked the minimum required hours, the correct difference between hours worked and hours required must be computed
    '''
    def test_correct_hours_difference(self):
        last_wednesday = get_day_previous_week(2)
        last_wednesday = last_wednesday.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        holidays = {
                    2014:
                        [
                        ]
                    }
        user = {
                 'active': True,
                 'admin': True,
                 'at': last_wednesday,
                 'avatar_file_name': 'randomurl.txt',
                 'email': 'unit.test@invokelabs.com',
                 'id': 321,
                 'inactive': False,
                 'name': 'Unit Test',
                 'togglURL': 'randomurl',
                 'uid': 123,
                 'wid': 456
        }

        users_to_contact = []
        dummy_user = User(user, self.hours_per_week, 36.5)
        dummy_user.new_flag = True
        dummy_user.setup_missing_hours(self.hours_per_week, users_to_contact, 0)

        self.assertEqual(1.0, dummy_user.missing_hours)
