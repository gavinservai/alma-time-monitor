#!/bin/bash
# Adding Heroku Environment Configurations

# HOLIDAYS - THE YAML FILE TO EXTRACT HOLIDAYS FROM - EITHER A URL OR A FILEPATH IS ACCEPTABLE
echo `heroku config:set HOLIDAY_CONFIG_PATH='your_path_or_url_here' --app your-app-name `

# SMTP - THE SMTP DETAILS FOR YOUR MAIL PROVIDER
echo `heroku config:set SMTP_HOST='smtp.yourhost.com' --app your-app-name `
echo `heroku config:set SMTP_PORT='1234' --app your-app-name`
echo `heroku config:set SMTP_USERNAME='your_username' --app your-app-name`
echo `heroku config:set SMTP_PASSWORD='your_password' --app your-app-name`

# DATE RESTRICTION - THE DAY AND HOUR OF THE WEEK THAT THE SCRIPT IS RESTRICTED TO. SET FLAG TO FALSE TO ENABLE MANUAL MODE
echo `heroku config:set DATE_RESTRICT_FLAG=False --app your-app-name`
echo `heroku config:set DATE_RESTRICT_WEEKDAY=0 --app your-app-name`
echo `heroku config:set DATE_RESTRICT_HOUR=0 --app your-app-name`

# SENDMAIL - WHETHER OR NOT THE SCRIPT SHOULD SEND OUT EMAILS. SET TO FALSE TO DISABLE MAILING
echo `heroku config:set SENDMAIL_FLAG=False --app your-app-name`

# TOGGL API - YOUR TOGGL API CREDENTIALS
echo `heroku config:set TOGGL_TOKEN='your_token' --app your-app-name`
echo `heroku config:set TOGGL_USER_AGENT='your_user_agent' --app your-app-name`
echo `heroku config:set TOGGL_WORKSPACE_ID=12345 --app your-app-name`

# ADMIN - THE EMAIL ADDRESSES OF ADMINS WHO SHOULD NOT BE INCLUDED IN THE REPORT - YOU CAN ADD AS MANY EMAILS AS NEEEDED
echo `heroku config:set ADMIN_EMAIL='["some_admin_user@somehost.com", "another_admin_user@somehost.com"]' --app your-app-name`

# STAFF - THE EMAIL ADDRESSES OF STAFF
echo `heroku config:set STAFF_EMAIL_ROLE_STAFF_RESOURCE='person_who_gets_cc_of_missing_hour_reports@somehost.com' --app your-app-name`
echo `heroku config:set STAFF_EMAIL_ROLE_GROUP_LEADS='person_who_receives_summary_reports@somehost.com' --app your-app-name`
echo `heroku config:set STAFF_FROM_EMAIL='sender_address@somehost.com' --app your-app-name`
