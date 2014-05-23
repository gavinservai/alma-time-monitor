import datetime
import os
import yaml
import json

'''
Description: Sets the configuration for the system based on the command line arguments passed in
Usage: Used at the beginning, when the script is run, in order to define the expected system behaviour
If no CONFIG_PATH is set, ENVIRONMENT variables are utilized. The supported ENVIRONMENT variables are:
SMTP_HOST: smtp host
SMTP_PORT: the smtp port
SMTP_USERNAME: username for smtp
SMTP_PASSWORD: password for smtp

DATE_RESTRICT_FLAG: True to restrict datetime that script can be run. False to allow manual execution
DATE_RESTRICT_WEEKDAY: The weekday to restrict script execution to. 0 = Monday
DATE_RESTRICT_HOUR: The hour to restrict script execution to.

SENDMAIL_FLAG: True to have the system send out mail. False to disable sending of mail.

TOGGL_TOKEN: toggl api token
TOGGL_USER_AGENT: toggl api user agent
TOGGL_WORKSPACE_ID: toggl workspace id

ADMIN_EMAIL_1: an email of admin - emails wont be sent to the admin
ADMIN_EMAIL_2: another email of another admin - emails wont be sent to this admin

STAFF_EMAIL_ROLE_STAFF_RESOURCE: email of the staff resource
STAFF_EMAIL_ROLE_GROUP_LEADS: email of the group leads
STAFF_FROM_EMAIL: email address from which emails will be sent
'''
class Loadup:
    '''
    Parameters: command_args (The command-line arguments (sys.argv)
    '''
    def __init__(self, command_args):
        self.arguments = command_args

    '''
    Description: Initialized the configuration options. Either loaded from YAML, or loaded from ENVIRONMENT
    '''
    def initialize_configs(self):
        self.configs = self.create_config(self.arguments)

    '''
    Return: Dict containing all of the configurations
    '''
    def create_config(self, arguments):
        configs_yml_stream = self.load_configs(arguments)

        if configs_yml_stream is False:
            configs = self.generate_config_from_environment()
        else:
            configs = yaml.load(configs_yml_stream)

        return configs


    '''
    Description: Loads the appropriate configuration, either for production or development mode
    Parameter: arguments (The command-line arguments (sys.argv))
    Return: Yaml stream, if CONFIG_PATH points to a valid yaml stream. Otherwise, returns False
    '''
    def load_configs(self, arguments):
        configs_path = self.get_config_path(arguments)
        if configs_path is False:
            try:
                configs_path = os.environ['CONFIG_PATH']
            except KeyError:
                print "No CONFIG_PATH specified. Loading Environment Values."
                return False

        try:
            configs_yml_stream = open(configs_path, 'r')
        except IOError:
            print "CONFIG_PATH invalid. Loading Environment Values"
            return False

        return configs_yml_stream

    '''
    Description: Halts the script if it is run outside of the desired time period
    Parameter: configs (contains the configurations loaded up by load_configs)
        Example configs:
            {
                "date_restrict" : {
                    "to_restrict" : True,
                    "hour" : 20,
                    "weekday" : 3
                },
                "smtp" : {
                    "host" : "[insert smtp host here]",
                    "password" : "[insert password here]",
                    "port" : "[insert port here]",
                    "username" : "[insert username here]"
                },
                "work_days" : [
                    1,
                    2,
                    3,
                    4,
                    5
                ]
            }
    Return: True if the datetime which the script was invoked is in an allowable range. Terminates the script otherwise.
    '''
    def date_restriction(self, configs):
        if configs['date_restrict']['to_restrict'] is True:
            if datetime.datetime.now().weekday() != configs['date_restrict']['weekday']:
                quit()
            if datetime.datetime.now().hour != configs['date_restrict']['hour']:
                quit()
        return True

    '''
    Return: Returns the config_yml_stream
    '''
    def get_yml_stream(self):
        return self.config_yml_stream

    '''
    Return: Returns the config dict
    '''
    def get_config(self):
        return self.configs

    '''
    Return: If a config path has been passed in via command line, the path is returned. Otherwise, False is returned
    '''
    def get_config_path(self, arguments):
        try:
            config_path = arguments[1]
        except IndexError:
            config_path = False

        return config_path


    '''
    Description: Uses environment variables to generate a config dict
    Return: A dict containing all configuration options
    '''
    def generate_config_from_environment(self):
        configs = {}

        #Default options
        work_days = [1, 2, 3, 4, 5]
        configs['work_days'] = work_days

        configs['smtp'] = self.generate_smtp_configs()
        configs['date_restrict'] = self.generate_date_configs()
        configs['sendmail'] = self.generate_sendmail_configs()
        configs['togglAPI'] = self.generate_toggl_api_configs()
        configs['admin'] = self.generate_admin_configs()
        configs['staff'] = self.generate_staff_configs()

        return configs

    '''
    Return: Date configurations from environment variables
    '''
    def generate_date_configs(self):
        try:
            date_configs = {}
            date_configs['to_restrict'] = os.environ['DATE_RESTRICT_FLAG']
            date_configs['weekday'] = os.environ['DATE_RESTRICT_WEEKDAY']
            date_configs['hour'] = os.environ['DATE_RESTRICT_HOUR']
        except KeyError:
            print "Please ensure that your DATE_RESTRICT environment variables are configured properly. System terminating"
            quit()

        return date_configs

    '''
    Return: SMTP configurations from environment variables
    '''
    def generate_smtp_configs(self):
        try:
            smtp_configs = {}
            smtp_configs['host'] = os.environ['SMTP_HOST']
            smtp_configs['port'] = os.environ['SMTP_PORT']
            smtp_configs['username'] = os.environ['SMTP_USERNAME']
            smtp_configs['password'] = os.environ['SMTP_PASSWORD']
        except KeyError:
            print "Please ensure that your SMTP environment variables are configured properly. System terminating"
            quit()
        return smtp_configs

    '''
    Return: Sendmail configurations from environment variables
    '''
    def generate_sendmail_configs(self):
        try:
            mail_configs = {}
            mail_configs['to_send'] = os.environ['SENDMAIL_FLAG']
        except KeyError:
            print "Please ensure that your SENDMAIL environment variables are configured properly. System terminating"
            quit()
        return mail_configs

    '''
    Return: Toggl API configurations from environment variables
    '''
    def generate_toggl_api_configs(self):
        try:
            api_configs = {}
            api_configs['token'] = os.environ['TOGGL_TOKEN']
            api_configs['user_agent'] = os.environ['TOGGL_USER_AGENT']
            api_configs['workspace_id'] = os.environ['TOGGL_WORKSPACE_ID']
        except KeyError:
            print "Please ensure that your TOGGL environment variables are configured properly. System terminating"
            quit()
        return api_configs

    '''
    Return: Admin configurations from environment variables
    '''
    def generate_admin_configs(self):
        try:
            admin_configs = {}
            admin_configs = json.loads(os.environ['ADMIN_EMAIL'])
        except KeyError:
            print "Please ensure that your ADMIN environment variables are configured properly. System terminating"
            quit()
        return admin_configs

    '''
    Return: Staff configurations from environment variables
    '''
    def generate_staff_configs(self):
        try:
            staff_configs = {}
            staff_configs['email_role_staff_resource'] = os.environ['STAFF_EMAIL_ROLE_STAFF_RESOURCE']
            staff_configs['email_role_group_leads'] = os.environ['STAFF_EMAIL_ROLE_GROUP_LEADS']
            staff_configs['from_email'] = os.environ['STAFF_FROM_EMAIL']
        except KeyError:
            print "Please ensure that your STAFF environment variables are configured properly. System terminating"
            quit()
        return staff_configs