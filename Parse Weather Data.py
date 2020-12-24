import requests
from bs4 import BeautifulSoup
import pandas as pd

month = 12
year = 2018
yrct = 2014
mtctstr = '2014'
yrctstr = '1'

def get_data(url):

    html = requests.get(url).content

    soup = BeautifulSoup(html,'html.parser')

    soup.find_all('tr')
    tr_list = soup.find_all('tr')

    locations, precipitations = [], []
    loc = str
    global mtct,yrct,mtctstr,yrctstr



    for data in tr_list[2:]:
        sub_data = data.text.split()
        if len(sub_data) >= 2 :
            if (sub_data[1].startswith('Karjääri') or sub_data [1].startswith('SMJ')) and len(sub_data) >= 3 :
                loc = sub_data[0] + ' ' + sub_data[1]
                locations.append(loc)
                precipitations.append(sub_data[2])
            elif (sub_data[1].startswith('Karjääri') or sub_data [1].startswith('SMJ')) and len(sub_data) < 3 :
                loc = sub_data[0] + ' ' + sub_data[1]
                locations.append(loc)
                precipitations.append(0)
            else:
                locations.append(sub_data[0])
                precipitations.append(sub_data[1])
        else :
            locations.append(sub_data[0])
            precipitations.append(0)

    _data = pd.DataFrame()
    _data['Location'] = locations
    _data['Precipitation'] = precipitations

    return _data

u = 'http://www.ilmateenistus.ee/ilm/ilmavaatlused/sademed/sademete-kuu-summad/?lang=en&filter%5Byear%5D=' + yrctstr + '&filter%5Bmonth%5D=' + mtctstr

mtctstr = str(1)
data = get_data(u)

for i in range (60) :

    if i == 0:
        continue

    if i % 12 == 0:
        yrct = yrct + 1

    mtct = (i % 12) + 1
    mtctstr = str(mtct)
    yrctstr = str(yrct)
    print(yrctstr + "          " + mtctstr)
    print(data)
    u = 'http://www.ilmateenistus.ee/ilm/ilmavaatlused/sademed/sademete-kuu-summad/?lang=en&filter%5Byear%5D=' + yrctstr + '&filter%5Bmonth%5D=' + mtctstr
    tmp = get_data(u)
    data = pd.concat([data,tmp],axis=1).reset_index(drop=True)


data.to_csv('EsPre', index=False, encoding = 'utf-8')
