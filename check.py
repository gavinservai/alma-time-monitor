import sys
import logging

from toggle_client_api.api_client import TogglClientApi
from libs.invoke_workdays.workday import WorkDay
from libs.invoke_users.invoke_users import User
from libs.invoke_loadup.invoke_loadup import Loadup
from libs.date_functions import get_day_previous_week, convert_milliseconds_to_hours

# log_level = logging.DEBUG
log_level = logging.WARN
logging.basicConfig(level=log_level)

# Load Configs
import yaml

loadup = Loadup(sys.argv)
loadup.initialize_configs()
configs = loadup.get_config()
logging.debug(configs)
loadup.date_restriction(configs)

# Toggl API Config
settings = {
    'token': configs['togglAPI']['token'],
    'user_agent': configs['togglAPI']['user_agent'],
    "workspace_id": configs['togglAPI']['workspace_id']
}
api = TogglClientApi(settings)

user_list_response = api.get_workspace_members(settings['workspace_id'])
last_monday = get_day_previous_week()
last_sunday = get_day_previous_week(6)

logging.debug(last_monday)
logging.debug(last_sunday)

start_date = last_monday.strftime('%Y-%m-%d')
end_date = last_sunday.strftime('%Y-%m-%d')

logging.debug(start_date)
logging.debug(end_date)

# Minimum Hours Calculation
holidays_yml_stream = WorkDay.get_holidays_stream()
holidays = yaml.load(holidays_yml_stream)
now = WorkDay.get_now()
workDays = WorkDay(holidays, configs['work_days'], now)
minimum_hours_for_week = workDays.calculate_total_work_hours(7.5, last_monday, last_sunday)

users = user_list_response.json()
users_to_contact = []
users_queried = []


print "\n\nTime Tracked for " + start_date + " until " + end_date
print "Minimum Hours Required: " + str(minimum_hours_for_week) + "\n"

users_to_contact = []
users_to_output = []
for user in users:

    time_tracked = api.get_user_hours_range(
            settings['user_agent'],
            settings['workspace_id'],
            user['uid'],
            start_date,
            end_date
    )

    user = User(user, minimum_hours_for_week, convert_milliseconds_to_hours(time_tracked))

    if user.skip_check(configs):
        continue

    user.prepare_user(start_date, end_date)

    hours_reduction = 0
    if user.is_new(last_monday):
        hours_reduction = user.hour_reduction(workDays, 7.5, last_monday, last_sunday)
        user.new_flag = True
    else:
        user.new_flag = False

    user.setup_missing_hours(minimum_hours_for_week, users_to_contact, hours_reduction)
    users_to_output.append(user)

users_to_output.sort(key=lambda x: x.percent_worked, reverse=False)
for user in users_to_output:
    print "{:20}".format(user.mark_notice+user.get_name()) + "{:15.2f}".format(user.hours) + "{:15.2f}".format(user.percent_worked) + '%'
    user_found = (user.get_name(), user.hours, str.format("{:0.2f}", user.hours), str.format("{:0.2f}", user.percent_worked), str.format("{:0.2f}", user.missing_hours), user.get_toggl_url())
    users_queried.append(user_found)

from smtplib import SMTP_SSL as SMTP
mandrill_credentials = {
    'host': configs['smtp']['host'],
    'port': configs['smtp']['port'],
    'username': configs['smtp']['username'],
    'password': configs['smtp']['password'],
}

email_conn = SMTP(mandrill_credentials['host'])
email_conn.set_debuglevel(False)
email_conn.login(mandrill_credentials['username'], mandrill_credentials['password'])

from libs.hours_alerts import HoursAlert
hoursAlert = HoursAlert("views", email_conn, configs)

users_sorted = sorted(users_queried, key=lambda tup: tup[1])
hoursAlert.send_hours_summary(last_monday, last_sunday, users_sorted, minimum_hours_for_week, configs['sendmail']['to_send'])

for user_data in users_to_contact:
    user, hours, percent_worked = user_data
    hoursAlert.send_hours_not_met(last_monday, last_sunday, user, hours, minimum_hours_for_week, configs['sendmail']['to_send'])
