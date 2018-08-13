# -*- coding: utf-8 -*-
"""
@author: Kip Badgery
"""
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from chatterbot import ChatBot

# Importing the training data
dataset = pd.read_csv('chatbot_trainer.csv')
training_data = dataset.iloc[:,:].values

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer',
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.6,
            'default_response': 'I am sorry, I am unable to help with that.'
        }]
)

for i in range (0,len(training_data)): # loop through all of the conversations in the training document
    nb_nan = np.count_nonzero(pd.isnull(training_data[i,:])) #counting the number of Nans in row so we don't train with these
    train_array=training_data[i,:-nb_nan] #create temporary train_array variable that can be used using chatbot.train
    chatbot.train(train_array) # train the chatbot using the current conversation row

bot_name='Kip:'
# Get a response to the input text
print(bot_name,'Hello, is there anything I can help you with?') 

while True:
    request = input("You: ")
    response = chatbot.get_response(request)
    
    print(bot_name, response)
    print(bot_name, 'Was I able to help?')
    while True: # check to see if you were able to help with issue
        help_response = input("You:")
        if "yes" in help_response.lower(): 
            print(bot_name, "Glad I could help. ") 
            #chatbot.learn_response(response,response) #because you were able to help, the chatbot learns that the response was appropriate for the initial question
            break
        elif "no" in help_response.lower():
            print(bot_name, "Sorry about that, please take a look at our FAQ's, reach out to us at info@hr.com or try rewording the question. ")
            break
        else:
            print(bot_name, "I'm sorry, I don't understand. Please respond with yes or no.")
            
    print(bot_name, "Please let me know if there is anything else I can help you with.")
    