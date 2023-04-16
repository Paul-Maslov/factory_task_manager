![image](static/images/logodls.png)
FACTORY TASK MANAGER

This project for managing the execution of tasks by factory employees.
Task Manager will handle all possible problems during product furniture in your factory.
Everyone from the company can create Task, assign this Task to team-members, and mark the Task as done.
Each employee has his own page with a list of projects in which he participates and tasks that he performs.
Everyone in the corresponding tasks can post posts containing the solution of the problem or comment on existing posts
   
Description of DB structure of our project

![factory_task_manager_database_v01](https://user-images.githubusercontent.com/112548104/230823770-b40458d6-8aef-4b48-a367-c78881df3c4e.png)

Features: 

✨ Authentication functionality for Employee/User

✨ Managing projects/tasks/posts/commentaries/users from website interface

✨ Powerful admin panel for advanced management

✨ The project can be expanded and supplemented with features at the request of the customer



Page images:

- home page
![image](https://user-images.githubusercontent.com/112548104/230824131-d0c1ce3d-260d-4fbc-815a-40c3de411f57.png)

- list of Tasks
![image](https://user-images.githubusercontent.com/112548104/230825666-8971e564-0823-41dd-a5c6-2fc48fb73d80.png)

- Task detail
![image](https://user-images.githubusercontent.com/112548104/230825761-5e8e2c1b-7317-4a54-a2e1-0e9907a39986.png)

- list of employeees
![image](https://user-images.githubusercontent.com/112548104/230826029-f6a8079b-c9b1-4206-a84b-5f62d2826e3d.png)

- Employee detail
![image](https://user-images.githubusercontent.com/112548104/230826124-09be38ee-2f70-4217-b5a9-c488e23516c2.png)


Developing

👉 Step 1 - Download the code from the GH repository (using GIT)

$ git clone git@github.com:Paul-Maslov/factory_task_manager.git

$ cd factory_task_manager

👉 Step 2 - Create virtual environment

$ python3 -m venv venv

👉 Set Up for Apple

$ source venv/bin/activate

👉 Set Up for Windows

$ venv/Scripts/activate

Install modules via VENV (windows)

$ virtualenv env

$ .\env\Scripts\activate

👉 Step 3 - Install info about project

$ pip install -r requirements.txt

👉 Step 4 Set Up Database

$ python manage.py makemigrations

$ python manage.py migrate

👉 Step 5 Start the project

$ python manage.py runserver

At this point, the app runs at http://127.0.0.1:8000/.

✨ Create Users

✨ To see .env variables

$ pip install python-dotenv
$ from dotenv import dotenv_values
$ config = dotenv_values(".env")

✨ Description of environment variables as sample 

👉 .env_sample is in the root folder
👉 Access token are defined as security credentials that allow your application to access an API 
👉 Secret token is environment variable that securely reference secrets for their value
👉 The Django secret key is used to provide cryptographic signing. This key is mostly used to sign session cookies.

Links

Repository: https://github.com/Paul-Maslov/factory_task_manager


