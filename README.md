# SOF535
## Hospital Appointment Application

**By Eric Cho**

This application is hospital appointment application for fulfillment of SOF535 course at Stratford University. The backend is implemented using Django (Python) and the front-end is implemented using HTML/Javascript/CSS

The main files in this code-base are as follows.

`templates/apptpage.html` - This page contains the HTML/Javascript to create the main user interface and the javascript to validate the forms and to pass the data to backend

`hospitalappt/views.py` - This page contains backend handling of patient data submitted from the frontend. This file also contains the class objects for Person, Patient, Patients, and Doctors for fulfillment of objected-oriented programming for this course.

To run this on local machine, `python3` should be installed and `django` should be installed as well. Once inside the project folder `python manage.py runserver` can be executed to run the application on `127.0.0.1:8000` 

The live instance is currently deployed on http://stratford.eric-cho.com/
