# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 20:18:46 2020

@author: Arti Patel
"""

from selenium import webdriver
import time
import numpy as np
import re
import pandas as pd
import pickle

path = 'chrome_driver_path'



def get_frb_article_links(browser):

    new_urls = []
    articles = browser.find_elements_by_class_name('itemTitle')
    for article in articles:
        url = article.find_element_by_tag_name('a').get_attribute('href')
        new_urls.append(url)
    return new_urls
def navigate_frb_speeches():

    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path=path, options=option)
    browser.get("https://www.federalreserve.gov/newsevents/speeches.htm")
    article_urls = []
    new_urls = get_frb_article_links(browser)
    while not article_urls or article_urls[-1] != new_urls[-1]:
        article_urls += get_frb_article_links(browser)
        next_button = browser.find_element_by_css_selector("a[ng-click='selectPage(page + 1, $event)']")
        next_button.click()
        new_urls = get_frb_article_links(browser)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return article_urls

def get_frb_speech_text(url_lst):

    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path = path,options=option)
    frb_articles = []
    for url in url_lst:
        article_details = []
        article_details.append(url)
        browser.get(url)
        article_times = browser.find_elements_by_class_name('article__time')
        article_details.append(article_times[0].text)
        article_titles = browser.find_elements_by_class_name('title')
        article_details.append(article_titles[0].text)
        article_speakers = browser.find_elements_by_class_name('speaker')
        article_details.append(article_speakers[0].text)
        article_locations = browser.find_elements_by_class_name('location')
        article_details.append(article_locations[0].text)
        article_texts = browser.find_elements_by_xpath('//*[@id="article"]/div[3]')
        article_details.append(article_texts[0].text)
        frb_articles.append(article_details)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return frb_articles




def get_fomc_article_links(browser):
    new_urls = []
    speeches = browser.find_elements_by_class_name('itemTitle')
    for speech in speeches:
        if re.findall(r'FOMC statement', speech.text):
            new_urls.append(speech.find_element_by_tag_name('a').get_attribute('href'))
    return new_urls

def navigate_fomc_speeches():
    fomc_urls = []
    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(options=option)
    browser.get("https://www.federalreserve.gov/newsevents/pressreleases.htm")
    new_urls = get_fomc_article_links(browser)
    while not fomc_urls or (not new_urls or fomc_urls[-1] != new_urls[-1]):
        fomc_urls += get_fomc_article_links(browser)
        time.sleep(np.random.randint(5,10))
        next_button = browser.find_element_by_css_selector("a[ng-click='selectPage(page + 1, $event)']")
        next_button.click()
        new_urls = get_fomc_article_links(browser)
    browser.close()
    return fomc_urls

def get_fomc_speech_text(url_lst):
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(options=option)
    fomc_speeches = []
    for url in url_lst:
        article_details = []
        article_details.append(url)
        browser.get(url)
        article_times = browser.find_elements_by_class_name('article__time')
        article_details.append(article_times[0].text)
        article_titles = browser.find_elements_by_class_name('title')
        article_details.append(article_titles[0].text)
        article_texts = browser.find_elements_by_xpath('//*[@id="article"]/div[3]')
        article_details.append(article_texts[0].text)
        fomc_speeches.append(article_details)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return fomc_speeches

def get_frb_article_links_archived(browser):

    new_urls = []
    new_titles = []
    new_speakers = []
    new_locations = []
    new_dates = []
    speeches = browser.find_element_by_id('speechIndex')
    speech_urls = speeches.find_elements_by_tag_name('a')
    for speech in speech_urls:
        url = speech.get_attribute('href')
        new_urls.append(url)
        title = speech.text
        new_titles.append(title)
    speech_dates = speeches.find_elements_by_tag_name('li')
    for speech in speech_dates:
        date_ = re.findall(r'(?<=)(\S+ \d+, \d{4})', speech.text)[0]
        new_dates.append(date_)
    speech_speakers = speeches.find_elements_by_class_name('speaker')
    for speaker in speech_speakers:
        new_speakers.append(speaker.text)
    speech_locations = speeches.find_elements_by_class_name('location')
    for location in speech_locations:
        new_locations.append(location.text)
    return new_urls, new_titles, new_speakers, new_locations, new_dates

def navigate_frb_archived_speeches():

    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path = path,options=option)
    browser.get("https://www.federalreserve.gov/newsevents/speech/speeches-archive.htm")
    speech_urls = []
    speakers = []
    locations = []
    dates_ = []
    titles = []
    year_links = []

    list_of_years = browser.find_element_by_xpath('//*[@id="article"]/div/div/div/ul')
    all_year_links = list_of_years.find_elements_by_tag_name("a")
    for year_link in all_year_links:
        url = year_link.get_attribute('href')
        year_links.append(url)
    for url in year_links:
        browser.get(url)
        new_urls, new_titles, new_speakers, new_locations, new_dates = get_frb_article_links_archived(browser)
        speech_urls = speech_urls + new_urls
        titles = titles + new_titles
        speakers = speakers + new_speakers
        locations = locations + new_locations
        dates_ = dates_ + new_dates
        time.sleep(np.random.randint(5,10))
    browser.close()
    # removing extra url accidentally picked up
    del titles[-118]
    del speech_urls[-118]
    return speech_urls, speakers, locations, dates_, titles



def get_frb_speech_text_archived(url_lst):

    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path = path,options=option)
    speech_text = []
    for url in url_lst:
        browser.get(url)
        paragraphs = browser.find_elements_by_tag_name('p')
        complete_text = ""
        for paragraph in paragraphs:
            complete_text += ' ' + paragraph.text
        speech_text.append(complete_text)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return speech_text

def clean_speech_text(df):

    df_new = df.copy()
    full_text_col = df_new['full_text'].apply(lambda x: remove_references(x))
    full_text_col = full_text_col.str.replace('\n', ' ')
    full_text_col = full_text_col.apply(lambda x: re.sub(r'(http)\S+(htm)(l)?', '', x))
    full_text_col = full_text_col.apply(lambda x: re.sub(r'(www.)\S+', '', x))
    full_text_col = full_text_col.apply(lambda x: re.sub(r'[\d]', '', x))
    full_text_col = full_text_col.str.replace('—', ' ')
    full_text_col = full_text_col.str.replace('-', ' ')
    full_text_col = full_text_col.apply(lambda x: re.sub(r'[^\w\s]', '', x))
    full_text_col = full_text_col.apply(lambda x: re.sub(r'([Rr]eturn to text)', '', x))
    full_text_col = full_text_col.apply(lambda x: re.sub(r'([Pp]lay [vV]ideo)', '', x))
    df_new.drop(labels='full_text', axis="columns", inplace=True)
    df_new['full_text'] = full_text_col
    return df_new



def remove_references(text):
    """
    Removes references at the end of
    speeches, if any. Helper function
    to assist in data cleaning.
    
    Parameters: 
    text (string): speech text
    
    Returns:
    string: cleaned speech text sans
          references
    """
    references_loc = text.find('\nReferences\n')
    if references_loc != -1:
        text = text[:references_loc]
    return_to_text_loc = text.find('[Rr]eturn to text\n')
    if return_to_text_loc != -1:
        text = text[:return_to_text_loc]
    concluding_remarks_loc = text.find('These remarks represent my own views, which do not necessarily represent those of the Federal Reserve Board or the Federal Open Market Committee.')
    if concluding_remarks_loc != -1:
        text = text[:concluding_remarks_loc]
    return text


#speech_urls = navigate_frb_speeches()
#speeches = get_frb_speech_text(speech_urls)
#speeches_df = pd.DataFrame(frb_arcolumns=['url', 'speech_date', 'title', 'speaker', 'location', 'full_text'])

def navigate_fomc_archived_speeches():
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path = path,options=option)
    browser.get("https://www.federalreserve.gov/newsevents/pressreleases/press-release-archive.htm")
    fomc_urls = []
    titles = []
    year_links = []

    list_of_years = browser.find_element_by_xpath('//*[@id="article"]/div/div/div/ul')
    all_year_links = list_of_years.find_elements_by_tag_name("a")
    for year_link in all_year_links:
        url = year_link.get_attribute('href')
        year_links.append(url)
    for url in year_links:
        browser.get(url)
        new_urls, new_titles = get_fomc_links_archived(browser)
        fomc_urls = fomc_urls + new_urls
        titles = titles + new_titles
        time.sleep(np.random.randint(5,10))
    browser.close()
    return fomc_urls, titles


def get_fomc_links_archived(browser):
    new_urls = []
    new_titles = []
    releases = browser.find_element_by_id('releaseIndex')
    release_urls = releases.find_elements_by_tag_name('a')
    for release in release_urls:
        if re.findall(r'FOMC [Ss]tatement', release.text):
            url = release.get_attribute('href')
            new_urls.append(url)
            title = release.text
            new_titles.append(title)
    return new_urls, new_titles


def get_fomc_text_archived(url_lst):
    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path = path,options=option)
    speech_text = []
    fomc_dates = []
    for url in url_lst:
        browser.get(url)
        paragraphs = browser.find_elements_by_tag_name('p')
        complete_text = ""
        for paragraph in paragraphs:
            complete_text += ' ' + paragraph.text
        speech_text.append(complete_text)
        date_ = browser.find_elements_by_tag_name('i')[0]
        date_ = re.findall(r'(?<=[rR]elease [dD]ate: )(\w* \d*,? \d*)', date_.text)[0]
        fomc_dates.append(date_)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return speech_text, fomc_dates

def get_fomc_article_links(browser):
    new_urls = []
    speeches = browser.find_elements_by_class_name('itemTitle')
    for speech in speeches:
        if re.findall(r'FOMC statement', speech.text):
            new_urls.append(speech.find_element_by_tag_name('a').get_attribute('href'))
    return new_urls

def navigate_fomc_speeches():
    fomc_urls = []
    # initiating selenium Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path=path,options=option)
    browser.get("https://www.federalreserve.gov/newsevents/pressreleases.htm")
    new_urls = get_fomc_article_links(browser)
    while not fomc_urls or (not new_urls or fomc_urls[-1] != new_urls[-1]):
        fomc_urls += get_fomc_article_links(browser)
        time.sleep(np.random.randint(5,10))
        next_button = browser.find_element_by_css_selector("a[ng-click='selectPage(page + 1, $event)']")
        next_button.click()
        new_urls = get_fomc_article_links(browser)
    browser.close()
    return fomc_urls

def get_fomc_speech_text(url_lst):
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    browser = webdriver.Chrome(executable_path=path,options=option)
    fomc_speeches = []
    for url in url_lst:
        article_details = []
        article_details.append(url)
        browser.get(url)
        article_times = browser.find_elements_by_class_name('article__time')
        article_details.append(article_times[0].text)
        
        article_titles = browser.find_elements_by_class_name('title')
        article_details.append(article_titles[0].text)
        
        article_texts = browser.find_elements_by_xpath('//*[@id="article"]/div[3]')
        article_details.append(article_texts[0].text)
        
        article_releasetime = browser.find_elements_by_class_name('releaseTime')
        article_details.append(article_releasetime[0].text)
        
        fomc_speeches.append(article_details)
        time.sleep(np.random.randint(5,10))
    browser.close()
    return fomc_speeches















