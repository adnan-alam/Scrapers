## Project Details

* **run_scraper.py**, the script to scrape proxies from https://openproxy.space/list.

* **user_agents.txt**, this file contains browsers' user agents.

* **requirements.txt**, program's dependencies. It can be used to install dependencies.


## Installation

* First Install Python 3.6 or latest version for your pc from www.python.org  if not installed. For 32bit pc install 32bit version otherwise install 64bit version.

* Open the command prompt/terminal in administrator mode and run: ```pip install virtualenv``` to install **virtualenv**, if not installed.
  Virtual environment is recommended.

* Go to the project directory from terminal. Then run: ```virtualenv .env```, it will create a virtual environment named **.env** in your project directory.
  Now, you'll have to activate it.

* To activate virtual environment, for Windows OS run: ```.env\Scripts\activate```. For Linux/Mac: ```source .env/bin/activate```.
  As virtual environment is activated, we can install dependencies(Python packages/modules).

* To install dependencies run: ```pip install -r requirements.txt```.

* Download chromedriver from: https://chromedriver.chromium.org/downloads and keep it in the project directory.
  Chromedriver is needed as we are using **Selenium** webdriver for the script.

* Run the scraper by this command: ```python run_scraper.py```.
  After the scraper runs successfully a file named **proxies.json** with proxies will be created.

* You can deactivate the virtual environment after running the script by: ```deactivate```.
