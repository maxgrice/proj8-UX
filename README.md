# Project 8: User interface for authenticated brevet time calculator service

In this project I created a frontend UI for Brevet app using Flask-WTF
and Flask-Login. The frontend UI reused the authentication service which was created in project 7. In this project, I added the following modifications:

** "http://<host:port>/api/register 

Entering the following url (shown above) in the browser takes the user to a sign up page where the user can enter their username and password to register. If the username already exists, a 401 error is returned. Otherwise, if fields are left blank, the sign up page will simply reload for the user to try again.

** "http://<host:port>/api/token

Once the user has registered, entering this url in the browser will display a login page where the user must enter a valid username and password. If the user is not in the data base or if their password is not valid, a 401 error is returned. If one of the fields is left blank, the login page is simply reloaded and rendered again for the user to try login in again. If the entered credentials are valid (determined using basic authentication), a page displaying the generated token as well as the tokens duration is displayed (in JSON format). This token can be pasted into the URL along with the desired query in order to obtain a desired resource (from project 6). An example is shown below:

http://127.0.0.1:5001/listAll?token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMDY0MzE2NiwiZXhwIjoxNTIwNjQzMTk2fQ.eyJpZCI6IjVhYTMyYzNlNTc0MWM1MDA0OTIyODMyMCJ9.olcjG8VkKYMsHlaTdKV-0K0bbZoEZo5Thfirxmqpz68

In the example above, the token (specified by ?token=) allows the user to access the desired resource which, in this case, lists all the brevet times in the default JSON format.

** "http://<host:port>/logout

Entering this url will log out the user and force any tokens generated in that session to expire (so the user can no longer access any protected resources), and then redirect the user back to the login page. This is done by adding a random integer to the session key so that the signature (when decoded) is no longer valid. Note that if the browser is simply closed and reopened, the user should still be logged in (due to remember me functionality). 

CSRF protection is also set in the form template in order to prevent any unwanted attacks on the users session data.

In Summary, the 3 Additional Functionalities Added to the UI are: 

(a) Remember Me
(b) Logout 
(c) CSRF protection (Note: Sessions are not maintained)

## Tasks

You'll turn in your credentials.ini using which we will get the following:

* The working application with three parts.
* Dockerfile
* docker-compose.yml
