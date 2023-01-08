import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import re
import os
from pathlib import Path


def write_clean_html_text_files(input_folder, output_folder):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    for item in os.listdir(input_folder):
        path = input_folder
        with open(os.path.join(path, item), 'rt',encoding="utf8") as dafile:
            soup = BeautifulSoup(dafile, "html.parser")
            text = soup.get_text()
            cleantext = re.sub(CLEANR, ' ', text)
            newtext = re.sub(r"[^a-zA-Z0-9 ]", "", cleantext)
        with open(os.path.join(output_folder, item + '.txt'), 'w+', encoding='utf-8') as f:
            f.write(newtext)
