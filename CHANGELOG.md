# Changelog

All notable changes to this project will be documented in this file.

## [v2.12.7] - 2025-06-23
- Update instruction in telegram notification second time

## [v2.12.6] - 2025-06-11
- Update instruction in telegram notification

## [v2.12.5] - 2025-06-09
- Update README.md

## [v2.12.4] - 2025-06-09
- Add description how to find a telegram ID in telegram notification route

## [v2.12.3] - 2025-06-08
- Add changelog file

## [v2.12.2] - 2025-06-08
- Update Dockerfile to use Hypercorn for serving the application
- Add environment variables for configuration (closes #20)

## [v2.12.1] - 2025-06-08
- Refactor view page layout with new header and row styling
- Implement sorting functionality for table columns

## [v2.12.0] - 2025-06-04
- Add change rule functionality to telegram notification service
- Update frontend to support new operation

## [v2.11.0] - 2025-06-03
- Add remove functionality to route and telegram utils (closes #24)
- Update frontend

## [v2.10.0] - 2025-06-03
- Add uuid to the message
- Change telegram service to telegram utils in write routes
- Add new hash functionality to telegram utils
- Delete it from telegramAPI
- Add unified function to telegramAPI to send data to rabbitmq
- Add docstrings
- Add uuid utils
- Add uuid test unit (closes #23, #26)

## [v2.9.0] - 2025-06-03
- Refactoring frontend with copilot agent

## [v2.8.2] - 2025-06-03
- Saving logs to the logs.txt (closes #27)

## [v2.8.1] - 2025-06-02
- Rename logs
- Fix bug (closes #25)

## [v2.8.0] - 2025-05-31
- Add telegram utils
- Refactoring telegram api (working with async)
- Convert flask into flask[async] (with hypercorn)
- Add post and get to telegram_notification
- Add html and js for telegram notification (closes #4)

## [v2.7.2] - 2025-05-26
- Add models unit tests (closes #15)
- Add docstring to hash model (closes #11)

## [v2.7.1] - 2025-05-26
- Fix database util
- Add database utils unit tests
- Add delete functionality to database service

## [v2.7.0] - 2025-05-26
- Add routes unit tests
- Fixes routes
- Add docstring to routes
- Add database utils
- Add delete functionality to database

## [v2.6.0] - 2025-05-25
- Add unit tests to utils
- Add docstring to utils
- Polishing functions

## [v2.5.0] - 2025-05-25
- Try to connect repeatedly to rabbitmq (closes #13)
- Added new database utils for write route
- Add log for better debugging

## [v2.4.2] - 2025-05-25
- Add database utils for view route
- Rename field in databases (closes #12)

## [v2.4.1] - 2025-05-24
- Update docker (closes #9)

## [v2.4.0] - 2025-05-23
- Add rating for hashes (representative way for telegram bot) (closes #7)

## [v2.3.0] - 2025-05-22
- Added telegramAPI service (with RabbitMQ communication)
- Add two new command to communicate (|ADD|, |PING|)
- Threading this in __init__.py
- Refactoring write route to new service
- Fix typos

## [v2.2.1] - 2025-05-21
- Hot fix in readme.md

## [v2.2.0] - 2025-05-21
- add LICENSE file and update readme.md

## [v2.1.3] - 2025-05-21
- hot fix

## [v2.1.2] - 2025-05-21
- Add database utils and use it in write routes

## [v2.1.1] - 2025-05-21
- Add dir utils and renaming functions.py to hash_utils.py

## [v2.1.0] - 2025-05-21
- add Hash model

## [v2.0.0] - 2025-05-21
- Refactor to MVC structure
- Update Dockerfile
- Remove and ignore __pycache__

## [v1.10.3] - 2025-04-05
- update dockerfile

## [v1.10.2] - 2025-04-03
- add counting for row in view.html

## [v1.10.1] - 2025-04-03
- cleaning the code

## [v1.10.0] - 2025-04-03
- add database class and refactor code for this change

## [v1.9.0] - 2025-04-02
- add telegram user route

## [v1.8.0] - 2025-03-28
- add json validation, ajax request and errno as a response to help catch the error in user input

## [v1.7.1] - 2025-03-27
- automaticly run pass permission with .env

## [v1.7.0] - 2025-03-27
- make a https connection (add ssl protokol)

## [v1.6.1] - 2025-03-25
- fix encoding error

## [v1.6.0] - 2025-03-25
- add telegram notification with bot

## [v1.5.0] - 2025-03-25
- add docker env

## [v1.4.0] - 2025-03-25
- migrate to .env
- docker installation

## [v1.3.3] - 2025-03-25
- fixed the route error

## [v1.3.2] - 2025-03-23
- added sort elements
- create write page

## [v1.3.1] - 2025-03-18
- make button pretty
- add counts

## [v1.3.0] - 2025-03-17
- add welcome and view html page

## [v1.2.3] - 2025-03-16
- add validation

## [v1.2.2] - 2025-03-16
- add __pycache__ to git ignore

## [v1.2.1] - 2025-03-16
- add max length of word

## [v1.2.0] - 2025-03-16
- working version 1.0

## [v1.1.0] - 2025-03-16
- add mongouri

## [v1.0.1] - 2025-03-16
- change gitignore

## [v1.0.0] - 2025-03-16
- Initial release

