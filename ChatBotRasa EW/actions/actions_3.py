
# importing libraries
import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused

logger = logging.getLogger(__name__)

class ActionEntity(Action):

    '''
        this class handles the cases if 
        user wants previously calculated value
        or he wants nationwide results or
        to ask for which location he wants 
        covid-19 stats
    '''

    def name(self) -> Text:

        '''
            defined name of action
        '''
        return "action_know_whether_previous_calculated"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        '''
            functions to manage cases
        '''
        slot_state = tracker.get_slot("state")
        slot_pincode = tracker.get_slot("pincode")
    
        # if the user answers no to the question if he wants previous result then he will get nationwode results
        if  tracker.latest_message['intent'].get('name')=='deny':
            dispatcher.utter_message(
            text="Showing Nationwide results")

        # first time covid stats check
        elif (slot_state is None and slot_pincode is None) :
            dispatcher.utter_message(
            text="Which pincode/state/city do you want to know about?")

        # recently shown results
        else:
            dispatcher.utter_message(
            text=f"Do you want recently shown results of {slot_pincode}?")

        return []