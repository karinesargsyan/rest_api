Task:
Building a Python REST API Test Automation Framework

1) Using Python requests library you need to build an API automation framework.
Use this website https://crudcrud.com/ which has a running server under it.
All neccessary documentation you can find in the webpage.

2) Using pytest framework create couple of cases for main API calls.

3) Generate allure report.

Here is the solution commited: 
Git copy and go to repo.

1. First install the environment
pip install -r requirements.txt

2. To see the allure report based on previews runs use this command line:
$ allure serve report/

3. To rerun test use this command line:
$ pytest -s tests/test_cases.py  --alluredir=report/
