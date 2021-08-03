import sqlite3

createTbl = '''
CREATE TABLE Bank (
    ID VARCHAR2(3) PRIMARY KEY,
    TimeStamp DATETIME,
    Type VARCHAR2(10),
    Amount NUMBER(10),
    Location VARCHAR2(5),
    Balance NUMBER(10)
);
'''

conn = sqlite3.connect('db.db')
cursor = conn.cursor()

cursor.execute(createTbl)

populate = '''
INSERT INTO Bank VALUES (?,?,?,?,?,?);
'''

with open('sample.txt', 'r') as file:
    sample = file.readlines()
    for line in sample:
        items = line.split(', ')
        cursor.execute(populate, (items[0],items[1],items[2],items[3], items[4], items[5]))

result = cursor.execute('SELECT * FROM Bank;')
result.fetchall()
conn.close()