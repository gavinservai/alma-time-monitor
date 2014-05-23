
# To Run
`python check.py`
# To Run without datetime restriction
Change the date restrict to_restrict to False, in your configurations

# DEPLOYMENT
0. (optional) Ensure that Procfile is created, with the contents as follows:
```
worker: python check.py
```
This Procfile contains the desired command that Heroku will run when starting a dyno. Refer to step 4 to see how it is used.
You can place multiple commands in this file - it is a simple way to tag commands for easy use.


1. Ensure that all gitsubmodule repo's are in http format. These can be found in .gitmodules.
Example: git@github.com:mechastrom/toggl-python-api-client.git should become: https://github.com/mechastorm/toggl-python-api-client.git

2. Ensure that requirements.txt contains all of your dependencies.

3. Run the following commands to set up the Heroku repository:

Create a new empty repository on Heroku: `heroku create`
Push your current branch onto Heroku's master branch: If on develop: `git push heroku develop:master`

If you get any errors in your push, ensure that steps 1 and 2 are satisfied properly.

4. Run the script manually on Heroku. There are two ways to do this:
If you have created your Procfile: Start a dyno: `heroku ps:scale worker=1`
To see the output of the script: `heroku logs`
Alternatively, you can run the following command to execute the script: `heroku run python check.py`

5. For the purposes of deploying on heroku, a .yml file is not ideal - we don't want to store sensitive credentials in version control.
We must create system environment variables to store configurations on Heroku. This process is easy - just put your data into the bash script provided, and run it. It will initialize the necessary config variables on Heroku.


If your scripts have any import errors, add those dependencies to requirements.txt, and push to your repository once more.

Once the script runs, it's time to schedule it.
1. Go to my apps: dashboard.heroku.com/apps

2. Hover over the app you pushed to. Icons will appear - click on the "resources" icon

3. Click "Get Add-ons"

4. Add the "Heroku Scheduler" add-on

5. Click on the scheduler to access your scheduled jobs. Click "Add Job.."

6. In the command field, enter: `python check.py`, or any terminal command. Select the frequency you want to run the script at.

7. You will need to modify your cofiguration. Heroku Scheduler does not allow for a weekly schedule. Thus, the python script automatically terminates
if it is not invoked at the correct time of the week. You may wish to adjust the valid range, under the date restriction options. Set the day of the week (0 = Monday), and the hour in which it may run.

8. Everything should be ready. Test things out to make sure the e-mails are being sent. Set the script to ignore date restrictions to make this easier(refer to MANUAL REPORT)

9. If you want to set up a staging App, refer to STAGING

#STAGING
It may be desirable to keep a Staging app and a Production app.

1. On the Heroku website, initialize a new App. Go to the settings of that app, and copy the repository URL to your clipboard.
2. On terminal, you need to add a new remote repository for staging: `git remote add staging your_repo_url_here`
3. If you run `git remove -v`, you should be able to see your heroku (production) remote, and your staging remote.
4. You can now run the steps outlined in #DEPLOYMENT, with two main differences, outlined in steps 5 to 7.
5. Instead of pushing to heroku, you must push to staging. NOTE: Heroku apps only run on their master branch. Thus, you push to the master branch of the dev app: `git push staging <branch_name>:master`

6. Because there are multiple heroku apps in your folder, `heroku run python check.py` will no longer work. You need to specify which app to run all commands on.
7. Use the --app flag to specify which app to run the command on: `heroku run python check.py --app alma-hours-monitoring-dev`

#CONFIG_PATH
- If an environment variable for CONFIG_PATH is set to the location of a .yml file, that configuration will be loaded instead of environment variables

- If a flag, containing the location of a .yml file, is passed to the script, that configuration will load instead of CONFIG_PATH or environment variables: 'python check.py config/configs.yml'

- If there is no configuration path available, either through flag or CONFIG_PATH, or if the specified .yml can not be loaded, the script will attempt to load the configuration from environment
variables.

If no CONFIG_PATH is specified and no flag passed, or if the YAML file can not be opened, the script will attempt to load configurations from system environment variables.

#CONFIGURATION NOTES
date_restrict - define the day and hour of the week which the script runs, and whether or not to apply this restriction

sendmail - defines whether or not the script should actually send out email

smtp - contains the smtp credentials used to send emails

togglAPI - contains the api credentials for toggl

admin - contains the email addresses of administrators. The users corresponding to these addresses (admins)  will not have hours computed for them

staff - email_role_staff_resource: the email address to which the summary reports will be sent to
staff - email_role_group_leads: the email address to which the 'not enough hours' emails will be cc'ed to
staff - from_email: the email address from which all emails will be sent

# MANUAL REPORT
If you want to run the report without taking into account the datetime restrictions, set the date restrict to_restrict to False in the .yml or environment variable options


#ADDING HOLIDAYS
Be sure to configure HOLIDAY_CONFIG_PATH to point to your yml file for holidays.
Observe this sample:
```
2014:
    -
        date: 2014-05-05

    -
        date: 2014-05-09
        percent_used: .5

    -
        date: 2014-05-11
        percent_used: .8

```

Listed are three holidays in 2014.
Percent_used is the value, from 0 to 1, representing how much of the holiday was utilized.

For example, on May 11, percent used is ".8". This means that the employee gets 80% of the day off, but still has to work 20% of the day.

Thus, if the regular workday was 10 hours, one would be expected to work for 2.

If no percent_used is specified, as with May 5th, it is automatically defaulted to "1" (full day off).


# To Test

Scenario 1.0:
If a full holiday occurs on the same day the report is requested, the report required hours should not change.

Scenario 1.1:
If a partial-holiday occurs on the same day the report is requested, the report required hours should not change.

Scenario 2:
If a full holiday occurs mid-week before the report is requested, the report required hours should be decreased by the working hours of a full day.

Scenario 2.1:
If a partial-holiday occurs mid-week before the report is requested, the report required hours should be decreased by the holiday utilization of a partial day.

Scenario 3.0.0:
If a full holiday occurs on the last working day of the report range, the report required hours should be decreased by the working hours of a full day.

Scenario 3.0.1:
If a partial holiday occurs on the last working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.

Scenario 3.1.0:
If a full holiday occurs on the first working day of the report range, the report required hours should be decreased by the working hours of a full day.

Scenario 3.1.1:
If a partial holiday occurs on the first working day of the report range, the report required hours should be decreased by the holiday utilization of a partial day.

Scenario 4.0:
If a full holiday occurs on the weekend contained in the report range, the report required hours should not change (weekend is not a working day).

Scenario 4.1:
If a partial-holiday occurs on the weekend contained in the report range, the report required hours should not change

Scenario 5.1.0 - 5.4.1:
If duplicate full/partial holidays occur in any of Scenario 1.0 to 4.1, only the first holiday should decrease the reports required hours by the workings hours of a full day

Scenario 6.0.0:
If checking on the boundary of two different years, a full holiday on a weekday of the reporting period, in the previous year, must still decrease the reports required holiday by a full work day

Scenario 6.0.1:
If checking on the boundary of two different years, a partial holiday on a weekday of the reporting period, in the previous year, must still decrease the reports required holiday by a partial holiday utilization

Scenario 6.1:
If checking on the boundary of two different years, if there is no holiday in the reporting period, the minimum required hours must be the same as if reporting on any other week of the year that contains no holiday

Scenario 7.0:
If a new employee is added to the system a month before he starts, he/she should not have required hours for the previous week (the week before they start work)

Scenario 7.1:
If a new employee joins part-way through the reporting week, the days that they did not work must not be included in their minimum hours calculation

Scenario 7.2:
If a new employee joins part-way through the reporting week, and works more hours than their minimum required, the percent they worked should exceed 100

Scenario 8.0:
If the user has not worked the minimum required hours, the correct difference between hours worked and hours required must be computed

#Loadup Class Tests

Scenario 9.0:
(load_configs) If no flag is passed in, and CONFIG_PATH is set to a file that exists, those options from CONFIG_PATH should be loaded in

Scenario 9.1:
(load_configs) If no flag is passed in, and CONFIG_PATH is set to something invalid, False should be returned

Scenario 9.2:
(load_configs) If a valid flag is passed in, and no CONFIG_PATH is set, the configurations should be loaded form the path in the flag

Scenario 9.3:
(load_configs) If an invalid flag is passed in, False should be returned

Scenario 10.0:
(create_config) If load_configs returns False, it should return configurations from environment variables

Scenario 10.1:
(create_config) If load_configs returns something, the configurations should be loaded from that stream

Scenario 11.0:
(generate_config_from_environment) If environment variables are properly set, returns configurations from the environment variables

Scenario 11.1:
(generate_config_from_environment) If environment variables are not properly set, should terminate (no return)










