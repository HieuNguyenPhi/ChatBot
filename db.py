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
conn.commit()
result = cursor.execute('SELECT * FROM Bank;')
result.fetchall()
# conn.close()
query = 'SELECT TimeStamp, Type, Amount, Location, Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 5'
cursor.execute(query)
results = cursor.fetchall()
balance = results[0][4]
print("Bot: Your current account balance is USD {}".format(balance))
print("Bot: Here is your latest 5 transactions:")
print("{:<20s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}".format("Date", "Type", "Amount", "Location", "Balance"))
for i in range(len(results)):
    print("{:<20s}\t{:<10s}\t{:<10s}\t{:<10s}\t{:<10s}".format(str(results[i][0]),str(results[i][1]),str(results[i][2]),str(results[i][3]),str(results[i][4])))

query = 'SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1'
cursor.execute(query)
response = ['Your balance is USD {}', "Oh! You have USD {} in your account", "You can use USD {} at the moment"]
results = cursor.fetchall()
print('Bot: ' + random.choice(response).format(list(*results)[0]))
conn.close()