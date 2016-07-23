# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 14:01:21 2016

@author: dokbr

An alexa app to check on the status of nearby capital bikeshare stations
"""

import xml.etree.ElementTree as ET
import httplib


def get_station_data():
    # get the xml as a string
    try:
        conn = httplib.HTTPSConnection('www.capitalbikeshare.com')
        conn.request("GET", "/data/stations/bikeStations.xml")
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    # put it into an ET object
    root = ET.fromstring(data)    
    return root
    
def get_bikes_dict():
    # get the xml
    root = get_station_data()
    
    #iterate through the stations and build a dict of just the terminalName
    bikes_dict = {}
    for station in root:
        bikes_dict[int(station.find('terminalName').text)] = int(station.find('nbBikes').text)
    
    return bikes_dict

#custom get speech function to return the speech for bikeshare
def get_speech():

    # define a list of stops and plain language names in the order
    # that you want Alexa to read them.
    station_list = [[31115, "Columbia"],[31102,"Kenyon"],[31105,"Harvard"],[31207,"Fairmont"]]

    # get the bikes counts
    bikes_dict = get_bikes_dict()

    # for each station we're looking for, look up the number of bikes in the bikes_dict
    results_list = []
    for station, name in station_list:
        results_list.append([name,bikes_dict[station]])
    
    speech_output = "Nearby bikes: "
    for name, bikes in results_list:
        speech_output += str(bikes) + " bike"
        if bikes != 1:
            speech_output += "s"
        speech_output += " at " + str(name) + ", "
    
    
    return speech_output
    
    
# ---------------------- ALEXA FUNCTIONS ------------------#
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill 
    For now, we aren't using any intents    
    """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "BikeshareAlexa":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    #elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
    #    return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = get_speech()
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't think this should be read..."
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }