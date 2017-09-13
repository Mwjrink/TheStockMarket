with open('NASDAQlist.csv', 'r') as csvfile:
	content = csvfile.read(2500).replace('"', '')
	rows = content.split("\n")
	cells = []
	for i in rows:
		cells.append(i.split(','))
	print(cells)
	print("\n\n\n ok")
	print(cells[0][9])

'''

import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='mydb')
cursor = mydb.cursor()

csv_data = csv.reader(file('students.csv'))
for row in csv_data:

    cursor.execute('INSERT INTO testcsv(names, \
          classes, mark )' \
          'VALUES("%s", "%s", "%s")', 
          row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"


'''