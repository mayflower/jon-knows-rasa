## Story User greets
* greet
    - utter_greet

## Story User says goodby
* greet
    - utter_goodbye

## Story User asks for something
* who_knows_topic
    - action_who_knows

## Story User claims to know something
* claim_to_know_topic
    - utter_get_who_knows_category
    - action_claim_to_know

## Story user asks for topics in category
* topics_in_category
    - action_topics_in_category

## Story user forgot skills
* forgott_topic
    - action_forgotten
