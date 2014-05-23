import jinja2
from jinja2 import Environment
import sys
from email.mime.text import MIMEText
from libs.date_functions import ordinal

'''
Description: Handles e-mailing as well as e-mail preparation. Fires off missing hours emails, as well as a summary email.
Usage: Useful when iterating on users from a mailing list, to send emails to them. Also useful in sending a summary report.
'''
class HoursAlert:

    template_env = None
    email_conn = None

    def __init__(self, views_path, email_conn, configs):
        templateLoader = jinja2.FileSystemLoader(searchpath=views_path)
        self.template_env = Environment(loader=templateLoader)
        self.email_conn = email_conn
        self.email_role_staff_resource = configs['staff']['email_role_staff_resource']
        self.email_role_group_leads = configs['staff']['email_role_group_leads']
        self.from_email = configs['staff']['from_email']

    '''
    Description: Sends out a summary email, containing a summary table of the hours worked by each employee over the previous week
    Parameters: start_date [YYYY-MM-DD], end_date [YYYY-MM-DD] (date range of the previous week, or desired reporting period)
        users_list (list of all employees - used to generate the summary table)
        minimum_hours_for_range (the minimum hours that an employee must work for the given date period specified by start_date and end_date)
    Usage: Used to send out a summary report.
    '''
    def send_hours_summary(self, start_date, end_date, users_list, minimum_hours_for_range, do_send=True):

        if do_send is not True:
            return False

        template = self.template_env.get_template('emails/hours_summary.html')
        template_vars = {
            "users_list": users_list,
            "minimum_hours_for_range": minimum_hours_for_range,
            "start_month": start_date.strftime("%B"),
            "start_dayWeek": start_date.strftime("%A"),
            "start_dayMonth": ordinal(int(start_date.strftime("%d"))),
            "end_month": end_date.strftime("%B"),
            "end_dayWeek": end_date.strftime("%A"),
            "end_dayMonth": ordinal(int(end_date.strftime("%d")))

        }
        body = template.render(template_vars)

        try:
            msg = MIMEText(body, 'html')
            msg['Subject'] = "Team Hours Summary for Week ending " + end_date.strftime('%Y-%m-%d')
            msg['From'] = 'alma@invokelabs.com'
            msg['To'] = self.email_role_staff_resource
            conn = self.email_conn
            try:
                conn.sendmail(msg['From'], msg['To'], msg.as_string())
            finally:
                return True

        except Exception, exc:
            sys.exit("mail failed; %s" % str(exc))  # give a error message

    '''
    Description: Sends an e-mail to an employee who has not met their quota of hours, describing how many they need, and providing a link to the report of their hours
    Parameters: start_date [YYYY-MM-DD], end_date [YYYY-MM-DD] (The range of the report desired (usually last Monday to Sunday))
        user (The employee that will be e-mailed. The employee should not have met their hour quota for the previous week)
        hours_worked (The amount of hours that the employee worked in the date range specified by start_date and end_date
        minimum_hours_for_range (The minimum hours that the employee is required to work for the date range specified by start_date and end_date)
    Usage: Used when iterating through a mailing list of all users who have not tracked enough hours
    '''
    def send_hours_not_met(self, start_date, end_date, user, hours_worked, minimum_hours_for_range, do_send=True):
        if do_send is not True:
            return False

        print "Emailing: " + user['name'] + " at " + user['email'] + " CC: " + self.email_role_staff_resource
        user["firstname"] = (user["name"].split())[0]

        #Used to fix the plural form of hour(s) in the email
        if (minimum_hours_for_range - hours_worked) > 1:
            user["hourflag"] = 1

        template = self.template_env.get_template('emails/hours_alert.html')
        template_vars = {
            "user": user,
            "hours_worked": str.format("{:15.2f}", hours_worked),
            "hours_missing": str.format("{:15.2f}", (minimum_hours_for_range - hours_worked)),
            "minimum_hours_for_range": minimum_hours_for_range,
            "percent_worked": hours_worked / minimum_hours_for_range * 100,
            "start_date": start_date.strftime('%d-%m-%Y'),
            "end_date": end_date.strftime('%d-%m-%Y')
        }
        body = template.render(template_vars)

        try:
            msg = MIMEText(body, 'html')
            msg['Subject'] = "Looks like you didn't log all your hours for the week ending " + end_date.strftime('%Y-%m-%d')
            msg['From'] = self.from_email

            msg['To'] = user['email']
            msg['cc'] = self.email_role_group_leads

            conn = self.email_conn
            try:
                conn.sendmail(msg['From'], [msg['To'], msg['cc']], msg.as_string())
            finally:
                return True

        except Exception, exc:
            sys.exit("mail failed; %s" % str(exc))  # give a error message
