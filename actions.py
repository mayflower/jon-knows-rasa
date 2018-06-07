import logging

from rasa_core.actions import Action

class ActionWhoKnows(Action):
    def name(self):
        return 'action_who_knows'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Action who_knows')
        return []

class ActionIForgot(Action):
    def name(self):
        return 'action_forgotten'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Action forgotten')
        return []
class ActionClaimToKnow(Action):
    def name(self):
        return 'action_claim_to_know'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Action claim_to_know')
        return []