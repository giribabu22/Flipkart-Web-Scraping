from os import listdir
import requests,json
from bs4 import BeautifulSoup

pn = '/search?q=smartphone&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_5_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_5_na_na_na&as-pos=3&as-type=RECENT&suggestionId=smartphone&requestId=892c2da5-bc52-4313-9f31-86ddbc7fb84b&as-searchtext=smart'
print('loading......')
link = '/search?q=smartphone&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_5_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_5_na_na_na&as-pos=3&as-type=RECENT&suggestionId=smartphone&requestId=892c2da5-bc52-4313-9f31-86ddbc7fb84b&as-searchtext=7&page='
link_,un,main_li= [],1,[]

for c in range(1,11):
  ml = link+str(c)
  link_.append(ml)

data = requests.get(f'https://www.flipkart.com{pn}').text
soup = BeautifulSoup(data,'lxml')

def next_link():
  global soup,pn,un
  pn=link_[un]
  print('\n \t loading.........')
  un+=1
  call_url()

def call_url():
  global main_li
  dl = listdir()
  if 'data_flipkart.json' in dl:
      with open('data_flipkart.json') as f :
        main_li = json.load(f)
  else:
    with open('data_flipkart.json','w') as f :
      json.dump(main_li,f,indent=3)
  lo = ['ROM','Display','Camera','Battery','Processor','more']
  data = requests.get(f'https://www.flipkart.com{pn}').text
  soup = BeautifulSoup(data,'lxml')
  r = soup.find_all('div',class_="_30jeq3 _1_WHN1")
  rev = soup.find_all('div',class_="_3LWZlK")
  lo ,pp= ['ROM','Display','Camera','Battery','Processor','more'],0
  
  for l in soup.find_all('div',class_ ='_3pLy-c row'):
    tit = l.find('div',class_="_4rR01T")
    c,d=0,{}
    hol = l.ul
    lz = str(hol).split('>')
    res2=rev[pp].text
    res=r[pp].text
    d['Name']=tit.text
    d['prise'] = res[1:]
    d['Rating'] = res2
    pp+=1
    for i in lz:
      rem = i.split('<')
      if c < len(lo):
        if 'class' not in i or '' not in i :
          d[lo[c]] = rem[0]
          c+=1
    main_li.append(d)
  with open('data_flipkart.json','w') as file:
    json.dump(main_li,file,indent=4)
  c = input('if you want next page scraping data y/n: ')
  if c =='y':
    next_link()
call_url()
