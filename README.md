# Github-Scraper
This repository searches for github profiles and extracts data from them


## Overview

This repository contains a code that aims to search for profiles in a specific field based on a keyword and extract data from each profile with a maximum number of 50 profiles per search
## Getting Started

### Follow these steps to get started with the project:
To begin, you will need to clone this GitHub repository by running this command in the command prompt :
```bash
$ git clone [https://github.com/06sahar06/Github-scraper.git]
```
Navigate to the project directory:
```bash 
$ cd Github-Scraper
```

## Usage

### Before running the project, you need to replace the Github_access_token with your own one 


### To run the project, use the following command:
```bash
$ python github_scraper.py
```


## Using the code with streamlit
### Follow these steps to create an interface:
First, you will need to install streamlit by running the following command in the command prompt :
```bash
$ pip install streamlit
```
Create a virtual environment:

```bash
$ python -m streamlit_env myenv
$ streamlit_env\Scripts\activate
```

you can then run the streamlit app directly:
```bash
$ streamlit run github_scraper.py
```
Streamlit will then launch a local web server and open your app in the default web browser. You can interact with your app through the browser.
To stop the Streamlit server, go back to the command prompt and press Ctrl + C.

