# A project built using Python (Django) to manage Oil Storage at an Oil Refinery

### To run the project on your PC using local server, perform following steps:

**Note: This project has been tested on Windows 10 platform only, so following steps are for Windows environment.**
***
* First of all you need to install Python version [3.8.6](https://www.python.org/ftp/python/3.8.6/python-3.8.6-amd64.exe "Python 3.8.6") on you PC
    * Don't forget to check the option `Add to PATH` while installing Python
***
* Then install [git](https://git-scm.com/ "Git For Windows") for windows
***
* Now open the command prompt in your desired directory (where you want to keep the project)
    * Press `SHIFT + Right Mouse Click` and Select `Open Command Window Here` or `Open Powershell Window Here`
***
* Run the following command:
    * `pip install pipenv`
***
* Next, you have to clone the repository to your PC
    * Run the following commmand:
        * `git clone https://github.com/naeemahmed972/Oil-Refinery-Project.git`
***
* Change to Project Directory by running the command:
    * `cd Oil-Refinery-Project`
***
* Run the following command:
    * `pipenv install`
***
* Now run the following command:
    * `python manage.py migrate`
***
* Now run the command and provide credentials to create the admin account for the project:
    * `python manage.py createsuperuser` 
***
* Now to run the project, give the following command:
    * `python manage.py runserver`