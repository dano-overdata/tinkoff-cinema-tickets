import requests
from bs4 import BeautifulSoup
from datetime import *
import calendar
import pandas as pd
from tqdm import tqdm


first_film_on_page = 1
df = pd.DataFrame(columns=['Film_id', 'Name', 'Country', 'Year', 'Month', 'Day', 'Show_type'])
row_index = 0


while first_film_on_page < 10507:
    parse_link = f'https://www.imdb.com/search/title/?title_type=feature&year=2020-01-01,2020-12-31&start={first_film_on_page}&ref_=adv_nxt'
    responce = requests.get(url=parse_link)
    soup = BeautifulSoup(responce.text, 'html.parser')
    fid = soup.findAll('h3', class_='lister-item-header')

    try:
        for film_id in tqdm(range(len(fid))):
            data = fid[film_id].find('a')
            film_name = data.text
            id = data['href'].split('/')[2]
            url = f'https://s.media-imdb.com/title/{id}/releaseinfo?ref_=tt_ov_rdat'
            responce1 = requests.get(url=url)
            soup1 = BeautifulSoup(responce1.text, 'html.parser')
            fid1 = soup1.findAll('tr',class_='ipl-zebra-list__item release-date-item')

            for country_id in range(len(fid1)):
                try:
                    lines = fid1[country_id].text.splitlines()
                    country_name = lines[1]
                    date = lines[3].split()
                    show_type = ['', '(' + lines[3].split('(')[-1]]['(' in lines[3]]
                    
                    if len(date) >= 3:
                        df.loc[row_index] = [first_film_on_page + film_id, film_name, country_name, date[2], date[1],
                                         date[0], show_type]
                    row_index += 1

                except IndexError as ex:
                    print(ex)
                    pass

    except IndexError as ex:
        print(ex)

    first_film_on_page += 50
    print(f"Processed {first_film_on_page - 1} films")
    df.to_csv('imdb_release_dates.csv')
    
