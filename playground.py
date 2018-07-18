# test loop
import json, random, re

def get_multiple_beans():
    # set intent attributes
    session_attributes = {}
    card_title = "beanmultiplegot"
    reprompt_text = ""
    should_end_session = False

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)

    speech_output = ""

    # loop around 20 beans and gradually reduce time
    for b in range(0,20):
        
        # select random bean
        randombean = beandata['beans'][random.randint(1,len(beandata['beans']))-1]['Name']

        # custom string depending on postion in loop
        if b == 0:
            speech_output = speech_output + "Get ready, your game will start in three" \
                            + '<break time="500ms"/>' + "two" + '<break time="500ms"/>' + "one" \
                            + '<break time="500ms"/>' + " play beans " +  '<break time="500ms"/>' + randombean
        elif b <= 5 :    
            pause = str(5000)
            speech_output = speech_output + '<break time=" ' + pause + 'ms"/>'  + randombean
        elif b <= 10 :
            pause = str(3500)
            speech_output = speech_output + '<break time=" ' + pause + 'ms"/>'  + randombean
        elif b <= 15 :
            pause = str(2500)
            speech_output = speech_output + '<break time=" ' + pause + 'ms"/>'  + randombean
        elif b <= 20 :
            pause = str(1000)
            speech_output = speech_output + '<break time=" ' + pause + 'ms"/>'  + randombean    

    # set in ssml frame
    speech_output = "<speak>" + speech_output + "</speak>"  

    print(speech_output)

#get_multiple_beans()

def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length - need to also add some code for milliseconds
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

#print(generatebreakstring(3500,"ms"))


# define tell me about the beans
def tell_bean():

    # open the bean json
    with open('beans.json') as json_file :  
        beandata = json.load(json_file)

    # set up temporary speech output
    speech_output = ""

    bean = 'the runner bean'

    for b in beandata['beans'] :
        if b['stringSearch'] in bean:
            speech_output = b['Description']
            break
        else:
            speech_output = "I don't know about that bean "        

    speech_output = "<speak>" + speech_output + "</speak>"

#tell_bean()

def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext

def test():
    #x = "ing"
    #y = "testing"
    #test = x in y
    #print(test)

    string = 'xxbeanxx'
    print(string)
    string = string.replace('bean','<phoneme alphabet="ipa" ph="biːn">bean</phoneme>') 
    print(string)
    string.replace('b','x')
    print(string)   

    string = cleanssml(string)

    print(string)

test()


