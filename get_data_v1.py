from re import findall
import requests
from bs4 import BeautifulSoup

# url = 'https://lienminh.fandom.com/wiki/Fizz'
# page = requests.get(url)

# soup = BeautifulSoup(page.content, 'html.parser')
# # print(soup.prettify())

# # with open('fizz.txt', 'w') as f:
# #     f.write(soup.prettify())
# #     f.close()

# td = soup.find_all('td', attrs={'style':"white-space: nowrap; font-size:140%; color: #9797fc; font-weight:bold; text-shadow: 0 2px black; padding-right:14px;"})
# for text in td:
#     print(text.get_text())

def buildLinks(link):
    url = 'https://lienminh.fandom.com'
    return url + link


def getAllChampURLs():
    url = 'https://lienminh.fandom.com/wiki/Wikia_Li%C3%AAn_Minh_Huy%E1%BB%81n_Tho%E1%BA%A1i'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    champ_table = soup.find(id='roster')
    all_a = champ_table.find_all('a')
    
    # print('total champs:', len(all_a))
    
    # print(champ_table)
    # print(links)
    
    # print(soup)
    
    champ_urls = []
    print('len:',len(all_a))
    for i, a in enumerate(all_a):
        champ = a['href']
        champ_urls.append(champ)
        # print(i,a['href'])
    
    # print(*links)
    
    all_champ_urls = list(map(buildLinks, champ_urls))
    
    # print(*list(all_champ_urls))
    # for i, champ in enumerate(all_champ_urls):
    #     print(i, champ)
    
    return all_champ_urls
    

def buildJson(champ_urls):
    abilities_list = []
    for i in range(len(champ_urls)):
        url = champ_urls[i]
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())

        # with open('fizz.txt', 'w') as f:
        #     f.write(soup.prettify())
        #     f.close()
        
        champNames = soup.find_all(id='championName')
        td = soup.find_all('td', attrs={'style':"white-space: nowrap; font-size:140%; color: #9797fc; font-weight:bold; text-shadow: 0 2px black; padding-right:14px;"})
        
        for champ in champNames:
            print(champ.get_text(),':')
            for text in td:
                # print(text.get_text())
                text = text.get_text()
                print(text)
            print('-----')
        
        
        
        
        
    
    

def main():
    all_champ_urls = getAllChampURLs()
    champsJson = buildJson(all_champ_urls)
    # writeToJson(all_champ_urls)
    

if __name__ == '__main__':
    main()
