# create the bean json from scratch

#import random package
import json, random

# setup json
def setupJson() :
    global beandata
    beandata = {}
    beandata['beans'] = []

setupJson()

# add beans to the json, called with parameters
def addbeantoJson(Name,Description, stringSearch) :
    beandata['beans'].append({    
    'Name': Name,
    'Description': Description,
    'stringSearch' : stringSearch
    })

addbeantoJson("String bean", "Stand up really tall with your hands in the air", "string")
addbeantoJson("Jumping bean", "Jump, jump, jump, jump", "jumping")
addbeantoJson("Broad bean", "Stand with your hands to the side and be broad", 'broad')
addbeantoJson("Mexican bean", "Say Ole, Ole, Ole", 'mexican')
addbeantoJson("French bean", "Say Oooo Laa Laa", 'french')
addbeantoJson("Runner bean", "Run on the spot as fast as you can", 'runner')
addbeantoJson("Jelly bean", "Wibble wobble like a jelly", 'jelly')
addbeantoJson("Baked bean", "Lay on the floor in a ball", 'baked')
addbeantoJson("Chilli bean", "Shiver like you are really cold", 'chilli')
addbeantoJson("Frozen bean", "Stay still and freeze", 'frozen')
addbeantoJson("beans on Toast", "Lay on the floor like a starfish", 'toast')

print(beandata)

def writejson():
    with open('beans.json', 'w') as outfile:  
        json.dump(beandata, outfile) 

writejson()

#def countelements():
#    ChosenBean = beandata['beans'][random.randint(1,len(beandata['beans']))-1]['Name']
#    print(ChosenBean)

#countelements()

