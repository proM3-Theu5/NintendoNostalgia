# For Web Crawling and Scraping data
import requests
from bs4 import BeautifulSoup
import re

# For storing the retrieved data
import pandas as pd
import numpy as np

# Preliminary data storage
import json
import os

def get_html_content(URL):
    web_page = requests.get(URL)
    return web_page

def page_details(web_page):
    print('URL : '+web_page.url)
    print("Status Code : "+str(web_page.status_code))
    print("Encoding : "+web_page.encoding)
    

def page_soup(web_page):
    return BeautifulSoup(web_page.content, 'html.parser')

# Function to find all occurences of hyphen in text
def all_occurences(text,char):
    return [i for i,char_s in enumerate(text) if char == char_s ]

def get_game_NameYearURL(game_uls):
    
    # Generating details for all games
    game_year = {}
    game_url = {}
    for game_ul in game_uls:
        game_li = game_ul.find_all('li')
        for game in game_li:
            text = game.text
            hyph_places = all_occurences(text,"-")
            if len(hyph_places) > 0:
                name = text[:hyph_places[-1]-1]
                year = text[hyph_places[-1]+2:]
            else:
                name = text[:-7]
                year = text[-5:]
            try :
                game_url[name] = game.find('a').get_attribute_list('href')[0]
                game_year[name] = year
            except:
                game_url[name] = np.NaN
                game_year[name] = np.NaN
                
    return game_year,game_url            
    
def get_attribute_list(game_infobox):
    
    try:
        info_divs = game_infobox.find_all('div',recursive = False)
        attr_list = [info_div.get_attribute_list('data-source')[0] for info_div in info_divs]
    except:
        attr_list = []
        print('No Attributes')
    print(attr_list)
    return attr_list


def get_infobox(game_soup):
    return game_soup.find('aside',{'class' : re.compile(r'^portable-infobox')})

def get_devs(game_infobox):
    
    try:
        dev_dets = game_infobox.find('div',{'data-source':'developer'})
        dev = dev_dets.find('a').get_attribute_list('title')[0]
    except:
        dev = np.NaN
        
    return dev

def get_publishers(game_infobox):
    try:
        publ_dets = game_infobox.find('div',{'data-source':'publisher'})
        publ = publ_dets.find('a').get_attribute_list('title')[0]
    except:
        publ = np.NaN
        
    return publ

def get_sales(game_infobox):
    
    try:
        sales_dets = game_infobox.find('div',{'data-source':'sales'})
        sales_val = sales_dets.find('div').text
    except:
        sales_val = np.NaN
    
    return sales_val

def get_size(game_infobox):
    
    try:
        size_dets = game_infobox.find('div',{'data-source':'size'})
        size_val = size_dets.find('div').text
    except:
        size_val = np.NaN
        
    return size_val

def get_platforms(game_infobox):
    
    try:
        platform_div = game_infobox.find('div',{'data-source':'system1'},recursive = False)
        platform_sub_secs = platform_div.find_all('a')
        platforms = [a.get_attribute_list('title')[0] for a in platform_sub_secs]
    except:
        platforms = np.NaN
        
    return platforms

def get_classifications(game_infobox):
    
    try:
        class_div = game_infobox.find('div',{'data-source':'class1'},recursive = False)
        class_subs = class_div.find_all('a')
        class_vals = [a.get_attribute_list('title')[0] for a in class_subs]
    except:
        class_vals = np.NaN
        
    return class_vals

def ger_genres(game_infobox):
    
    try:
        genre_div = game_infobox.find('div',{'data-source':'genre'},recursive = False)
        genre_l = [gen_val.find(text = True,recursive = False) for gen_val in genre_div.find_all()]
    except:
        genre_l = np.NaN
    
    return genre_l

def get_sections(game_infobox):
    
    try:
        sections = game_infobox.find_all('section',recursive = False)
    except:
        sections = np.NaN
    try:
        release_date_sec = sections[0]
    except:
        release_date_sec = np.NaN
    try:
        ratings_sec = sections[1]
    except:
        ratings_sec = np.NaN
    
    return release_date_sec,ratings_sec

def get_release_dates(release_date_sec):
    
    rdate_subsecs = release_date_sec.find_all('section',recursive = False)

    sub_sec_dates = {}
    for sub_sec in rdate_subsecs:
        sec_header = sub_sec.find('section',class_ = 'pi-smart-group-head').text.strip()
        sec_body = sub_sec.find('section',class_ = 'pi-smart-group-body')
        sec_date_list = sec_body.find_all('li')
        temp_dict = {}
        for sec_date in sec_date_list:
            loc = sec_date.find('a',class_ = 'image').get_attribute_list('title')[0]
            date_val = sec_date.text
            temp_dict[loc] = date_val
        sub_sec_dates[sec_header] = temp_dict
    
    return sub_sec_dates

def get_ratings(ratings_sec):
    
    rate_body = ratings_sec.find('tbody')
    rate_td = rate_body.find_all('td')
    rate_text_dict = {}
    rate_img_dict = {}
    for rate_src in rate_td:
        source = rate_src.get_attribute_list('data-source')[0]
        rate_txt = rate_src.find('a').get_attribute_list('title')[0]
        rate_img_val = rate_src.find('img').get_attribute_list('data-image-name')[0]
        rate_text_dict[source] = rate_txt
        rate_img_dict[source] = rate_img_val
    
    return rate_text_dict,rate_img_dict

def get_based_on(game_infobox):
    
    try:
        based_on_div = game_infobox.find('div',{'data-source':'based_on'},recursive = False)
        based_on_sub_div = based_on_div.find('div')
        based_ons = based_on_sub_div.text
    except:
        based_ons = np.NaN
        
    return based_ons

def get_firstgame(game_infobox):
    
    try:
        firstgame_div = game_infobox.find('div',{'data-source':'firstgame'},recursive = False)
        firstgame_sub_div = firstgame_div.find('div')
        firstgame = firstgame_sub_div.text
    except:
        firstgame = np.NaN
        
    return firstgame

def get_latest(game_infobox):
    
    try:
        latest_div = game_infobox.find('div',{'data-source':'latest'},recursive = False)
        latest_sub_div = latest_div.find('div')
        latest = latest_sub_div.text
    except:
        latest = np.NaN
        
    return latest

def get_details(game_soup):
    game_infobox = get_infobox(game_soup)
    
    try:
        game_attr = get_attribute_list(game_infobox)
    except:
        game_attr = np.NaN
    
    try:
        devs = get_devs(game_infobox)
    except:
        devs = np.NaN
    try:
        publs = get_publishers(game_infobox)
    except:
        publs = np.NaN
    try:
        sales = get_sales(game_infobox)
    except:
        sales = np.NaN
    try:
        size = get_size(game_infobox)
    except:
        size = np.NaN
    try:
        platforms = get_platforms(game_infobox)
    except:
        platforms = np.NaN
    try:
        classes = get_classifications(game_infobox)
    except:
        classes = np.NaN
    try:
        genres = ger_genres(game_infobox)
    except:
        genres = np.NaN
    
    try:
        release_date_sec,ratings_sec = get_sections(game_infobox)
    except:
        release_date_sec = np.NaN
        ratings_sec = np.NaN
    try:
        release_dates = get_release_dates(release_date_sec)
    except:
        release_dates = np.NaN
    try:
        ratings = get_ratings(ratings_sec)
    except:
        ratings = np.NaN
    try:
        based_on = get_based_on(game_infobox)
    except:
        based_on = np.NaN
        
    try:
        firstgame = get_firstgame(game_infobox)
    except:
        firstgame = np.NaN
        
    try:
        latest = get_latest(game_infobox)
    except:
        latest = np.NaN

    return devs,publs,sales,size,platforms,classes,genres,release_dates,ratings,game_attr,based_on,firstgame,latest

def gen_json(dict_var,file_name):
    
#     file_name = f'{dict_var=}'.split('=')[0]
    with open(file_name+'.json', 'w') as fp:
        print(os.getcwd())
        print(file_name+'.json')
        json.dump(dict_var, fp)
        
def get_json(dict_var):
    
    file_name = f'{dict_var=}'.split('=')[0]
    with open(file_name+'.json') as json_file: 
        return json.load(json_file)

# Base URL to which the game specific urls can be appended to get each games page
base_URL = 'https://nintendo.fandom.com'

list_of_games_URL = '/wiki/List_of_Nintendo_games'
URL = base_URL+list_of_games_URL

nintendo_page = get_html_content(URL)
page_content = nintendo_page.content
page_details(nintendo_page)
nin_soup = page_soup(nintendo_page)

# Getting the game list section of the page
game_list_section = nin_soup.find('div',class_ = 'mw-parser-output')

# The game list in this page are all listed under similar ul tags 
# as li tag elements with nothing differentiating them apart from the text value

# Getting all the ul elements
game_uls = game_list_section.find_all('ul',recursive = False)

game_year,game_url = get_game_NameYearURL(game_uls)

game_dev = {}
game_publs = {}
game_sales = {}
game_size = {}
game_platforms = {}
game_classes = {}
game_geners = {}
game_rdates = {}
game_ratings = {}
game_attr = {}
game_based_on = {}
game_firstgame = {}
game_latest = {}
for game in game_url:
    print('******************')
    print(game)
    if game_url[game] != None and game_url[game] == game_url[game] and 'https' not in game_url[game]:
        URL_game = base_URL + game_url[game]
        game_page = get_html_content(URL_game)
        page_content = game_page.content
        page_details(game_page)
        game_soup = page_soup(game_page)
        
        devs,publs,sales,size,platforms,classes,genres,release_dates,ratings,attributes,based_on,firstgame,latest = get_details(game_soup)
        
        print("Devs :",devs)
        print("Publishers :",publs)
        print("Sales :",sales)
        print("Size :",size)
        print("Platforms :",platforms)
        print("Classification(s) :",classes)
        print("Geners :",genres)
        print("Releases :",release_dates)
        print("Ratings :",ratings)
        print("Based On :",based_on)
        print("First Game :",firstgame)
        print("Latest :",latest)
        
        game_dev[game] = devs
        game_publs[game] = publs
        game_sales[game] = sales
        game_size[game] = size
        game_platforms[game] = platforms
        game_classes[game] = classes
        game_geners[game] = genres
        game_rdates[game] = release_dates
        game_ratings[game] = ratings
        game_attr[game] = attributes
        game_based_on[game] = based_on
        game_firstgame[game] = firstgame
        game_latest[game] = latest
    else:
        game_dev[game] = np.NaN
        game_publs[game] = np.NaN
        game_sales[game] = np.NaN
        game_size[game] = np.NaN
        game_platforms[game] = np.NaN
        game_classes[game] = np.NaN
        game_geners[game] = np.NaN
        game_rdates[game] = np.NaN
        game_ratings[game] = np.NaN
        game_attr[game] = np.NaN
        game_based_on[game] = np.NaN
        game_firstgame[game] = np.NaN
        game_latest[game] = np.NaN
        
script_dir = os.getcwd()
os.chdir("../Results/JSON")

gen_json(game_dev,'game_dev')
gen_json(game_publs,'game_publs')
gen_json(game_sales,'game_sales')
gen_json(game_size,'game_size')
gen_json(game_platforms,'game_platforms')
gen_json(game_classes,'game_classes')
gen_json(game_geners,'game_geners')
gen_json(game_rdates,'game_rdates')
gen_json(game_ratings,'game_ratings')
gen_json(game_attr,'game_attr')
gen_json(game_based_on,'game_based_on')
gen_json(game_firstgame,'game_firstgame')
gen_json(game_latest,'game_latest')

os.chdir(script_dir)