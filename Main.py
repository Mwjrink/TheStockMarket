import time, sys
# from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
# from datetime import datetime
import re
# import sqlite3
import csv
# import pandas
import pymysql
# import sqlalchemy
import PriceScraper, Stock, PressReleaseScraper


def internet_on():
    try:
        urlopen('https://www.google.com', timeout=1)
        return False
    except URLError as err: 
        return True

print("Hello")
print("Let's get started")

if(internet_on()):
    print("no internet :(")
    # sys.exit


csv_file = urlretrieve("http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download", "NASDAQlist.csv")
csv_file = urlretrieve("http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download", "AMEXlist.csv")
csv_file = urlretrieve("http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download", "NYSElist.csv")

NASDAQtable = []
NYSEtable = []
AMEXtable = []


# print(table[2:200])

#load into MySQL server

NASDAQdb = pymysql.connect(
                    host="localhost",
                    user="NASDAQ",
                    passwd='''OC\PSRI2a/@=@=6]-ICNt.;D$-[!nCC@''',
                    port=3306,
                    db='NASDAQ',
                    autocommit=True
                    )

NYSEdb = pymysql.connect(
                    host="localhost",
                    user="NYSE",
                    passwd='''FX3M{['(7Gx[TQCY^k6I+=DSp+exC|f''',
                    port=3306,
                    db='NYSE',
                    autocommit=True
                    ) 

AMEXdb = pymysql.connect(
                    host="localhost",
                    user="AMEX",
                    passwd='''SW4`Oq@v&g{1G>?uZj?*hQ&zn<(9Kpd&''',
                    port=3306,
                    db='AMEX',
                    autocommit=True
                    ) 


# .connect(   host='localhost',
#             user='user',
#             password='passwd',
#             db='db',
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )

NASDAQcur = NASDAQdb.cursor()
NYSEcur = NYSEdb.cursor()
AMEXcur = AMEXdb.cursor()



NASDAQcur.execute('''drop table if exists NASDAQ''')
NYSEcur.execute('''drop table if exists NYSE''')
AMEXcur.execute('''drop table if exists AMEX''')

# NASDAQcur.execute('''drop table if exists NEWNASDAQ''')

NASDAQcur.execute('''CREATE TABLE NASDAQ(
    Symbol varchar(4), 
    Name varchar(256), 
    LastSale int, 
    MarketCap int, 
    ADRTSO varchar(256), 
    IPOyear varchar(4), 
    Sector varchar(256), 
    Industry varchar(256), 
    SummaryQuote varchar(256))
    ''')
NYSEcur.execute('''CREATE TABLE NYSE(Symbol varchar(4), Name varchar(256), LastSale decimal(13,2), MarketCap decimal(16,2), ADRTSO varchar(256), IPOyear varchar(4), Sector varchar(256), Industry varchar(256), SummaryQuote varchar(256))''')
AMEXcur.execute('''CREATE TABLE AMEX(Symbol varchar(4), Name varchar(256), LastSale decimal(13,2), MarketCap decimal(16,2), ADRTSO varchar(256), IPOyear varchar(4), Sector varchar(256), Industry varchar(256), SummaryQuote varchar(256))''')


# print(NASDAQcur.execute('''show tables'''))
# print(NYSEcur.execute('''show tables'''))
# print(AMEXcur.execute('''show tables'''))
# print("(\"" + NASDAQtable[1][0] + "\", \"" + NASDAQtable[1][1] + "\", " + NASDAQtable[1][2] + ", " + NASDAQtable[1][3] + ", \"" + NASDAQtable[1][4] + "\", \"" + NASDAQtable[1][5] + "\", \"" + NASDAQtable[1][6] + "\", \"" + NASDAQtable[1][7] + "\", \"" + NASDAQtable[1][8] + "\"" + "))")

# print(NASDAQcur.execute('''
# SELECT * 
# FROM NASDAQ
# '''))
count = 0
with open('NASDAQlist.csv', 'rt') as csvfile:
    NASCSV = csv.reader((line.replace('","', '|').replace('",', '').replace('"', '').replace('n/a', '-1').replace(" ", "_") for line in csvfile), delimiter='|', quotechar='|')
    for row in NASCSV:
        if(count is 0):
            count += 1
            continue
        # if(count < 5):
        #     # print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        #     print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(*row))
        #     count += 1
        # NASDAQcur.execute('INSERT INTO NASDAQ VALUES (' + '''"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8][29:]) + ')')
        # print(row[3])
        print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(*row))
        NASDAQcur.execute('INSERT INTO NASDAQ VALUES (' + '''"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'''.format(*row) + ')')
        print(NASDAQcur.execute('''SELECT MarketCap FROM NASDAQ LIMIT ''' + str(count-1) + ''',1;'''))
        # del row[4]
        # del row[4]
        # del row[6]
        count+=1
        NASDAQtable.append(row)

with open('AMEXlist.csv', 'rt') as csvfile:
    spamreader = csv.reader((line.replace('","', '|').replace('",', '').replace('"', '') for line in csvfile), delimiter='|', quotechar='|')
    for row in spamreader:
        # del row[4]
        # del row[4]
        # del row[6]
        NYSEtable.append(row)

with open('NYSElist.csv', 'rt') as csvfile:
    spamreader = csv.reader((line.replace('","', '|').replace('",', '').replace('"', '') for line in csvfile), delimiter='|', quotechar='|')
    for row in spamreader:
        # del row[4]
        # del row[4]
        # del row[6]
        AMEXtable.append(row)


# NASDAQcur.execute('''
#     INSERT INTO NASDAQ 
#     VALUES (''' "" + NASDAQtable[1][0] + ",2,3,4,5,6,7,8,9)")

# NASDAQcur.execute('''
#     INSERT INTO NASDAQ 
#     VALUES ('''
#     "(\"" + NASDAQtable[1][0] + '''\", 
#     \"''' + NASDAQtable[1][1] + '''\", 
#     ''' + NASDAQtable[1][2] + ''', 
#     ''' + NASDAQtable[1][3] + ''', 
#     \"''' + NASDAQtable[1][4] + '''\", 
#     \"''' + NASDAQtable[1][5] + '''\", 
#     \"''' + NASDAQtable[1][6] + '''\", 
#     \"''' + NASDAQtable[1][7] + '''\", 
#     \"''' + NASDAQtable[1][8] + "\""
#      + "))")



# print(NASDAQcur.execute('''SELECT LastSale FROM NASDAQ WHERE Symbol = PIH'''))


# sql = '''INSERT INTO addresses (name, street, zipcode, city, state) VALUES (%s, %s, %s, %s, %s)'''
# data = sum([zip(*x) for x in k1], [])
# cursor.executemany(sql, data)


print("done")

# NASDAQengine = sqlalchemy.create_engine("postgres://postgres@/postgres")
# NYSEengine = sqlalchemy.create_engine("postgres://postgres@/postgres")
# AMEXengine = sqlalchemy.create_engine("postgres://postgres@/postgres")

# NASDAQconn = NASDAQengine.connect()
# NYSEconn = NYSEengine.connect()
# AMEXconn = AMEXengine.connect()

# NASDAQconn.execute("commit")
# NYSEconn.execute("commit")
# AMEXconn.execute("commit")

# NASDAQcur.execute("create database NASDAQ")
# NYSEcur.execute("create database NYSE")
# AMEXcur.execute("create database AMEX")

# NASDAQcur = NASDAQconn.cursor()

# conn.close()

# "Symbol" : str
# "Name" : str
# "LastSale" : int
# "MarketCap" : int
# "ADR TSO" : str
# "IPOyear" : str
# "Sector" : str
# "Industry" : str
# "Summary Quote" : str


#0: Symbol
#1: Name
#2: LastSale
#3: MarketCap
#4: Sector
#5: Industry
#6: Summary Quote




# soup = PriceScraper.retrieveHTML("http://www.nasdaq.com/markets/most-active.aspx")

# for i in range(amnt):
#     # link = soup.find('a', attrs={'id': 'two_column_main_content_MostActiveByShareVolume_tickerwidget_MostActiveByShareVolume_' + str(i) + '_summaryquotes_' + str(i)})
#     link = soup.find('a', attrs={'href': 'http://www.nasdaq.com/symbol/'})
#     symbols.append(link.text.strip())
# name_elements = soup.find_all('a', attrs={'class': 'mostactive'})

# symbols = [i.text.strip() for i in soup.find_all('a', attrs={'href': re.compile('http://www.nasdaq.com/symbol/'), 'id': re.compile('two_column_main_content')})]
# names = [i.text.strip() for i in soup.find_all('a', attrs={'class': 'mostactive'})]

# most_recent_prices = [i.text.strip() for i in [a if a.test.strip().startswith("$") for a in soup.find_all('td')]


# print(symbols)
# print(names)
# print(most_recent_prices)