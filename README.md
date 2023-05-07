# indeed-job-finder

## Introduction

A simple web app to practice and showcase frontend and backend coding, plus use of NLP techniques.

Tech stack: Python, Selenium, React JS, FastAPI, NLP (Spacy, NLTK, Gensim, etc).

Below is a screenshot of the app:

<img src="https://user-images.githubusercontent.com/26933333/236651424-0cb03108-fa35-4caf-8ec8-1aa815df3b81.png" width="800" height="450" style="border: 2px solid  gray;" />

## Dependencies for Backend:

(1) Python 3.8+

(2) Selenium: https://pypi.org/project/selenium/
pip install selenium

(3) Firefox desktop version for Ubuntu: https://www.mozilla.org/en-US/firefox/new/
download and extract to local path, e.g.: '~/OpenSource/Selenium/bin/firefox-112.0.1/firefox'

(4) Selenium driver for Firefox: https://github.com/mozilla/geckodriver/releases
download and extract to local path, e.g.:'~/OpenSource/Selenium/bin/firefox-106+/geckodriver'

(5) FastApi, Unicorn
pip install fastapi
pip install unicorn[standard]

(6) BeautifulSoup: https://pypi.org/project/beautifulsoup4/

pip install beautifulsoup4

(7) Spacy: https://spacy.io/usage
pip install spacy

(8) download a spacy language model
python -m spacy download en_core_web_lg

(9) use NLTK functions
pip install nltk

(10) to train doc2vec model
pip install gensim

## Dependencies for Frontend:

(1) Node JS:

For Ubuntu 22.04, it can be done by:

```
sudo apt update
sudo apt install nodejs npm
```

After installation, check version should be something like:

```
$ node -v
v18.14.2
$ npm -v
9.5.0
```

## Usage

Step 1. Start backend:

(1) Edit .env in backend folder to be something like:

```
# the absolute path to firefox driver for selenium
DRIVER_PATH_FIREFOX='/home/mgu/OpenSource/Selenium/bin/firefox-driver-106+/geckodriver'

# the absolute path to firefox browser executable
BROWSER_PATH_FIREFOX='/home/mgu/OpenSource/Selenium/bin/firefox-browser-112.0.1/firefox'

# the User-Agent string of your browser
BROWSER_USER_AGENT='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'
```

(2) Open a new terminal to run the following command:

```
$ cd backend
$ ./start_backend_server.sh
```

Step 2. Start frontend:

(1) install npm modules:

```
$ npm install
```

(2) start frontend app:

```
$ npm start
```

or

```
$ ./start_frontend_app.sh
```

Step 3. Interact with UI:

(1) Enter JobTitle and Location and click Search. Backend will scrape Indeed for the entered location (for now, assume JobTitle is fixed to 'Senior Software Engineer' for my case).

UI will see a modal popup telling the search has started. You can then click "Search Results" or "Server Logs".

(2) Upon the search complete, click Search Results will see a list of job items. Click each item will show the job description.

(3) During the search, click Server Logs will show how the search is going at backend.

## To-Do

(1) Allow user to enter skills or upload resume;
(2) Match user skills or the resume against each job description to get a score;
(3) Order the job items by the score;
