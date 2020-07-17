import json
import requests
from bs4 import BeautifulSoup
import traceback



# Get html of the webpage
session = requests.Session()
# Windows 10 with Google Chrome
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'
heading = { 'User-Agent': user_agent_desktop}
url = 'https://www.w3schools.com/python/'
response = session.get(url, headers=heading)
soup = BeautifulSoup(response.text, 'lxml')

python = soup.find(id="leftmenuinnerinner")

def generate_data():
    data = {}

    for p in python.contents:
        try: 
            if p.name == 'a' and p.text.startswith('Python'): 
                title = p.text
                page_url = url+p['href']
                name = title.replace('Python','').lower()
                name = name.replace(' ', '')
                data[name] = {'title': title, 'url': page_url, 'info': dict()}
                
                page_response = session.get(page_url, headers=heading)
                page_soup = BeautifulSoup(page_response.text, 'lxml')
                headers = page_soup.find(id='main')
                
                current_header = None
                for header in headers.contents:

                    if header.name == 'h2': 
                        current_header = header.text
                        if current_header == "Test Yourself With Exercises": break
                        data[name]['info'][header.text] = ''
                    
                    elif current_header != None:
                        if header.name == 'p':
                            text = header.text
                            text = text.replace('\n', '')
                            text = text.replace('\r', '')
                            text = text.replace('**', '`**`')
                            text = text.replace('__', '`__`')
                            data[name]['info'][current_header] += text

                        elif header.name == 'div':

                            section_soup = BeautifulSoup(str(header), 'lxml')
                            example = section_soup.find('div', class_='w3-example')

                            if example != None: 
                                code_stuff = BeautifulSoup(str(example), 'lxml')
                                code = code_stuff.find('div', class_='w3-code')

                                

                                # Convert br to '\n'
                                code = BeautifulSoup(str(code), 'lxml')
                                
                                for br in code.find_all('br'):
                                    br.replace_with("\n")

                                # Store code
                                code_text = code.getText()
                                code_text = code_text.replace('\u00a0', ' ')
                                code_text = code_text.replace('\r\n  ', '')
                                code_text = code_text.replace('\r\n\t', '\t')
                                code_text = code_text.replace('\t \t', '\t')
                                code_text = code_text.replace('\t \t', '\t')
                                code_text = code_text.replace('\n\n', '\n')
                                data[name]['info'][current_header] += '```py\n'+code_text+'```'                          

        except: 
            traceback.print_exc()


    with open('python_data.json', 'w') as f:
        json.dump(data, f, indent=4)

generate_data()