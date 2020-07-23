import json
import requests
from bs4 import BeautifulSoup
import traceback


def generate_data(page_name:str):
    topic_blacklist = ['certificate', 'exercises', 'quiz', 'examples', 'templates', 'home', 'intro', 'compiler', 'introduction', 'glossary']

    data = {}
    # Set url
    url = 'https://www.w3schools.com/{}/'.format(page_name)

    # Get the sidebar's html
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = soup.find(id="leftmenuinnerinner")

    # Get all topics
    topics = BeautifulSoup(str(sidebar), 'lxml')
    topics_names = topics.find_all('a')

    for topic in topics_names:
        try: 
            # Get the title of topic
            title = topic.text
            name = title.lower().replace(page_name,'')
            name = name.replace(' ', '')
            if name in topic_blacklist: continue

            # Get url of topic
            if topic['href'].startswith('/'): continue
            page_url = url + topic['href']

            # Init data key
            if not name in data: data[name] = {'title': title, 'url': page_url, 'info': dict()}
            
            # Get contents of topic
            page_response = session.get(page_url)
            page_soup = BeautifulSoup(page_response.text, 'lxml')
            headers = page_soup.find(id='main')
            
            # If page doesnt have relevant info
            if headers == None: 
                print(page_url,'has no relevant content.')
                continue

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
                        text = text.replace('*', '\*')
                        text = text.replace('_', '\_')
                        data[name]['info'][current_header] += text

                    elif header.name == 'div':

                        section_soup = BeautifulSoup(str(header), 'lxml')
                        example = section_soup.find('div', class_='w3-example')

                        if example != None: 
                            code_stuff = BeautifulSoup(str(example), 'lxml')
                            code = code_stuff.find('div', class_='w3-code')
                            if code == None: code = code_stuff.find('pre', class_='w3-white')

                            # No code
                            if code == None: continue

                            # Convert br to '\n'
                            code = BeautifulSoup(str(code), 'lxml')
                            
                            for br in code.find_all('br'):
                                br.replace_with("\n")

                            # Store code
                            code_text = code.getText().rstrip().lstrip()
                            code_text = code_text.replace('\u00a0', ' ')
                            code_text = code_text.replace('\r\n  ', '')
                            code_text = code_text.replace('\r\n\t', '\t')
                            code_text = code_text.replace('\t \t', '\t')
                            code_text = code_text.replace('\t \t', '\t')
                            code_text = code_text.replace('\n\n', '\n')

                            if len(code_text) + len(data[name]['info'][current_header]) > 1024: continue

                            data[name]['info'][current_header] += '```{}\n{}```'.format(page_name, code_text)                        

        except: 
            traceback.print_exc()

    return data


# init data storage
all_data = {}

# Get html of the webpage
session = requests.Session()
page_names = ['python', 'css', 'js', 'html', 'cpp', 'cs', 'sql', 'react', 'jquery', 'php', 'java']

# Get all data for each page
for page_name in page_names:
    print('Getting data for page', page_name+'...')
    all_data[page_name] = generate_data(page_name)


# Save to json
print('Saving data to code_data.json...')
with open('code_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print('Done!')