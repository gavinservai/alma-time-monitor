# Release Notes

# 1.2.0

*Changes*

- Removed PRODUCTION, DEV, and MANUAL flags
- CONFIG_PATH now used to load configurations. Loads environment variables if no CONFIG_PATH specified.
- HOLIDAY_CONFIG_PATH now used to load holidays. Can be loaded from the filesystem or from a URL.
- Scenario's and Tests added (9.0 to 11.1)
- Fixed issue where the output said that e-mail were being sent, even when e-mails were not being sent
- Command line reporting now re-ordered by the percent of required hours that employees worked
- Sample Configuration files created, old files untracked
- Sample bash script created for convenient Heroku Deployment
- System now supports a variable amount of administrator e-mails - previously, only two were supported

*Known Issues*

- If a new employee is added to Toggl in advance of starting his/her work-term, that employee will receive e-mails for a week they did not work
- The command-line output is not in real-time. This creates an inconvenience when debugging issues.

# 1.1.0

*Changes*

- DEV mode no longer sends out e-mails
- E-mails sent out to individual employees
- All credentials and keys moved to configuration files
- User Case Scenario's expanded and refined
- Unit Tests added for Scenario's 1.0 - 8.0

*Known Issues*

- When in DEV mode, the output says that e-mails are being sent. In reality, no e-mails are being sent.
- If a new employee is added to Toggl in advance of starting his/her work-term, that employee will receive e-mails for a week they did not work
- Removing of config files for open-source
- Command line report must be re-ordered by hours missing

# 1.0.0

*Changes*

- Version 1.0 Initial Release

*Known Issues*

- If a new employee is added to Toggl in advance of starting his/her work-term, that employee will receive e-mails for a week they did not work
- Must thoroughly test system for use cases mentioned in README
- Must write Use Cases for the New Employee checking