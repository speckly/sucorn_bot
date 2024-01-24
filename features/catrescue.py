from ntpath import basename
from requests import get
import os
try: 
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    if input(f"BeautifulSoup4 is required to run this program, execute pip install bs4? (Y): ").lower().strip() in ["", "y"]:
        os.system(f"pip install bs4")
    else:
        exit()
import re

def catRescue(URL: str) -> list:
    """
Author: @speckly
https://github.com/speckly

-- Cat Rescue --
This gets the full image of the nya nya nyan (i mean ) from a Bing Image AI link with 1-4 nya images nyan
Uses Beautiful Soup 4

-- Inputs --
URL of the collage nyan

-- Process --
Legacy: Individual full href can be found on <a class="iusc">. Opens the href and extracts the full URL.

Eliminates the parameter that shrinks the image with class "mimg" and therefore not requiring to open the full URL

-- Outputs --
List of embeddable hrefs of nyan, nyan be used in Discord, master."""

    rawHTML: bytes = get(URL).text
    soup: BeautifulSoup = BeautifulSoup(rawHTML, "html5lib")
    PREFIX = "https://th.bing.com/th/id/"

    # Don't worry about memory, its just up to 4 links
    elements = soup.find_all('img', class_='mimg') #get elements
    if not elements:
        elements = soup.find_all('img', class_='gir_mmimg') #get elements
    full_links = [link.get('src') for link in elements]
    #Thanks OpenAI for the regex for ID
    pattern = r'id/([^/?]+)'
    links = [PREFIX + re.search(pattern, url).group(1) for url in full_links]

    # Assume only one element, I dont know why firefox shows input while here it is textarea
    textinput = soup.find('textarea', {'id': 'sb_form_q'})
    if textinput:
        prompt = textinput.text
    else:
        prompt = ''

    return links, prompt

def catDownloader(URL: str, folder_name: str, mode: str) -> str:
    """
Author: @speckly
https://github.com/speckly

-- Cat Downloader --
Simple downloading of images customized for the use with the sucorn bot, triggered when the Discord buttons
are clicked. NOTE: ASSUMES THAT THE PAGE DOES NOT RETURN HTML BUT ONLY JPG!!!!!!!!

-- Inputs --
URL embedded in Discord and the folder_name which is the Discord channel name

-- Process --
Use requests

-- Outputs --
Response messages"""
    message = ""
    os.chdir('C:\\Users\Dell\OneDrive - Singapore Polytechnic\Documents\compooting\CScraper-SpeckOS\sucorn_bot\images') # SENSTIVE!!!!!!!!!!
    try:
        if not os.path.exists(f'{folder_name}'):
            # If it doesn't exist, create the directory
            os.makedirs(f'{folder_name}')
            message += ", Directory created"
        
        response = get(URL)
        if response.status_code == 200:
            URL = basename(URL)
            query_start = URL.find('?')
            file_name = URL[:query_start] if query_start != -1 else URL # Get rid of parameters
            path = f'{folder_name}/{file_name}'
            for filename in os.listdir(folder_name):
                if filename.startswith(file_name):
                    message += f", Image {file_name} already exists"
                    return message[2:]
            with open(f'{path}_{mode[:-1]}.jpg', 'wb') as file: # Mode Posneg(1-4)
                file.write(response.content)
            message += ", Saved successfully"
        else:
            message += ", **Request failed**"

        return message[2:]
    except:
        return "**Unknown error**"

if __name__ == "__main__":
    SAMPLE_URL = "https://www.bing.com/images/create/colored-drawing-of-an-anime-girl-with-cat-ears-and/1-6580752df8ad4d05ae377fd4cbd0482e?FORM=GENCRE"
    # print(catRescue(SAMPLE_URL))
    print(catDownloader("https://th.bing.com/th/id/OIG.AS.gbMFww.HfRikyMMdB", "testfrommain"))
