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
        this class performs the action of
        remembering name of the user if
        there was any name input before
    '''

    def name(self) -> Text:

        '''defining name of the action'''
        return "action_get_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        '''
            function to perform the task
        '''
        slot_name = tracker.get_slot("name")

        # if there is no name stored
        if slot_name is None:
            dispatcher.utter_message(
            text="Hi! What is your name?")

        # if there is a name stored
        else:
            dispatcher.utter_message(
            text="Hi " + slot_name.title() +  "! What can I do for you ?")

        return []