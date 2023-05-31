import json
import re

from openai_config import OPENAI_API_KEY
import openai
import random
import numpy.random
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import ast

openai.organization = "org-dTvWFBPgytk7lTpqZMZMImrL"
openai.api_key = OPENAI_API_KEY


def generateDateList(startDate, endDate):
    generatedDates = [startDate]

    # loop to get each date till end date
    while startDate != endDate:
        startDate += timedelta(days=1)
        generatedDates.append(startDate)

    return generatedDates


birthdate_ranges = [generateDateList(date(1995, 1, 1), date(2020, 1, 1)),
                    generateDateList(date(2021, 1, 1), date(2045, 1, 1)),
                    generateDateList(date(2046, 1, 1), date(2057, 1, 1))]


def getRandomBSEDates():
    current_year = 2075

    chosen_range_list = birthdate_ranges[numpy.random.choice(numpy.arange(3), p=[0.1, 0.4, 0.5])]

    birthDate = random.choice(chosen_range_list)
    hire_age = random.randint(18, 35)
    days_to_add = random.randint(0, 180)

    startDate = birthDate + relativedelta(years=hire_age, days=days_to_add)

    while startDate.year > current_year:
        hire_age = random.randint(18, 35)
        days_to_add = random.randint(0, 180)

        startDate = birthDate + relativedelta(years=hire_age, days=days_to_add)

    endDate = None

    if current_year - birthDate.year > 65:
        endDate = birthDate + relativedelta(years=65, days=random.randint(0, 30))

    birthDate = birthDate.strftime("%Y-%m-%d")
    startDate = startDate.strftime("%Y-%m-%d")
    if endDate is not None:
        endDate = endDate.strftime("%Y-%m-%d")

    return birthDate, startDate, endDate


def cleanTextForList(t):
    t = re.sub(r'.*(?=\[([\s\S]*?)\])', '', t, re.DOTALL)

    return t


def EmployeeCreation():
    def get_last_integer(string):
        pattern = r'\d+'  # Matches one or more digits
        integers = re.findall(pattern, string)
        if integers:
            return int(integers[-1])
        else:
            return None


    with open('base_data.json') as d:
        depData = json.load(d)

    with open("ai_data.json") as output:
        aiData = json.load(output)

    empWClea = 0
    amtEmp = len(aiData["employee"])
    try:
        clearances = aiData["ClearanceLevel"]
        for e in aiData["employee"]:
            if "clearance" in e:
                empWClea += 1
            if "clearance" not in e:
                for dep in depData["department"]:
                    if dep["name"] == e["dep"]:

                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{
                                "role": "system",
                                "content": """The Frontier Space Exploration Agency, is at the forefront of space exploration and colonization endeavors. With a mission to push the boundaries of human knowledge and find a new home after the destruction of Earth, F-SEA undertakes ambitious projects and scientific missions to explore uncharted frontiers beyond our solar system.
                                    F-SEA's primary focus revolves around three key areas: space exploration, colonization, and scientific research. F-SEA ventures into space to gather valuable data, study celestial bodies, and unlock the mysteries of the universe. Their missions include manned and unmanned expeditions to distant planets, moons, and other celestial objects.
                                    F-SEA envisions a future where humans establish sustainable colonies beyond the mothership. Their dedicated teams of scientists and researchers conduct studies on various disciplines, including astrophysics, planetary geology, astrobiology, and more. By unraveling the secrets of the cosmos, F-SEA contributes to our understanding of the universe, potentially leading to breakthroughs in fields such as cosmology, exoplanet exploration, and the search for extraterrestrial life.
                                    In summary, F-SEA is a pioneering organization that combines technological innovation, human exploration, and scientific research to expand our knowledge of the universe, establish sustainable colonies beyond Earth, and pave the way for humanity's future in space."""
                            },
                                {"role": "assistant", "content":
                                    '''Here is the employee clearance levels list:
                                     %s
                                     I want you to select a clearance level for the following employee based on their information, 
                                     the department information, and based on what you know about F-SEA.
    
                                     Employee: %s
    
                                     Department: %s
                                     
                                     If you cannot find a suitable clearance level to match the employee, assume general access level.
                                     Format your response as a single number without any extracurricular text.
                                     Do not explain your answer. Do not respond with anything other than just an integer.
                                    
                                ''' % (e, clearances, dep)}
                            ],
                            n=1,
                            temperature=0
                        )
                        for d in completion["choices"]:
                            try:
                                mess = d["message"]["content"]
                                print(mess)
                                c = get_last_integer(mess)
                                e["clearance"] = c

                                print("Success!: ", e["clearance"])
                                with open("ai_data.json", "w") as output:
                                    json.dump(aiData, output, indent=4)

                            except Exception as e:
                                print(e)
                                pass
                            break

    except Exception as e:
        print("GPT Exception")
        print(e)
        pass

    print(empWClea, '/', amtEmp, " clearances generated")


activeDates = generateDateList(date(2038, 6, 7), date(2075, 11, 20))


def generateMissionDuration(dDate):
    startDate = random.choice(generateDateList(dDate, date(2075, 11, 20)))
    endDate = startDate + relativedelta(years=random.randint(0, 2), days=random.randint(0, 180))
    startDate = startDate.strftime('%Y-%m-%d')
    endDate = endDate.strftime('%Y-%m-%d')

    return startDate, endDate


def OriginCreation():
    with open('base_data.json') as d:
        depData = json.load(d)["department"]

    deps = []
    for d in depData:
        if d["name"] not in ["Navigation", "Communications",
                             "Security", "Human Resources",
                             "Legal", "Education",
                             "Entertainment"]:
            deps.append(d)

    with open("ai_data.json") as output:
        aiData = json.load(output)

    print("Number of Generated Origins: ", len(aiData["origin"]))

    messageList = []
    try:
        for i in range(20):
            for j in range(2):
                dDate = random.choice(activeDates)
                dateRanges = []
                for k in range(random.randint(1, 5)):
                    s, e = generateMissionDuration(dDate)
                    dateRanges.append((s, e))

                message = {"role": "user", "content":
                    '''I want you to generate a list of python dictionaries given the following example and given what you know about F-SEA:
                    example:
                    [{
                      "name": "Lypso",
                      "description": "A highly hazardous gaseous ice planet",
                      "discoveryDate": "yyyy-mm-dd",
                      "depID": 0,
                      "missions": [
                        {
                          "name": "Dying Prophet",
                          "startDate": "yyyy-mm-dd",
                          "endDate": "yyyy-mm-dd",
                          "description": "Recon mission to investigate reports of a glowing 'rosetta-stone-like' object"
                        },
                        {
                          "name": "Gaseous Depths",
                          "startDate": "yyyy-mm-dd",
                          "endDate": "yyyy-mm-dd",
                          "description": "Exploratory mission to study the atmospheric composition and behavior of gaseous pockets"
                        }
                      ]
                        }]
                        
                    Important:
                    This is the discovery date to use: %s
                    These are the departments to choose from: %s
                    These are the mission startDate-endDate pairs to choose from: %s
                    The depID should match the depID of the department that headed the mission.
                    Each origin discoveryDate must be before any of the mission dates.
                    Each origin should have a number of missions that matches the amount of mission duration pairs.
                    Do not use the origin name given in the example.
                    Each mission must have startDate within this range: 2038-06-06 to 2075-11-22
                    Not every mission must have an end date, if it makes sense within the context of the mission. It is your choice. If it does not have an endDate, mark the endDate as None.
                    Every mission duration must make sense given the nature and purpose of the mission.
                    Missions can range from very dangerous/lethal to harmless.

                    
                    The produced data should be in the format of a python list of python dictionaries. 
                Blank attributes should be marked with the keyword None as found in python. Do NOT mark them null.
                Return the list of python dicts as is. I will be using the ast.literal_eval() function to process the data,
                so make sure your response is in a usable format.
    
    
                ''' % (dDate, deps, dateRanges)}
                fsea = {
                    "role": "system",
                    "content": """The Frontier Space Exploration Agency, is at the forefront of space exploration and colonization endeavors. With a mission to push the boundaries of human knowledge and find a new home after the destruction of Earth, F-SEA undertakes ambitious projects and scientific missions to explore uncharted frontiers beyond our solar system.
            F-SEA's primary focus revolves around three key areas: space exploration, colonization, and scientific research. F-SEA ventures into space to gather valuable data, study celestial bodies, and unlock the mysteries of the universe. Their missions include manned and unmanned expeditions to distant planets, moons, and other celestial objects.
            F-SEA envisions a future where humans establish sustainable colonies beyond the mothership. Their dedicated teams of scientists and researchers conduct studies on various disciplines, including astrophysics, planetary geology, astrobiology, and more. By unraveling the secrets of the cosmos, F-SEA contributes to our understanding of the universe, potentially leading to breakthroughs in fields such as cosmology, exoplanet exploration, and the search for extraterrestrial life.
            In summary, F-SEA is a pioneering organization that combines technological innovation, human exploration, and scientific research to expand our knowledge of the universe, establish sustainable colonies beyond Earth, and pave the way for humanity's future in space.
            F-SEA also works to contain and experiment on discovered extraterrestrial lifeforms"""
                }

                messageList.append(fsea)
                messageList.append(message)

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messageList,
                    n=1,
                    temperature=1
                )
                for d in completion["choices"]:
                    messageList.clear()
                    o = cleanTextForList(d["message"]["content"])
                    try:
                        originList = ast.literal_eval(o)
                        messageList.append(
                            {"role": "system", "content": f"""This is the last generated origin list: {originList}
                            You do not need to generate anything for this origin. Just keep this origin's data in mind
                            while you fill in the data for the next origin."""})
                        aiData["origin"] = aiData["origin"] + originList
                        print("Success!: ", o)
                        print("Total Origins: ", len(aiData["origin"]))
                        with open("ai_data.json", "w") as output:
                            json.dump(aiData, output, indent=4)

                    except Exception as e:
                        print(o)
                        print("literal_eval() Exception")
                        print(e)
                        messageList.append({"role": "user",
                                            "content": "You either added unnecessary text or formatted incorrectly. Do not do that with the next generation."})
                        pass

    except Exception as e:
        print(e)
        pass


def SpecimenCreation():

    with open("ai_data.json") as output:
        aiData = json.load(output)

    print("Number of Generated Specimens: ", len(aiData["specimen"]))

    messageList = []
    try:
        for i in range(20):
            for j in range(2):
                oDict = random.choice(aiData["origin"])
                statusList = aiData["ContainmentStatus"]
                message = {"role": "user", "content":
                    '''I want you to generate a short python list of python dictionaries given the following example and given what you know about F-SEA:
                    example:
                    [{
                        "name": "SpecimenName",
                        "statusID": 1,
                        "mission": "Name of mission",
                        "threatLevel": 5.4,
                        "acquisitionDate": "yyyy-mm-dd",
                        "notes": "notes detailing any fun or important facts about the specimen",
                        "description": "detailed description"
                }]

                    Important:
                    The threatLevel should be a float from 0.0 to 10.0. The closer to 0, the less dangerous, the higher the more dangerous.
                    The threatLevel should be based on aggressiveness and hostility and how much of a danger the specimen poses to humans and other specimens.
                    The statusID should match the containmentStatusID whose description best matches the specimen's threat. Choose from the follwoing:
                    %s
                    
                    The acquisition date should correlate to a date between the startDate and endDate (inclusive) of one of the missions provided in the dictionary below:
                    %s
                   
                   The specimens are mostly alien or anomalous in nature.
                   Notes should detail any fun or important facts about the specimen or what anything odd about the specimen.
                   The description should thoroughly detail each specimen's habits, appearance, and it should correspond to their threatLevel.
                   The mission name should match the mission the specimen was discovered on in the provided dict.

                    The produced data should be in the format of a python list of python dictionaries. 
                Blank attributes should be marked with the keyword None as found in python. Do NOT mark them null.
                Return the list of python dicts as is. DO NOT PUT ANY TEXT BEFORE OR AFTER THE LIST.


                ''' % (statusList, oDict)}
                fsea = {
                    "role": "system",
                    "content": """The Frontier Space Exploration Agency, is at the forefront of space exploration and colonization endeavors. With a mission to push the boundaries of human knowledge and find a new home after the destruction of Earth, F-SEA undertakes ambitious projects and scientific missions to explore uncharted frontiers beyond our solar system.
            F-SEA's primary focus revolves around three key areas: space exploration, colonization, and scientific research. F-SEA ventures into space to gather valuable data, study celestial bodies, and unlock the mysteries of the universe. Their missions include manned and unmanned expeditions to distant planets, moons, and other celestial objects.
            F-SEA envisions a future where humans establish sustainable colonies beyond the mothership. Their dedicated teams of scientists and researchers conduct studies on various disciplines, including astrophysics, planetary geology, astrobiology, and more. By unraveling the secrets of the cosmos, F-SEA contributes to our understanding of the universe, potentially leading to breakthroughs in fields such as cosmology, exoplanet exploration, and the search for extraterrestrial life.
            In summary, F-SEA is a pioneering organization that combines technological innovation, human exploration, and scientific research to expand our knowledge of the universe, establish sustainable colonies beyond Earth, and pave the way for humanity's future in space.
            F-SEA also works to contain and experiment on discovered extraterrestrial lifeforms"""
                }

                messageList.append(fsea)
                messageList.append(message)

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messageList,
                    n=1,
                    temperature=1
                )
                for d in completion["choices"]:
                    messageList.clear()
                    mess = d["message"]["content"]
                    o = mess[mess.find('['):mess.rfind(']')+1]
                    try:
                        originList = ast.literal_eval(o)
                        messageList.append(
                            {"role": "system", "content": f"""This is the last generated specimen list: {originList}
                            You do not need to generate anything for this origin. Just keep this origin's data in mind
                            while you fill in the data for the next origin."""})

                        for ori in aiData["origin"]:
                            if oDict == ori:
                                for m in ori["missions"]:
                                    for ol in originList:
                                        if m["name"] == ol["mission"]:
                                            m["specimens"].append(ol)

                                print('Booyah!')

                        print("Success!: ", o)
                        with open("ai_data.json", "w") as output:
                            json.dump(aiData, output, indent=4)

                    except Exception as e:
                        print(o)
                        print("literal_eval() Exception")
                        print(e)
                        messageList.append({"role": "user",
                                            "content": "You either added unnecessary text or formatted incorrectly. Do not do that with the next generation."})
                        pass

    except Exception as e:
        print(e)
        pass


