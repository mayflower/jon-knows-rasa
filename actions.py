import logging
import json

from rasa_core.actions import Action
from rasa_core.events import AllSlotsReset

class ActionWhoKnowsTopic(Action):
    def name(self):
        return 'action_who_knows_topic'
    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic') if tracker.get_slot('topic') else None
        if topic is None:
            dispatcher.utter_message('Ich habe kein Topic bekommen')
            return []

        topic = str(topic) 
        bests = []
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'skills' not in skillData:
            dispatcher.utter_message('Keine Skills sinds vorhanden')
            return []

        for persistedTopic in skillData['skills']:
            if topic.lower() != persistedTopic.lower() or len(skillData['skills'][persistedTopic]) == 0: continue
            for user in skillData['skills'][persistedTopic]: bests.append(user)
        if len(bests) == 0:
            dispatcher.utter_message('Kein Kollege weiß etwas zun Thema '+topic)
        else:
            bestsString = ''
            for user in bests:
                bestsString += user['name']+' (Score: '+str(user['score'])+'), '
            if bestsString.endswith(", "): bestsString = bestsString[:-2]
            dispatcher.utter_message('Die folgenden Kollegen meinen Ahnung zu haben: '+bestsString)
        return [AllSlotsReset()]

class ActionIForgot(Action):
    def name(self):
        return 'action_forgotten'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Action forgotten')
        return []

class ActionClaimToKnowTopic(Action):
    def name(self):
        return 'action_claim_to_know_topic'
    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic')
        user = tracker.get_slot('user')
        if topic is None:
            dispatcher.utter_message('No topic given')
            return []
        if user is None:
            dispatcher.utter_message('No user given')
            return []
        topic = str(topic) 
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'skills' not in skillData:
            dispatcher.utter_message('Keine Skills sinds vorhanden')
            return []
        if topic not in skillData['skills']:
            skillData['skills'][topic] = []
            dispatcher.utter_message('Das Topic '+topic+' ist noch nicht bekannt, wird angelegt')
        persistedTopic = skillData['skills'][topic]

        foundUser = False
        for key in persistedTopic:
            if persistedTopic[key].name == user:
                persistedTopic[key].score = persistedTopic[key].score + 1 
                dispatcher.utter_message('User '+user+'` Score um eins erhöht für Topic: '+topic)
                foundUser = True
                break
        if foundUser is True:
            skillData[topic].append({"name": user, "score": 1})
            dispatcher.utter_message('User '+user+'` wurde für das Topic vermerkt: '+topic)
        
        return [AllSlotsReset()]
    
    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
            

class ActionTopicsInCategory(Action):
    def name(self):
        return 'action_topics_in_category'
    def run(self, dispatcher, tracker, domain):
        category = tracker.get_slot('category') if tracker.get_slot('category') else 'None'
        category = str(category) 
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'categories' not in skillData:
            dispatcher.utter_message('Keine Skills sinds vorhanden')
            return []
        for persistedCategory in skillData['categories']:
            if persistedCategory.lower() != category.lower():
                continue
            topics = skillData['categories'][persistedCategory]
            if len(topics) == 0:
                dispatcher.utter_message('Kein Topic gefunden in Kategroie: '+category)
                return []
            topicsString = ''
            for topic in topics:
                topicsString += ', '+topic
            dispatcher.utter_message('Folgen Topics habe ich in Kategoie '+category+' gefunden: '+topicsString)
            return [AllSlotsReset()]
        
        categories = ''
        for category in skillData['categories']:
            categories += ', '+category
        dispatcher.utter_message('Keine Kategorie mit dem name '+category+' gefunden, wähle doch eine von '+categories)
        
        return [AllSlotsReset()]