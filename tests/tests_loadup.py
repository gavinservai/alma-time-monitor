import unittest
import os
import yaml

from libs.invoke_loadup.invoke_loadup import Loadup
from pprint import pprint

class LoadupTests(unittest.TestCase):

    def tearDown(self):
        os.environ.clear()

    '''
    Scenario 9.0
    (load_configs) If no flag is passed in, and CONFIG_PATH is set to a file that exists, those options from CONFIG_PATH should be loaded in
    '''
    def test_load_configs_no_flag_valid_config_path(self):

        os.environ['CONFIG_PATH'] = 'tests/test_config.yml'
        argsv = []

        loadup = Loadup(argsv)
        configs_yml_stream = loadup.load_configs(argsv)
        result = yaml.load(configs_yml_stream)

        self.assertEqual('a', result['smtp']['host'])

    '''
    Scenario 9.1
    (load_configs) If no flag is passed in, and CONFIG_PATH is set to something invalid, False should be returned
    '''
    def test_load_configs_no_flag_invalid_config_path(self):

        os.environ['CONFIG_PATH'] = "This is an invalid path"
        argsv = []

        loadup = Loadup(argsv)
        configs_yml_stream = loadup.load_configs(argsv)

        self.assertEqual(False, configs_yml_stream)

    '''
    Scenario 9.2
    (load_configs) If a valid flag is passed in, and no CONFIG_PATH is set, the configurations should be loaded form the path in the flag
    '''
    def test_load_configs_valid_flag_no_config_path(self):

        os.environ['CONFIG_PATH'] = ""

        argsv = []
        argsv.append("name")
        argsv.append("tests/test_config.yml")

        loadup = Loadup(argsv)
        configs_yml_stream = loadup.load_configs(argsv)
        result = yaml.load(configs_yml_stream)

        self.assertEqual('a', result['smtp']['host'])

    '''
    Scenario 9.3
    (load_configs) If an invalid flag is passed in, False should be returned
    '''
    def test_load_configs_invalid_flag_no_config_path(self):

        os.environ['CONFIG_PATH'] = ""

        argsv = []
        argsv.append("name")
        argsv.append("tests/thisfiledoesn'texist.yml")

        loadup = Loadup(argsv)
        configs_yml_stream = loadup.load_configs(argsv)

        self.assertEqual(False, configs_yml_stream)

    '''
    Scenario 10.0
    (create_config) If load_configs returns False, it should return configurations from environment variables
    '''
    def test_create_config_false_load_configs(self):

        os.environ['CONFIG_PATH'] = ""
        os.environ['SMTP_HOST'] = 'b'
        os.environ['SMTP_PORT'] = 'b'
        os.environ['SMTP_USERNAME'] = 'b'
        os.environ['SMTP_PASSWORD'] = 'b'

        os.environ['DATE_RESTRICT_FLAG'] = 'b'
        os.environ['DATE_RESTRICT_WEEKDAY'] = 'b'
        os.environ['DATE_RESTRICT_HOUR'] = 'b'

        os.environ['SENDMAIL_FLAG'] = 'b'
        os.environ['TOGGL_TOKEN'] = 'b'
        os.environ['TOGGL_USER_AGENT'] = 'b'
        os.environ['TOGGL_WORKSPACE_ID'] = 'b'


        os.environ['ADMIN_EMAIL_1'] = 'b'
        os.environ['ADMIN_EMAIL_2'] = 'b'

        os.environ['STAFF_EMAIL_ROLE_STAFF_RESOURCE'] = 'b'
        os.environ['STAFF_EMAIL_ROLE_GROUP_LEADS'] = 'b'
        os.environ['STAFF_FROM_EMAIL'] = 'b'

        argsv = []
        argsv.append("name")

        loadup = Loadup(argsv)
        configs = loadup.create_config(argsv)

        self.assertEqual('b', configs['smtp']['host'])

    '''
    Scenario 10.1
    (create_config) If load_configs returns something, the configurations should be loaded from that stream
    '''
    def test_create_config_resource_load_configs(self):

        os.environ['CONFIG_PATH'] = ""
        os.environ['SMTP_HOST'] = 'b'
        os.environ['SMTP_PORT'] = 'b'
        os.environ['SMTP_USERNAME'] = 'b'
        os.environ['SMTP_PASSWORD'] = 'b'

        os.environ['DATE_RESTRICT_FLAG'] = 'b'
        os.environ['DATE_RESTRICT_WEEKDAY'] = 'b'
        os.environ['DATE_RESTRICT_HOUR'] = 'b'

        os.environ['SENDMAIL_FLAG'] = 'b'
        os.environ['TOGGL_TOKEN'] = 'b'
        os.environ['TOGGL_USER_AGENT'] = 'b'
        os.environ['TOGGL_WORKSPACE_ID'] = 'b'


        os.environ['ADMIN_EMAIL_1'] = 'b'
        os.environ['ADMIN_EMAIL_2'] = 'b'

        os.environ['STAFF_EMAIL_ROLE_STAFF_RESOURCE'] = 'b'
        os.environ['STAFF_EMAIL_ROLE_GROUP_LEADS'] = 'b'
        os.environ['STAFF_FROM_EMAIL'] = 'b'

        argsv = []
        argsv.append("name")
        argsv.append("tests/test_config.yml")

        loadup = Loadup(argsv)
        configs = loadup.create_config(argsv)

        self.assertEqual('a', configs['smtp']['host'])


    '''
    Scenario 11.0
    (generate_config_from_environment) If environment variables are properly set, returns configurations from the environment variables
    '''
    def test_generate_config_from_environment_valid_env(self):

        os.environ['CONFIG_PATH'] = ""
        os.environ['SMTP_HOST'] = 'b'
        os.environ['SMTP_PORT'] = 'b'
        os.environ['SMTP_USERNAME'] = 'b'
        os.environ['SMTP_PASSWORD'] = 'b'

        os.environ['DATE_RESTRICT_FLAG'] = 'b'
        os.environ['DATE_RESTRICT_WEEKDAY'] = 'b'
        os.environ['DATE_RESTRICT_HOUR'] = 'b'

        os.environ['SENDMAIL_FLAG'] = 'b'
        os.environ['TOGGL_TOKEN'] = 'b'
        os.environ['TOGGL_USER_AGENT'] = 'b'
        os.environ['TOGGL_WORKSPACE_ID'] = 'b'


        os.environ['ADMIN_EMAIL_1'] = 'b'
        os.environ['ADMIN_EMAIL_2'] = 'b'

        os.environ['STAFF_EMAIL_ROLE_STAFF_RESOURCE'] = 'b'
        os.environ['STAFF_EMAIL_ROLE_GROUP_LEADS'] = 'b'
        os.environ['STAFF_FROM_EMAIL'] = 'b'

        argsv = []
        argsv.append("name")
        argsv.append("tests/test_config.yml")

        loadup = Loadup(argsv)
        configs = loadup.generate_config_from_environment()

        self.assertEqual('b', configs['smtp']['host'])

    '''
    Scenario 11.1
    (generate_config_from_environment) If environment variables are not properly set, should terminate (SystemExit)
    '''
    def test_generate_config_from_environment_invalid_env(self):
        os.environ['CONFIG_PATH'] = ""
        os.environ['SMTP_HOST'] = 'b'
        os.environ['SMTP_PORT'] = 'b'
        os.environ['SMTP_USERNAME'] = 'b'
        os.environ['SMTP_PASSWORD'] = 'b'

        os.environ['DATE_RESTRICT_FLAG'] = 'b'
        os.environ['DATE_RESTRICT_WEEKDAY'] = 'b'
        os.environ['DATE_RESTRICT_HOUR'] = 'b'

        os.environ['SENDMAIL_FLAG'] = 'b'
        os.environ['TOGGL_USER_AGENT'] = 'b'
        os.environ['TOGGL_WORKSPACE_ID'] = 'b'


        os.environ['ADMIN_EMAIL_1'] = 'b'
        os.environ['ADMIN_EMAIL_2'] = 'b'

        os.environ['STAFF_EMAIL_ROLE_STAFF_RESOURCE'] = 'b'
        os.environ['STAFF_EMAIL_ROLE_GROUP_LEADS'] = 'b'
        os.environ['STAFF_FROM_EMAIL'] = 'b'

        argsv = []
        argsv.append("name")
        argsv.append("tests/test_config.yml")

        loadup = Loadup(argsv)
        system_exit = False
        try:
            configs = loadup.generate_config_from_environment()
        except SystemExit:
            system_exit = True

        self.assertTrue(system_exit)
