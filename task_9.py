from os import listdir
from random import randrange
import  requests,json,time
from bs4 import BeautifulSoup as soupUse 

oldlist,c,l,url=[],0,[],'https://www.imdb.com/chart/top/'
print('loaging....')
data_list_123=listdir('data')
p = requests.get(url)
s = soupUse(p.content,'lxml')


def scrape_movie_details(link):
  global c
  zm2 = link[-10:-1:1]+'.json'
  c+=1
  movie={}
  if zm2 not in data_list_123:
    print('loading.......')
    p=randrange(1,6)
    time.sleep(randrange(p))
    page=requests.get(link)
    soup=soupUse(page.content,'lxml')
    movie['title'] = soup.title.text
    movie['link'] = link
    bio = soup.find('div' ,class_ = "sc-16ede01-9 bbiYSi sc-910a7330-11 GYbFb").text
    rating = soup.find('div', class_ = "sc-7ab21ed2-2 kYEdvH").text
    director = soup.find('a', class_ = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
    storyline = soup.find('div',class_ = "ipc-html-content-inner-div").text
    release_data = soup.find('li', class_ = "ipc-inline-list__item").text[0:4]
    ad=soup.find('span', class_ = "ipc-metadata-list-item__list-content-item").text  
    more=soup.find_all('section',class_ = "ipc-page-section ipc-page-section--base celwidget" )
    cny = soup.find('li',attrs = {'data-testid' : "title-details-origin"}).text
    lng = soup.find('li',attrs = {'data-testid' : "title-details-languages"}).text
    pag = soup.find_all('a')

    str_Genres=' '
    for i in pag:
      if 'Action' == i.text or 'Drama' == i.text or 'Crime' == i.text:str_Genres = str_Genres+ i.text
    ee = lng.find('es')
    if ee > 1:res2 = ee+1
    else:
      res2=lng.index('e')
    fl = soup.find('li',attrs={'data-testid':"title-details-companies"}).text
    rt = soup.find('li', attrs={'data-testid':"title-techspec_runtime"}).text
    newstring = ''.join([i for i in rt if not i.isalpha()])
    s = int(newstring[0])*60
    re = int(newstring[1:])+int(s)
    e = fl.find('companies')
    if e > 4:
      res = e
    else:
      res = fl.find('company')

    movie['position'] = c
    movie['bio'] = bio
    movie['rating'] = rating
    movie['director'] = director
    movie['storyline'] = storyline
    movie['release_date'] = release_data
    movie['awards'] = ad
    movie['Country of origin'] = cny[17:]
    movie['Language'] = lng[res2+1:]
    movie['Production company'] = fl[res:]
    movie['runtime'] = str(re)+' '+'min'
    movie['Genres'] = str_Genres
    movie['Certificate'] = pag[51].text
    zm = link[-10:-1:1]

    print('this is from the database')

    with open(f'data/{zm}.json','w') as file:json.dump(movie,file,indent = 3)
  else:
    with open(f'data/{zm2}') as file:
      print(json.load(file))


def scrape_top_list():
  li = [em  for em  in  s.find_all('td', class_ = "titleColumn")]
  c = 1
  for ele in li:
    c += 1
    lin = 'https://www.imdb.com' + ele.find('a').attrs['href']
    scrape_movie_details(lin)
scrape_top_list()

