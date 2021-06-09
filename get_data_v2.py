from os import write
from bs4 import BeautifulSoup
import requests
import json

homepage = 'https://lienminh.garena.vn/champions/'
base_url = 'https://lienminh.garena.vn'

# Get a list of all champion links
def getAllChampLinks():
    page = requests.get(homepage)
    soup = BeautifulSoup(page.content, 'html.parser')

    boxes = soup.find_all(class_='box')
    all_champ_urls = []
    # print("total:", len(boxes))
    for box in boxes:
        all_champ_urls.append(base_url +  box['href'])
    print(f'Retrieved {len(all_champ_urls)} links')

    return all_champ_urls

# Get each champ's abilities
def getAbilities(champ):
    # url = 'https://lienminh.garena.vn/champions/Leblanc'
    url = champ
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # print(page.content)
    
    # f = open('zed.txt', 'w')
    # f.write(str(soup))
    # f.close()
    
    full_html = str(soup)
    
    start_index = 0
    stop_index = 0
    
    for i in range(len(full_html)):
        if full_html[i:i+7] == 'spells:':
            start_index = i + 7
        if full_html[i:i+10] == ',breadData':
            stop_index = i
            
    # print(full_html[start_index:stop_index])
    # champHTML = full_html[start_index:stop_index] + ']'
    champ_html = full_html[start_index:stop_index].split(',')
    # print('champ html:', champ_html)
    
    # Order: [Q, W, E, R, Passive]
    abilities = []
    descriptions = [] # BUGGED!
    
    print('\n----\n')
    
    for i in range(len(champ_html)):
        line = champ_html[i]
        # print(i, line)
        ability = {}
        if 'name:' in line:
            ability = line[line.find("\"")+1:-1]
            abilities.append(ability)
        if 'description:' in line:
            if '."' in champ_html[i+1]:
                description = line[line.find("\"")+1:] + "," + champ_html[i+1][:-1]
            else:
                description = line[line.find("\"")+1:-1]
            descriptions.append(description)
    
    # print('ABILITIES:', abilities)
    # print('DESCRIPTIONS:', descriptions)
        
    # print('len:', len(champ_html))
        
    
    # champJson = ast.literal_eval(champHTML)
    # print(type(champJson))
    
    # zed_json = json.loads(champHTML)
    # print(zed_json)
    
    
    return abilities
    
    
    
def buildJson(all_champ_urls):
    championJson = []
    for url in all_champ_urls:
        champion = {}
        champion['name'] = url[url.rfind('/')+1:]
        champion['abilities'] = getAbilities(url)
        print(champion)
        championJson.append(champion)
    # print(championJson)
    return championJson


def writeToFile(champJson):
    print(f"Finished retrieving {len(champJson)} champions' spells!")

    choice = input("Press the Enter key to write downloaded data to 'lienminh.json' file, anything else to abort: ")

    if choice == "":
        champ_obj = json.dumps(champJson, indent=4, ensure_ascii=False)
        with open('lienminh.json', 'w', encoding='utf8') as f:
            f.write(champ_obj)
            f.close()
            print("Write to 'lienminh.json' successfully!")
    else:
        print("Aborted")
        exit()



def main():
    all_champ_urls = getAllChampLinks()
    # all_abilities = getAbilities('https://lienminh.garena.vn/champions/Yorick')
    championJson = buildJson(all_champ_urls)
    writeToFile(championJson)


    
if __name__ == '__main__':
    main()