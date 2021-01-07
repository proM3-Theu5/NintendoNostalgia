# For Web Crawling and Scraping data
import requests
from bs4 import BeautifulSoup
import re
import logger as log

# For storing the retrieved data
import pandas as pd
import numpy as np

# Preliminary data storage
import json
import os

global_log_level = 'DEBUG'
file_path = "..\..\..\..\..\Logs\\"
filename = log.get_filename()

def get_html_content(URL):

    log.log_generate('ALL',global_log_level,'Getting HTML Content',file_path,filename)
    log.log_generate('ALL',global_log_level,'URL :'+str(URL),file_path,filename)
    web_page = requests.get(URL)
    return web_page

def page_details(web_page):

    log.log_generate('ALL',global_log_level,'Getting HHTP Page Request Details',file_path,filename)
    print('URL : '+web_page.url)
    print("Status Code : "+str(web_page.status_code))
    log.log_generate('DEBUG',global_log_level,"Status Code : "+str(web_page.status_code),file_path,filename)
    print("Encoding : "+web_page.encoding)
    log.log_generate('DEBUG',global_log_level,"Encoding : "+web_page.encoding,file_path,filename)
    

def page_soup(web_page):

    log.log_generate('ALL',global_log_level,'Getting WebPage Soup',file_path,filename)
    return BeautifulSoup(web_page.content, 'html.parser')

# Function to find all occurences of hyphen in text
def all_occurences(text,char):

    log.log_generate('ALL',global_log_level,'Fetching all occurrences of "'+char+'" in '+text,file_path,filename)
    occur = [i for i,char_s in enumerate(text) if char == char_s ]
    log.log_generate('DEBUG',global_log_level,'Occurences found : "'+str(occur),file_path,filename)
    return occur

def get_game_NameYearURL(game_uls):
    
    log.log_generate('ALL',global_log_level,'Getting Game Name, Year and URL',file_path,filename)
    # Generating details for all games
    log.log_generate('ALL',global_log_level,'Input : game_uls = '+str(game_uls),file_path,filename)
    game_year = {}
    game_url = {}
    for game_ul in game_uls:
        # log.log_generate('ALL',global_log_level,'In Loop : game_uls',file_path,filename)
        log.log_generate('DEBUG',global_log_level,'game_ul : '+str(game_ul),file_path,filename)
        game_li = game_ul.find_all('li')
        for game in game_li:
            log.log_generate('DEBUG',global_log_level,'game : '+str(game),file_path,filename)
            text = game.text
            hyph_places = all_occurences(text,"-")
            log.log_generate('DEBUG',global_log_level,'hyph_places : '+str(hyph_places),file_path,filename)
            if len(hyph_places) > 0:
                name = text[:hyph_places[-1]-1]
                year = text[hyph_places[-1]+2:]
                log.log_generate('DEBUG',global_log_level,'if - name : '+str(name),file_path,filename)
                log.log_generate('DEBUG',global_log_level,'if - year : '+str(year),file_path,filename)
            else:
                name = text[:-7]
                year = text[-5:]
                log.log_generate('DEBUG',global_log_level,'else - name : '+str(name),file_path,filename)
                log.log_generate('DEBUG',global_log_level,'else - year : '+str(year),file_path,filename)
            try :
                game_url[name] = game.find('a').get_attribute_list('href')[0]
                game_year[name] = year
            except:
                game_url[name] = np.NaN
                game_year[name] = np.NaN
            log.log_generate('DEBUG',global_log_level,'game_url : '+str(game_url[name]),file_path,filename)
            log.log_generate('DEBUG',global_log_level,'game_year : '+str(game_year[name]),file_path,filename)
                
    return game_year,game_url            
    
def get_attribute_list(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting attribute list for the game',file_path,filename)
    
    try:
        info_divs = game_infobox.find_all('div',recursive = False)
        attr_list = [info_div.get_attribute_list('data-source')[0] for info_div in info_divs]
    except:
        attr_list = []
        print('No Attributes')
    print(attr_list)
    return attr_list


def get_infobox(game_soup):
    log.log_generate('ALL',global_log_level,'Getting infobox for the game',file_path,filename)
    return game_soup.find('aside',{'class' : re.compile(r'^portable-infobox')})

def get_devs(game_infobox):
    
    log.log_generate('ALL',global_log_level,'Getting Developers for the game',file_path,filename)
    try:
        dev_dets = game_infobox.find('div',{'data-source':'developer'})
        dev = dev_dets.find('a').get_attribute_list('title')[0]
    except:
        dev = np.NaN
        
    return dev

def get_publishers(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting publishers for the game',file_path,filename)
    try:
        publ_dets = game_infobox.find('div',{'data-source':'publisher'})
        publ = publ_dets.find('a').get_attribute_list('title')[0]
    except:
        publ = np.NaN
        
    return publ

def get_sales(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting sales for the game',file_path,filename)
    
    try:
        sales_dets = game_infobox.find('div',{'data-source':'sales'})
        sales_val = sales_dets.find('div').text
    except:
        sales_val = np.NaN
    
    return sales_val

def get_size(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting size for the game',file_path,filename)
    
    try:
        size_dets = game_infobox.find('div',{'data-source':'size'})
        size_val = size_dets.find('div').text
    except:
        size_val = np.NaN
        
    return size_val

def get_platforms(game_infobox):
    
    log.log_generate('ALL',global_log_level,'Getting platforms for the game',file_path,filename)
    
    try:
        platform_div = game_infobox.find('div',{'data-source':'system1'},recursive = False)
        platform_sub_secs = platform_div.find_all('a')
        platforms = [a.get_attribute_list('title')[0] for a in platform_sub_secs]
    except:
        platforms = np.NaN
        
    return platforms

def get_classifications(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting classifications for the game',file_path,filename)
    
    try:
        class_div = game_infobox.find('div',{'data-source':'class1'},recursive = False)
        class_subs = class_div.find_all('a')
        class_vals = [a.get_attribute_list('title')[0] for a in class_subs]
    except:
        class_vals = np.NaN
        
    return class_vals

def ger_genres(game_infobox):
    
    log.log_generate('ALL',global_log_level,'Getting genres for the game',file_path,filename)

    try:
        genre_div = game_infobox.find('div',{'data-source':'genre'},recursive = False)
        genre_l = [gen_val.find(text = True,recursive = False) for gen_val in genre_div.find_all()]
    except:
        genre_l = np.NaN
    
    return genre_l

def get_sections(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting sections for the game',file_path,filename)
    
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

    log.log_generate('ALL',global_log_level,'Getting release dates for the game',file_path,filename)
    
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

    log.log_generate('ALL',global_log_level,'Getting classifications for the game',file_path,filename)
    
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

    log.log_generate('ALL',global_log_level,'Getting Based On for the game',file_path,filename)
    
    try:
        based_on_div = game_infobox.find('div',{'data-source':'based_on'},recursive = False)
        based_on_sub_div = based_on_div.find('div')
        based_ons = based_on_sub_div.text
    except:
        based_ons = np.NaN
        
    return based_ons

def get_firstgame(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting First Game for the game',file_path,filename)
    
    try:
        firstgame_div = game_infobox.find('div',{'data-source':'firstgame'},recursive = False)
        firstgame_sub_div = firstgame_div.find('div')
        firstgame = firstgame_sub_div.text
    except:
        firstgame = np.NaN
        
    return firstgame

def get_latest(game_infobox):

    log.log_generate('ALL',global_log_level,'Getting Latest for the game',file_path,filename)
    
    try:
        latest_div = game_infobox.find('div',{'data-source':'latest'},recursive = False)
        latest_sub_div = latest_div.find('div')
        latest = latest_sub_div.text
    except:
        latest = np.NaN
        
    return latest

def get_details(game_soup):

    log.log_generate('ALL',global_log_level,'Getting all details for the game',file_path,filename)

    game_infobox = get_infobox(game_soup)
    
    try:
        log.log_generate('ALL',global_log_level,'Attempting Attribute List for the game',file_path,filename)
        game_attr = get_attribute_list(game_infobox)
    except:
        game_attr = np.NaN
    
    try:
        log.log_generate('ALL',global_log_level,'Attempting Developers for the game',file_path,filename)
        devs = get_devs(game_infobox)
    except:
        devs = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Publishers for the game',file_path,filename)
        publs = get_publishers(game_infobox)
    except:
        publs = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Sales for the game',file_path,filename)
        sales = get_sales(game_infobox)
    except:
        sales = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Size for the game',file_path,filename)
        size = get_size(game_infobox)
    except:
        size = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Platform for the game',file_path,filename)
        platforms = get_platforms(game_infobox)
    except:
        platforms = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Classification for the game',file_path,filename)
        classes = get_classifications(game_infobox)
    except:
        classes = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Genre for the game',file_path,filename)
        genres = ger_genres(game_infobox)
    except:
        genres = np.NaN
    
    try:
        log.log_generate('ALL',global_log_level,'Attempting Release Date and Ratings sections for the game',file_path,filename)
        release_date_sec,ratings_sec = get_sections(game_infobox)
    except:
        release_date_sec = np.NaN
        ratings_sec = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Release Dates for the game',file_path,filename)
        release_dates = get_release_dates(release_date_sec)
    except:
        release_dates = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Ratings for the game',file_path,filename)
        ratings = get_ratings(ratings_sec)
    except:
        ratings = np.NaN
    try:
        log.log_generate('ALL',global_log_level,'Attempting Based On for the game',file_path,filename)
        based_on = get_based_on(game_infobox)
    except:
        based_on = np.NaN
        
    try:
        log.log_generate('ALL',global_log_level,'Attempting Firstgame for the game',file_path,filename)
        firstgame = get_firstgame(game_infobox)
    except:
        firstgame = np.NaN
        
    try:
        log.log_generate('ALL',global_log_level,'Attempting Latest for the game',file_path,filename)
        latest = get_latest(game_infobox)
    except:
        latest = np.NaN

    return devs,publs,sales,size,platforms,classes,genres,release_dates,ratings,game_attr,based_on,firstgame,latest

def gen_json(dict_var,file_name):
    
#     file_name = f'{dict_var=}'.split('=')[0]
    # log.log_generate('ALL',global_log_level,'Generating JSON for'+str(file_name),file_path,filename)
    with open(file_name+'.json', 'w') as fp:
        print(os.getcwd())
        print(file_name+'.json')
        json.dump(dict_var, fp)
        
def get_json(dict_var):
    
    # log.log_generate('ALL',global_log_level,'Fetching JSON into dict',file_path,filename)
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

game_year,game_url = get_game_NameYearURL(game_uls[:5])

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
    log.log_generate('DEBUG',global_log_level,'************************************',file_path,filename)
    print(game)
    log.log_generate('DEBUG',global_log_level,'GAME :'+str(game),file_path,filename)
    if game_url[game] != None and game_url[game] == game_url[game] and 'https' not in game_url[game]:
        URL_game = base_URL + game_url[game]
        game_page = get_html_content(URL_game)
        page_content = game_page.content
        page_details(game_page)
        game_soup = page_soup(game_page)
        
        devs,publs,sales,size,platforms,classes,genres,release_dates,ratings,attributes,based_on,firstgame,latest = get_details(game_soup)
        
        log.log_generate('DEBUG',global_log_level,"Devs :"+str(devs),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Publishers :"+str(publs),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Sales :"+str(sales),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Size :"+str(size),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Platforms :"+str(platforms),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Classification(s) :"+str(classes),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Geners :"+str(genres),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Releases :"+str(release_dates),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Ratings :"+str(ratings),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Based On :"+str(based_on),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"First Game :"+str(firstgame),file_path,filename)
        log.log_generate('DEBUG',global_log_level,"Latest :"+str(latest),file_path,filename)
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