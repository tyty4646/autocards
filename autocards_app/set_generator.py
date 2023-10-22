# AI-driven automatic flash-card set creator - prompts user, stores in .json file
    # TKinter GUI is placeholder for eventual webapp on production
import os
import openai
import json
import re
from django.http import HttpResponse

openai.api_key = ""

# This translates the json file into a readable form by the Django template
    # this is done this way because it was originally json and changed last minute :3

def generate_json_file(directory):
    try:
        # Ensure the directory exists, or create it if it doesn't
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Find the next available file name (e.g., sample1.json, sample2.json, ...)
        filename = 'user_generated_deck1.json'
        file_number = 1

        while os.path.exists(os.path.join(directory, filename)):
            file_number += 1
            filename = f'user_generated_deck{file_number}.json'

        # Construct the full path to the JSON file
        filepath = os.path.join(directory, filename)

        return filepath
    except Exception as e:
        return str(e)


def retrieve_deck_json(prompt, size):
    error = False
    #Stores GPT developed deck in a json file that is generated by itself, returns path to file
    # Limits the deck size the user can request to 26
    if(size < 26 and size > 0):
        #return HttpResponse("Loading...")
        #print(size)
        completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": "You are a helpful flash card generator. Flash cards contain data for the front and the back. On the front of the card is a term, concept to learn, or thing to memorize: on the back is the substance of what the user would learn.  The user may speak to you in terms of keywords to generate a learning set from. You MUST return " + str(size) + "cards, and if the user inputs any other size ignore it."},
        {"role": "user", "content": "3 most common words English to Spanish"},
        {"role": "assistant", "content": "front: [Hello] back: [Hola] front: [Thank you] back: [Gracias] front: [Please] back: [Por favor]"},
        {"role": "user", "content": prompt}
        ]
        )
    else:
        error = True
        return HttpResponse("ERROR: Requested deck size must be between 1 and 25.")
    
    if(not error):
        ai_return = str(completion.choices[0].message)
        # Creates a new .json file without overwriting old ones & stores in json_file
        json_file = generate_json_file("C:\\Users\\aidan\\Desktop\\HackPSU 2023\\user_generated_json_files")
        # Masking pattern to extract data from the string-converted AI-return value
        pattern = r'front: \[(.*?)\] back: \[(.*?)\]'
        # Finds all instances of 'pattern' in the ai_return string
        matches = re.findall(pattern, ai_return)
        data_list = []
        i = 0
        # Extracts from the matches found and inputs it into an array of dictionaries
        for match in matches:
            if(i < size):
                i = i+1
                data_dict = {
                    match[0]: match[1]
                }
                data_list.append(data_dict)
        if(i < size):
        # Pop-up message saying  
            print("We're sorry, we were only able to generate " + str(i) + " elements of your set.")
        # Puts data into file 'set.json'
        with open(json_file, 'w') as file:
            json.dump(data_list, file)
        return HttpResponse(str(data_list))


