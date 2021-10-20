# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


# importing default libraries for rasa
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

import re

class Actioncoronastats(Action):

    '''
        This class defines the action of 
        displaying statistics after picking the
        intent from user's message
    '''

    def name(self) -> Text:

        '''          
            method to define the name
            of this action
        '''
    
        return "actions_corona_state_stat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''
            this method contains the working i.e., : 
            matching intent, calling api's, handling errors
            and displaying the results
        
        '''
        slot_state = tracker.get_slot("state") # get the value in state slot
        slot_pincode = tracker.get_slot("pincode") # get the vaue in pincode slot
      
        # this if statement handles the case when user 
        # replies 'no' when asked if he wants previous 
        # results, to get nationwide results 

        if tracker.latest_message['intent'].get('name')=='deny': #check denial intent in user's latest message

            responses = requests.get("https://api.covid19india.org/data.json").json() # requesting the api for states data
            state = "Total" # `Total` signifies the data for entire India 

            # iterating through states    
            for data in responses["statewise"]:
                if data["state"] == state.title():
                
                    message = "Now Showing Cases For --> " + state.title()+"\n" + "****Overall****"+ "\n"+"\n" + "Active: " + data["active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data["recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n"+"\n"+"\n" + "****Today's Reported Cases****"+ "\n"+ "\n" + "Confirmed Today: " + data["deltaconfirmed"] + " \n"  + "Recovered Today: " + data["deltarecovered"] + " \n" + "Deaths Today: " + data["deltadeaths"]
            
            # output the message to user and return
            dispatcher.utter_message(message) 
            return []


        # else statement handles calls to api  
        # when asked for previous 
        # results
        elif tracker.latest_message['intent'].get('name')=='affirm':
            
     

            if slot_pincode : # if the previous pincode slot has a value

                # get data from pincode api --> get information with respect to pincodes
                responses = requests.get(f"https://api.postalpincode.in/pincode/{tracker.get_slot('pincode')}").json()

                # get the pincode
                pincode = slot_pincode
                
                # to catch exceptions of invalid pincodes 
                try:
                    temp_district = responses[0]['PostOffice'][0]['District']
                
                    temp_district = str(temp_district)
                    temp_state = responses[0]['PostOffice'][0]['State']

                    # removing brackets from district/postoffice names `Ashok Nagar (New Delhi)`-----> Ashok Nagar`
                    # and replacing `&`` with `and` to match the data for both api's and maintain uniformity
                    temp_district =  re.sub("\(.*?\)","",temp_district).replace('&', 'and') 
                    print(temp_district)
                    temp_state = re.sub("\(.*?\)","",temp_state).replace('&', 'and')
                    print(temp_state)

                        
                    # correcting some specific differences in data of postoffice and covid api's
                    # like - Bangalore and Bengaluru mismatch
                    if temp_district=='Bangalore':
                        temp_district='Bengaluru Urban'
                    if temp_state=='Chattisgarh':
                        temp_state='Chhattisgarh'                    
                    
                    responses = requests.get("https://api.covid19india.org/state_district_wise.json").json()
                    
                    # catching exception in case like : if state is 'Jammu And Kashmir' but key name is 'Jammu and Kashmir'
                    try:
                        info = responses[(temp_state.title())]['districtData'][temp_district.title()]
                    except:                            
                        info = responses[(temp_state.title()).replace('And', 'and')]['districtData'][temp_district.title().replace('And', 'and')]

                    
                    message = "Now Showing Cases For --> " + temp_district +"\n"+ "****Overall****"+ "\n"+  "\n" +  "\n"+ "Active: " + str(info["active"]) + " \n" + "Confirmed: " + str(info["confirmed"]) + " \n" + "Recovered: " + str(info["recovered"]) + " \n" + "Deaths: " + str(info["deceased"])+" \n"+ "\n" + "\n"+ "****Today's Reported Cases****"+ "\n" +  " \n" + "Confirmed Today: " + str(info["delta"]["confirmed"]) + " \n" + "Recovered Today: " + str(info["delta"]["recovered"]) + " \n" + "Deaths Today: " + str(info["delta"]["deceased"])

                    dispatcher.utter_message(message)

                    return []
                except: # exception in case of invalid pincode
                    
                    dispatcher.utter_message('Please Enter valid PinCode !')
                    return []





            else: # if the previous state slot has a value
               
                responses = requests.get("https://api.covid19india.org/data.json").json() # calling states data api
                message = "Please Enter Correct State Name !" #default message
                
                state = slot_state
                
                # if 'India' then show total cases for country
                if state.title() == "India":
                    state = "Total"

                # iterating and checking which state matches
                for data in responses["statewise"]:

                    if data["state"].title() == state.title()  :                    
                        message = "Now Showing Cases For --> " + state.title()+"\n" + "****Overall****"+ "\n"+"\n" + "Active: " + data["active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data["recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n"+"\n"+"\n" + "****Today's Reported Cases****"+ "\n"+ "\n" + "Confirmed Today: " + data["deltaconfirmed"] + " \n"  + "Recovered Today: " + data["deltarecovered"] + " \n" + "Deaths Today: " + data["deltadeaths"]
                
                # display output to user if a valid result came in all states 
                if message != "Please Enter Correct State Name !":
                    dispatcher.utter_message(message)
                    return []

                # otherwise check if it is a city/ other place name
                else:

                    # calling post office api for data of all post offices in India
                    responses = requests.get(f"https://api.postalpincode.in/postoffice/{tracker.get_slot('state')}").json()


                    
                    try: # to catch invalid/random names of places 
                        
                        # iterating over the 'PostOffice' key
                        for i in responses[0]['PostOffice']: 

                            # break the loop in case either the postoffice or district name matches
                            if str(i['Name']) == state.title() or str(i['District']) == state.title() :     
                                
                                temp_district = i['District']
                                temp_state = i['State']
                                break
                        
                        # removing brackets from district/postoffice names `Ashok Nagar (New Delhi)`-----> Ashok Nagar`
                        # and replacing `&`` with `and` to match the data for both api's and maintain uniformity
                        temp_district =  re.sub("\(.*?\)","",temp_district).replace('&', 'and') 
                        print(temp_district)
                        temp_state = re.sub("\(.*?\)","",temp_state).replace('&', 'and')
                        print(temp_state)

                        
                        # correcting some specific differences in data of postoffice and covid api's
                        # Bangalore and Bengaluru mismatch
                        if temp_district=='Bangalore':
                            temp_district='Bengaluru Urban'
                        if temp_state=='Chattisgarh':
                            temp_state='Chhattisgarh'

                        
                        responses = requests.get("https://api.covid19india.org/state_district_wise.json").json()
                        
                        # catching exception in case like : if state is 'Jammu And Kashmir' but key name is 'Jammu and Kashmir'
                        try:
                            info = responses[(temp_state.title())]['districtData'][temp_district.title()]
                        except:                            
                            info = responses[(temp_state.title()).replace('And', 'and')]['districtData'][temp_district.title().replace('And', 'and')]

                    
                        message = "Now Showing Cases For --> " + temp_district +"\n"+ "****Overall****"+ "\n"+  "\n" +  "\n"+ "Active: " + str(info["active"]) + " \n" + "Confirmed: " + str(info["confirmed"]) + " \n" + "Recovered: " + str(info["recovered"]) + " \n" + "Deaths: " + str(info["deceased"])+" \n"+ "\n" + "\n"+ "****Today's Reported Cases****"+ "\n" +  " \n" + "Confirmed Today: " + str(info["delta"]["confirmed"]) + " \n" + "Recovered Today: " + str(info["delta"]["recovered"]) + " \n" + "Deaths Today: " + str(info["delta"]["deceased"])

                        dispatcher.utter_message(message)

                        return []
                    
                    # in case of any exception means name is not a valid indian postoffice
                    except:
                        dispatcher.utter_message('Please Enter valid city/state name !')
                        return []
                        

        

            
            

        # this condition will match all other calls like when user asks for a specific location
        else: 
            
            # to handle exceptions during api calls and extracting information from returned json
            try: 

                
                entities = tracker.latest_message['entities']
                print('entities ',entities)

                # if the latest message entity had 'state'
                if entities[0]["entity"] == "state": 

                    # calling state data api
                    responses = requests.get("https://api.covid19india.org/data.json").json()
                    
                    # default message in case no state matches
                    message = "Please Enter Correct State Name !"
                    
                    # if user has entered `India` as state then get entire country's data
                    state = entities[0]["value"]
                    if slot_state.title() == "India":
                        state = "Total"
                
                    
                    # iterating through states - 'Total' means whole country's data
                    for data in responses["statewise"]:
                        if data["state"].title() == state.title():
                        
                            message = "Now Showing Cases For --> " + state.title()+"\n" + "****Overall****"+ "\n"+"\n" + "Active: " + data["active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data["recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n"+"\n"+"\n" + "****Today's Reported Cases****"+ "\n"+ "\n" + "Confirmed Today: " + data["deltaconfirmed"] + " \n"  + "Recovered Today: " + data["deltarecovered"] + " \n" + "Deaths Today: " + data["deltadeaths"]
                    
                    # if the state matches then output result message
                    if message != "Please Enter Correct State Name !":
                        dispatcher.utter_message(message)
                        return []
                    
                    # otherwise check if the input is a city/district/postoffice name
                    else:
                        
                        # calling api to get postoffice data
                        responses = requests.get(f"https://api.postalpincode.in/postoffice/{tracker.get_slot('state')}").json()

                        # printing to check what entity the bot interprets from user's data
                        entities = tracker.latest_message['entities']
                        print("Now Showing Data For:", entities)
                    

                        # store state
                        for i in entities:
                            if i["entity"] == "state":
                                state = i["value"]
                        

                        # to catch invalid/random names of places 
                        try:  
                            # iterating over the 'PostOffice' key
                            for i in responses[0]['PostOffice']: 

                                # break the loop in case either the postoffice or district name matches
                                if str(i['Name']) == state.title() or str(i['District']) == state.title() :     
                                    
                                    temp_district = i['District']
                                    temp_state = i['State']
                                    break
                            

                            # removing brackets from district/postoffice names `Ashok Nagar (New Delhi)`-----> Ashok Nagar`
                            # and replacing `&`` with `and` to match the data for both api's and maintain uniformity
                            temp_district =  re.sub("\(.*?\)","",temp_district).replace('&', 'and')
                            print(temp_district)
                            temp_state = re.sub("\(.*?\)","",temp_state).replace('&', 'and')
                            print('district is',temp_district)
                            print(temp_state)

                            

                            # correcting some specific differences in data of postoffice and covid api's
                            # like - Chattisgarh and Chhattisgarh mismatch
                            if temp_district=='Bangalore':
                                temp_district='Bengaluru Urban'
                            if temp_state=='Chattisgarh':
                                temp_state='Chhattisgarh'

                            # calling covid stats api
                            responses = requests.get("https://api.covid19india.org/state_district_wise.json").json()
                            
                            # catching exception in case like : if state is 'Jammu And Kashmir' but key name is 'Jammu and Kashmir'
                            try:
                                info = responses[(temp_state.title())]['districtData'][temp_district.title()]
                            except:    
                                info = responses[(temp_state.title()).replace('And', 'and')]['districtData'][temp_district.title().replace('And', 'and')]

                        
                            message = "Now Showing Cases For --> " + temp_district +"\n"+ "****Overall****"+ "\n"+  "\n" +  "\n"+ "Active: " + str(info["active"]) + " \n" + "Confirmed: " + str(info["confirmed"]) + " \n" + "Recovered: " + str(info["recovered"]) + " \n" + "Deaths: " + str(info["deceased"])+" \n"+ "\n" + "\n"+ "****Today's Reported Cases****"+ "\n" +  " \n" + "Confirmed Today: " + str(info["delta"]["confirmed"]) + " \n" + "Recovered Today: " + str(info["delta"]["recovered"]) + " \n" + "Deaths Today: " + str(info["delta"]["deceased"])

                            dispatcher.utter_message(message)

                            return []
                        except:
                            dispatcher.utter_message('Please Enter valid city/state name !')
                            return []
            except:
                dispatcher.utter_message('Please enter valid city/state name!')
                return []


        


            
            else:

                # calling pincode api
                responses = requests.get(f"https://api.postalpincode.in/pincode/{tracker.get_slot('pincode')}").json()

                entities = tracker.latest_message['entities']
                print("Now Showing Data For:", entities)

                for i in entities:
                    if i["entity"] == "pincode":
                        pincode = i["value"]

                # to catch exceptions of invalid pincodes        
                try:
                        
                    temp_district = responses[0]['PostOffice'][0]['District']
                
                    temp_district = str(temp_district)
                    temp_state = responses[0]['PostOffice'][0]['State']

                    # removing brackets from district/postoffice names `Ashok Nagar (New Delhi)`-----> Ashok Nagar`
                    # and replacing `&`` with `and` to match the data for both api's and maintain uniformity
                    temp_district =  re.sub("\(.*?\)","",temp_district).replace('&', 'and') 
                    print(temp_district)
                    temp_state = re.sub("\(.*?\)","",temp_state).replace('&', 'and')
                    print(temp_state)

                        
                    # correcting some specific differences in data of postoffice and covid api's
                    # like - Bangalore and Bengaluru mismatch
                    if temp_district=='Bangalore':
                        temp_district='Bengaluru Urban'
                    if temp_state=='Chattisgarh':
                        temp_state='Chhattisgarh'                    
                    
                    responses = requests.get("https://api.covid19india.org/state_district_wise.json").json()
                    
                    # catching exception in case like : if state is 'Jammu And Kashmir' but key name is 'Jammu and Kashmir'
                    try:
                        info = responses[(temp_state.title())]['districtData'][temp_district.title()]
                    except:                            
                        info = responses[(temp_state.title()).replace('And', 'and')]['districtData'][temp_district.title().replace('And', 'and')]

                    
                    message = "Now Showing Cases For --> " + temp_district +"\n"+ "****Overall****"+ "\n"+  "\n" +  "\n"+ "Active: " + str(info["active"]) + " \n" + "Confirmed: " + str(info["confirmed"]) + " \n" + "Recovered: " + str(info["recovered"]) + " \n" + "Deaths: " + str(info["deceased"])+" \n"+ "\n" + "\n"+ "****Today's Reported Cases****"+ "\n" +  " \n" + "Confirmed Today: " + str(info["delta"]["confirmed"]) + " \n" + "Recovered Today: " + str(info["delta"]["recovered"]) + " \n" + "Deaths Today: " + str(info["delta"]["deceased"])

                    dispatcher.utter_message(message)

                    return []
                except: # exception in case of invalid pincode
                    
                    dispatcher.utter_message('Please Enter valid PinCode !')
                    return []

