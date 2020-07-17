import json
import requests
from bs4 import BeautifulSoup
import traceback



# Get html of the webpage
session = requests.Session()
my_headers = {"User-Agent":'Mozilla/5.0'}

url = 'https://www.w3schools.com/python/'
response = session.get(url, headers=my_headers)
soup = BeautifulSoup(response.text, 'html.parser')

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
                
                page_response = session.get(page_url, headers=my_headers)
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                headers = page_soup.find(id='main')
                
                current_header = None
                for header in headers.contents:
                    if header.name == 'h2': 
                        current_header = header.text
                        data[name]['info'][header.text] = ''
                    
                    elif current_header != None:
                        if header.name == 'p':
                            text = header.text
                            text = text.replace('\n', '')
                            text = text.replace('\r', '')
                            text = text.replace('**', '`**`')
                            text = text.replace('__', '`__`')
                            data[name]['info'][current_header] += text

                        if header.name == 'div':

                            header_str = str(header)
                            section_soup = BeautifulSoup(header_str, 'html.parser')
                            example = section_soup.find(class_='w3-example')

                            if example != None: 
                                for code in example.contents:
                                    if code.name == 'div':
                                        # Convert br to '\n'
                                        code = BeautifulSoup(str(code), 'html.parser')
                                        code_text = ''
                                        
                                        for br in code.find_all('br'):
                                            
                                            br.replace_with("\n")

                                        # Store code
                                        code_text = code.text.replace('\r\n  ', '')
                                        code_text = code_text.rstrip().lstrip()
                                        data[name]['info'][current_header] += '```py\n'+code_text+'```'                          

        except: 
            traceback.print_exc()


    with open('python_data2.json', 'w') as f:
        json.dump(data, f, indent=4)

generate_data()