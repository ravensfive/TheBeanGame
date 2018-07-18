# main python program
import json, random, re

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.b6886b51-4e5f-4e46-872c-eb7167e1e67e"):
        raise ValueError("Invalid Application ID")

    # test if session is new
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    # test and set session status
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# define session start
def on_session_started(session_started_request, session):
    print ("Starting new session")

# define session launch
def on_launch(launch_request, session):
    return get_welcome_response()

# control intent call 
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetOneBean":
        return get_bean()
    elif intent_name == "TellBean":
        return tell_bean(intent)
    elif intent_name == "TellAllBean":
        return tell_me_all_beans()
    elif intent_name == "PlayGame":
        return play_game()
    elif intent_name == "GetInstructions":
        return get_instructions()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

# code to automatically remove ssml markup
def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Hope you enjoyed playing the bean game, please play again soon"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}
    card_title = "The Bean Game"
    speech_output = "Welcome to the bean game, if you've played before, just say lets play beans, if you need to know how to play, then just say, how do you play? " \
                    "if you need a reminder of all the beans then please say tell me about the beans"       
    reprompt_text = "Start a game by saying lets play beans, or if you need help, just say how do you play? or if you need a reminder of the " \
                    "beans then say, tell me about the beans "
    should_end_session = False

    speech_output = "<speak>" + speech_output + "</speak>"
    #speech_output = '<speak> <amazon:effect name="whispered"> ' + speech_output + '</amazon:effect> </speak>'

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')
    
    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define welcome intent
def get_instructions():
    session_attributes = {}
    card_title = "Instructions"
    speech_output = "Here's how you play the bean game, I'll call out the names of the beans, when I do, you must do the action for that bean,   " \
                    " for example, when I say jumping bean you must jump until the " \
                    "next bean is called, if you need to know the actions for each bean, say " \
                    "tell me about the beans, if you think you are ready to go then, say lets play beans"
    reprompt_text = "if you want to know about the actions for each bean, say " \
                    "tell me about the beans, if you think you are ready to go then, say lets play beans"
    
    should_end_session = False

    speech_output = "<speak>" + speech_output + "</speak>"

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')
    #speech_output = '<speak> <amazon:effect name="whispered"> ' + speech_output + '</amazon:effect> </speak>'

    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define get_bean function
def get_bean():
    # set intent attributes
    session_attributes = {}
    card_title = "A Bean"
    reprompt_text = ""
    should_end_session = False

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)

    # randomly select bean from json, zero based = random number between 1 and number in json minus 1
    speech_output = beandata['beans'][random.randint(1,len(beandata['beans']))-1]['Name'] + generatebreakstring(500,"ms") + ", if you would like another, just say bean please"

    speech_output = "<speak>" + speech_output + "</speak>"

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')
 
    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, card_output, reprompt_text, should_end_session))

def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length - need to also add some code for milliseconds
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

# define get_bean function
def play_game():
    # set intent attributes
    session_attributes = {}
    card_title = "Playing Game"
    reprompt_text = ""
    should_end_session = False

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)
    
    breakstring = generatebreakstring(500, 'ms')

    speech_output = "Get ready your game will start in one, " + breakstring + "two, " + breakstring + "three, " + breakstring + " lets play beans, " +  generatebreakstring(250, 'ms')

    # loop around 20 beans and gradually reduce time
    for b in range(0,20):
        
        # select random bean
        randombean = beandata['beans'][random.randint(1,len(beandata['beans']))-1]['Name']

        #if randombean == "French Bean" :
        #    randombean = randombean +  "<audio src=https://s3.amazonaws.com/alexaskillravensfive/ooh_la_la._TTH_.mp3 />"

        # <audio src=https://s3.amazonaws.com/alexaskillravensfive/ooh_la_la._TTH_.mp3 />

        # custom string depending on postion in loop                            
        if b == 0 :
            speech_output = speech_output + "<audio src='https://s3.amazonaws.com/alexaskillravensfive/music_zapsplat_mr_jelly.mp3' /> " + randombean 
        elif b <= 4 :    
            speech_output = speech_output + " " + generatebreakstring(4000, 'ms') + " " + randombean
            if b == 4 :
                speech_output = speech_output + "<audio src='https://s3.amazonaws.com/alexaskillravensfive/music_zapsplat_mr_jelly.mp3' /> " + generatebreakstring(500, 'ms')
        elif b <= 9 :
            speech_output = speech_output + " " + generatebreakstring(3000, 'ms') + " " + randombean
            if b == 9 :
                speech_output = speech_output + "<audio src='https://s3.amazonaws.com/alexaskillravensfive/music_zapsplat_mr_jelly.mp3' /> " + generatebreakstring(500, 'ms')
        elif b <= 14 :
            speech_output = speech_output + " " + generatebreakstring(2000, 'ms') + " " + randombean
            if b == 14 :
                speech_output = speech_output + generatebreakstring(500, 'ms') + ", are you ready for super fast mode? " + generatebreakstring(500, 'ms')
        elif b <= 19 :
            speech_output = speech_output + " " + generatebreakstring(750, 'ms') +  " " +randombean    
            if b == 19 :
                speech_output = speech_output + generatebreakstring(500, 'ms') + ", woah, that was awesome, I think you did great, if you want to play again just say play game"
            
        # build string with break of 3 seconds
        #speech_output = speech_output + '<break time="3s"/>'  + randombean    

    # set in ssml frame
    speech_output = "<speak>" + speech_output  + "</speak>"      

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')
 
    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define tell me about the beans
def tell_me_all_beans():
    # set intent attributes
    session_attributes = {}
    card_title = "Tell Me About The Beans"
    reprompt_text = ""
    should_end_session = False

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)

    # set up temporary speech output
    speech_output = ""

    # loop through each bean in json
    for b in beandata['beans'] :
        if b == 0 :
            speech_output = b['Name'] + " , " + b['Description'] 
        else:
         # add name and description to speech output
            speech_output = speech_output + " " + generatebreakstring(1,'s') + " , " + b['Name'] + " , " + b['Description']    

    speech_output = "<speak>" + speech_output + "</speak>"

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')

    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define tell me about the beans
def tell_bean(intent):
    # set intent attributes
    session_attributes = {}
    card_title = "Tell me about a Bean"
    reprompt_text = ""
    should_end_session = False

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)
    
    # set up temporary speech output
    speech_output = ""

    # test if bean exists in json
    if 'bean' in intent['slots']:
        # extract slot value
        bean = intent['slots']['bean']['value']

        # test json for the bean (based on a keyword search), record instructions and break if found
        for b in beandata['beans'] : 
            if b['stringSearch'] in bean:
                speech_output = "For the " + b['Name'] + " you must " + b['Description'] + generatebreakstring(500,'ms') + " feel free to ask me about another"
                break
            else:
                speech_output = "Hmm I must admit, I haven't heard of that bean before "        

    else:
        speech_output = "Hmm I must admit, I haven't heard of that bean before. Try again with another bean"

    # wrap for SSML output
    speech_output = "<speak>" + speech_output + "</speak>"

    # replace bean with phonetic version
    speech_output = speech_output.replace("beans",'<phoneme alphabet="ipa" ph="biːns">beans</phoneme>')
    speech_output = speech_output.replace("bean",'<phoneme alphabet="ipa" ph="biːn">bean</phoneme>')

    card_output = cleanssml(speech_output)

    # return values
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))
    
    
# build message response
def build_speechlet_response(title, output, cardoutput, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml":  output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": cardoutput
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

# build response
def build_response(session_attributes, speechlet_response):
    return {
    "version": "1.0",
    "sessionAttributes": session_attributes,
    "response": speechlet_response }

