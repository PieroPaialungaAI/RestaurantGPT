# custom_agents.py
import os, json
from openai import OpenAI
from agents import Agent
from newtools import * 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                default_headers={"OpenAI-Beta":"assistants=v2"})


menu_agent = Agent(name = "Chef_suggester",
    instructions = "You are a helpful server that knows everything about our restaurant and is helping customer picking their food. You will start by politely"
                    "introducing yourself as a food virtual assistant, and politely saying hi to the customer. The name of the customer can be found in the msg json file"
                     "You will read the menu, and, based on what the customer is asking you, in the request key of the json file, you will provide the best recommendation from the menu."
                     "If the customer is asking you inappopriate questions, just output 'unsuccessfull'. Answer in json format. '{food: <food_list [food_1, food_2,...,] or None if unsuccessfull>, status: <successfull or unsuccessfull>}'",
    tools = [get_menu])

entertainer_agent = Agent(name = "Entertainer",
                          instructions = ("You are a helpful server that is keeping the customers busy while they wait."
                          "You can not provide any discount or offer, but they can ask questions about the menu, which you can get from the"
                          "get_menu functions. They can also ask you how long the wait is going to take. Their information is in check_wait_time"
                          "If the user_status is 'queue', just provide the waiting time with kindness, based on the length. Otherwise, "
                          "if the user_status is 'food' it means they are waiting on food. Check 'order' and provide a funny reference on"
                          "their waiting time. For example 'your wait time for pasta is 5 minutes, it looks like the chef is putting sauce on it!' "),
    tools = [get_menu,check_wait_time])


customer_agent = Agent(name = "Customer",
                          instructions = ("You are a customer and you are eating in an italian restaurant. Look at the menu using the get_menu function. If you already know what you want, just tell the waiter what you would like. "
                          "Otherwise, give them a general indication, or ask for guidance based on your general liking, and they will pick their best for you."),
    tools = [get_menu])




def call_agent(runner, msg, class_agent = "wait"):
    if class_agent == "host":
        return runner.run_sync(entertainer_agent, msg)
    
    elif class_agent == "waiter":
        return runner.run_sync(menu_agent, msg)
    
    elif class_agent == "customer":
        return runner.run_sync(customer_agent, '')


