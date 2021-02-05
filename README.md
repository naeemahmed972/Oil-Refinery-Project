# A project built using Python (Django) to manage Oil Storage at an Oil Refinery

### To run the project on your PC using local server, perform following steps:

**Note: This project has been tested on Windows 10 platform only, so following steps are for Windows environment.**

***

* First of all you need to install Python version [3.8.6](https://www.python.org/ftp/python/3.8.6/python-3.8.6-amd64.exe "Python 3.8.6") on you PC
    * Don't forget to check the option `Add to PATH` while installing Python

***

* Then install [git](https://github-releases.githubusercontent.com/23216272/70412280-5663-11eb-990d-a4a657b9c1cf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20210205%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210205T041832Z&X-Amz-Expires=300&X-Amz-Signature=ad969cc6d9eaf85e6adfe19e52048e61a1bafee537421be77e0399b4cc79d007&X-Amz-SignedHeaders=host&actor_id=42473829&key_id=0&repo_id=23216272&response-content-disposition=attachment%3B%20filename%3DGit-2.30.0.2-64-bit.exe&response-content-type=application%2Foctet-stream "Git For Windows") for windows

***

* Now open the command prompt in your desired directory
    * Press `SHIFT + Right Mouse Click` and Select `Open Command Window Here` or `Open Powershell Window Here`

***

* Next, you have to clone the repository to your PC
    * Run the following commmand:
    `git clone https://github.com/naeemahmed972/Oil-Refinery-Project.git`

***

* Change to Project Directory by running the command:
    `cd Oil-Refinery-Project`

***

* Run the following command:
    `pipenv install`

***

* Now run the following command:
    `python manage.py migrate`