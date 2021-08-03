import spacy
import json

import random
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer

import sqlite3
import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load('en')

def train():
    pipeline = 'tensorflow_embedding'
    args = {"pipeline": pipeline}
    config = RasaNLUModelConfig(args)
    trainer = Trainer(config)

    training_data = load_data('train_data.json')
    interpreter = trainer.train(training_data)
    return interpreter

interpreter = train()

conn = sqlite3.connect('db.db')
cursor = conn.cursor()

def response(message):
    data = interpreter.parse(message)
    if (len(data['entities']) == 0):
        Class = data['intent']['name']
        if Class == 'check_balance':
            query = 'SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1'
            cursor.execute(query)
            response = ['Your balance is USD {}', "Oh! You have USD {} in your account", "You can use USD {} at the moment"]
            results = cursor.fetchall()
            print('Bot: ' + random.choice(response).format(list(*results)[0]))
        
        if Class == 'account_information':
            pass

        if Class == 'account_statement':
            query = 'SELECT TimeStampt, Type, Amount, Location, Balance FROM Bank ORDER BY TimeStampt DESC LIMIT 5'
            cursor.execute(query)
            results = cursor.fetchall()
            balance = results[0][4]
            print("Bot: Your current account balance is USD {}".format(balance))
            print("Bot: Here is your latest 5 transactions:")
            print("Date", "Type", "Amount", "Location", "Balance", sep="\t")
            for i in range(len(results)):
                # lsts = [results[i][0],results[i][1],results[i][2],results[i][3],results[i][4]]
                # lsts = '\t'.join(str(lst) for lst in lsts) 
                # print(lst)
                print("{:<15s}\t{:<10s}\t{:<10s}\t{:<5s}\t{:<10s}".format(results[i][0],results[i][1],results[i][2],results[i][3],results[i][4]))
        
        if Class == 'greet':
            response = ["Hello!", "Good to see you again!", "Hi there!"]
            print("Bot: " + random.choice(response))

        if Class == 'auto_bot':
            response = ["My name is Jarvis!", "You can call me Javis", "Jarvis, your assistant!"]
            print("Bot: " + random.choice(response))
        
        if Class == 'work_bot':
            response = ["I'm here to help you", "I can fetch your account detail"]
            print("Bot: " + random.choice(response))

    else:
        dic = data['entities'][0]
        if dic['confidence'] < 0.5:
            print("Bot: Sorry, I didn't understand your question :((")
        else:
            Class = dic['entity']
            if Class == 'money':
                query = 'SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1'
                cursor.execute(query)
                response = ['Your balance is USD {}', "Oh! You have USD {} in your account", "You can use USD {} at the moment"]
                results = cursor.fetchall()
                print('Bot: ' + random.choice(response).format(list(*results)[0]))
            
            elif Class == 'statement':
                query = 'SELECT TimeStampt, Type, Amount, Location, Balance FROM Bank ORDER BY TimeStampt DESC LIMIT 5'
                cursor.execute(query)
                results = cursor.fetchall()
                balance = results[0][4]
                print("Bot: Your current account balance is USD {}".format(balance))
                print("Bot: Here is your latest 5 transactions:")
                print("Date", "Type", "Amount", "Location", "Balance", sep="\t")
                for i in range(len(results)):
                    # lsts = [results[i][0],results[i][1],results[i][2],results[i][3],results[i][4]]
                    # lsts = '\t'.join(str(lst) for lst in lsts) 
                    # print(lst)
                    print("{:<15s}\t{:<10s}\t{:<10s}\t{:<5s}\t{:<10s}".format(results[i][0],results[i][1],results[i][2],results[i][3],results[i][4]))
            
            elif Class == 'greet':
                response = ["Hello!", "Good to see you again!", "Hi there!"]
                print("Bot: " + random.choice(response))

            elif Class == 'auto_bot':
                response = ["My name is Jarvis!", "You can call me Javis", "Jarvis, your assistant!"]
                print("Bot: " + random.choice(response))
            
            elif Class == 'work_bot':
                response = ["I'm here to help you", "I can fetch your account detail"]
                print("Bot: " + random.choice(response))
            
            else:
                response = ["I didn't understand your question :((", "I don't know the answer for this :("]
                print("Bot: Sorry, "+ random.choice(response))

while True:
    message = unicode("User: " + str(raw_input()), "utf-8")
    if message in [unicode("User: Thank you", "utf-8"), unicode("User: Thanks", "utf-8"), unicode("User: thank you", "utf-8"), unicode("User: thanks", "utf-8")]:
        print("Bot: Welcome! I am here to help you any time")
        break
    response(message)