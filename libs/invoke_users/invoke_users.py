from datetime import datetime
'''
Description: A User object contains the information for a user which will be used to send emails
Usage: When iterating through the information of all users, these User objects are generated in order to abstract
the user-related logic and data that is pertinent to e-mailing.
'''
class User:

    '''
    Description: Initializes the default values for the user
    Parameters: user, min_hours (minimum hours required to work for the week), hours (hours that the user tracked)
    '''
    def __init__(self, user, min_hours, hours):
        self.user = user
        self.missing_hours = 0
        self.mark_notice = ''
        self.hours = hours
        self.percent_worked = self.hours / min_hours * 100
        self.joined_date = datetime.strptime(self.user['at'], '%Y-%m-%dT%H:%M:%S+00:00')
        self.min_hours = min_hours

    '''
    Description: If the user has not reported enough hours, they are added to the mailing list
    Parameters: minimum_hours_for_week, users_to_contact (reference to a list of users who are on the mailing list)
        hours_reduction (the hours that may be subtracted from the minimum weekly hours for this user)
    Usage: When iterating through all users, this method can be called on each user to populate a list containing all users
    who are missing hours. The hours they would need to meet the minimum threshold is also stored.
    '''
    def setup_missing_hours(self, minimum_hours_for_week, users_to_contact, hours_reduction):
        if self.is_not_enough_hours():
            if self.new_flag is True:
                try:
                    self.percent_worked = self.hours / (self.min_hours - hours_reduction) * 100
                except ZeroDivisionError:
                    self.percent_worked = 100
                self.mark_notice = "[NEW] "
            self.missing_hours = minimum_hours_for_week - self.hours - hours_reduction

            if not self.missing_hours <= 0:
                self.mark_notice = '*'
                users_to_contact.append((self.user, self.hours, self.percent_worked))

    '''
    Description: Checks to see if the user is inactive, or an admin. If so, they should be excluded from the e-mail reports.
    Return: True if the user is an admin or is inactive. False otherwise.
    Usage: When iterating through all users, this method can be used to ignore the current user. If the user is inactive or
    an admin, there would be no reason to add them to the mailing list.
    '''
    def skip_check(self, configs):
        if self.is_inactive() or self.is_admin(configs):
            return True
        else:
            return False
    '''
    Description: Prepares the users toggl url. Handles the situation where there is no name for the user, by setting it to the email
    Parameters: start_date [YYYY-MM-DD], end_date [YYYY-MM-DD] (range of the report period)
    Usage: When iterating through all users, this method can be called one ach user to generate the url to the users toggl report.
    It also takes care of users without a name, by setting it to their email.
    '''
    def prepare_user(self, start_date, end_date):
        self.set_toggl_url(start_date, end_date)
        self.email_to_name()

    '''
    Description: Computes the hours, for the user, that need to be subtracted from the total minimum hours
    Parameters: work_day [WorkDay], working_hours (hours required to work in a full day), start_date [datetime], end_date [datetime]
    Return: Returns the hours that the user may subtract from the minimum required hours of the week
    Usage: Useful when a new employee joined during the reporting period.
        Example: If the reporting period is last Monday to Sunday, and an employee joined in Wednesday, this computes the hours that
        they did not need to work on Monday and Tuesday
    '''
    def hour_reduction(self, work_day, working_hours, start_date, end_date):
        if self.joined_date > end_date:
            effective_end_date = end_date
        else:
            effective_end_date = self.joined_date

        return work_day.calculate_total_work_hours(working_hours, start_date, effective_end_date)

    '''
    Description: Checks if the user is new. A user is new if they joined within the last two weeks
    Parameters: start_date [datetime] (The start_date of the reporting period - usually last Monday)
    Return: True if the user is new, False otherwise
    '''
    def is_new(self, start_date):
        if self.joined_date > start_date and self.joined_date.day > start_date.day:
            return True
        else:
            return False

    '''
    Description: Checks if the user is inactive
    Return: True if the user is inactive, False Otherwise
    '''
    def is_inactive(self):
        if self.user['inactive'] == True:
            return True
        else:
            return False
    '''
    Description: Checks if the user is an administrator
    Return: True if the user is an admin, False otherwise
    '''
    def is_admin(self, configs):
        admins = configs['admin']
        admin = next((item for item in admins if item == self.user['email']), None)

        if admin is None:
            return False
        else:
            return True

    '''
    Description: Creates the URL of the Toggl report pertaining to the user
    Parameter: start_date [YYYY-MM-DD], end_date [YYYY-MM-DD] (The date range that the report should cover)
    '''
    def set_toggl_url(self, start_date, end_date):
        self.user['togglURL'] = "https://www.toggl.com/app/#reports/summary/" + str(self.user['wid']) + "/from/" + start_date + "/to/" + end_date + "/users/" + str(self.user['uid']) + "/billable/both"

    '''
    Description: If the user has no name, the name is set to the email
    '''
    def email_to_name(self):
        try:
            if not self.user['name']:
                self.user['name'] = self.user['email']
        except KeyError:
            self.user['name'] = self.user['email']
    '''
    Description: Checks if the user has not worked enough hours
    Return: True if the user has not worked enough hours last week
    '''
    def is_not_enough_hours(self):
        return self.percent_worked < 100

    '''
    Return: The users id
    '''
    def get_id(self):
        return self.user['uid']

    '''
    Return: The users name
    '''
    def get_name(self):
        return self.user['name']

    '''
    Return: The url to the toggl report of the user
    '''
    def get_toggl_url(self):
        return self.user['togglURL']

    '''
    Return: The users email
    '''
    def get_email(self):
        return self.user['email']

