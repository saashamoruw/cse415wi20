'''saashm_agent.py.
CSE 415, Winter 2020, Assignment 1
Saasha Mor 
'''
import chatbot

'''... code defining rules etc.'''
you_me = {'I':'you', 'me':'you','you':'me','am':'are', 'mine':'yours','my':'your','yours':'mine','your':'my'}
prompt = '''Say "I like books" if you want to know about resources for books 
Say "I like websites" if you wan to learn about websites you can learn from 
You can also talk about which aspects of data science you like for example, data visualization, analysis,
databases etc. Type "roles" if you want to see which roles you might be in as a data enthusiast.
Say "author" if you want to know more about the author of this chatbot
Say "?" if you don't know what to say
Say "Bye" if you want to exit'''

intro_string = '''My name is DS Genius Bot. The DS in my name stands for Data Science!
 I was designed by Saasha Mor a Informatics major in college and she has a keen interest in Data Science.
 If you don't like the way I assist you today, contact here at saashm@uwedu.
 How can I help you? \n''' + prompt
 

my_rules = [
    (r"(hi|hello|hey|whatsup|greetings)", ["'sup bro", "hey", "*nods*", "Wazzzaaaa"]), 
    # 1
    # The above rule catches user inputs for the form "Hi what can you do"
    # There are four response patterns for differnt kinds of greetings 
    (r"you want to know about (.*)", ["What do you want to know about $1$?",
     "That's great initiative, what can I tell you about?"]),
    # 2
    # The above rule catches user inputs for the form "I like data science."
    # There are two response patterns.
    # (r"", [prompt]),
    (r"you like books", ["You might like The Drunkard’s Walk, book by Leonard Mlodinow",
     "You might like Machine Learning Course, Created by Stanford University and taught by Dr. Andrew Ng",
     "You might like Introduction to Mathematical Thinking, also by Stanford and taught by Dr. Keith Devlin"]),
     # 3
     # The above rule catches user inputs for the form "I like books about data science"
     # There are three possible responses of books they might like
     (r"(.*) websites", ["You might want to checkout Kaggle", "You might like Freebase"]),
     # 4
     # The above rule catches user inputs for the form "I like websites to learn about data science"
     # There are two possible responses of websites they might use
     (r"(.*) (visualization|visualizations)", ["What kind of charts do you like?", "What are your favorite colors?"]),
     # 5
     # The above rule catches user inputs for the form "Tell me about data visualization stuff" or any
     # thing that has the phrase data visualization
     # There are two possible responses to inquire more about the topic
     (r"(.*) analysis", ["What do you want to analyze?", "What do you like about it?"]),
     # 6
     # The above rule catches user inputs for the form "Tell me about data analysis stuff" or any
     # thing that has the phrase data analysis
     # There are two possible responses to inquire more about the topic
     (r"(.*) (databases|database)", ["Do you want to create a database?", "Which database do you want to look for?"]),
     # 7
     # The above rule catches user inputs for the form "Tell me about databases stuff" or any
     # thing that has the phrase databases
     # There are two possible responses to inquire more about the topic
     (r"(.*) (roles|role) (.*)", ["You can be whatever you want to be!"]),
     # 8
     # The above rule catches user inputs for the form "Tell me about the roles"  or any
     # thing that has the phrase roles
     # There are two possible responses
     (r"(.*) (author|authors)", ["Hit me up at saashm@uw.edu", "Her name is Saasha Mor!"]),
     # 9
     # The above rule catches user inputs for the form "Tell me about the author"
     # There are two possible responses
     (r"\?", [prompt]),
     # 10
     # This prompts the user about what they could ask the chat bot
     (r"", ["That's great! Say ? if you want to know how I can help you"])
     # 11
     # This rule catches all other inputs .
]

SaashasAgent = chatbot.chatbot(my_rules, you_me, "Saasha-bot", intro_string)

if __name__=="__main__":
    SaashasAgent.chat()