import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as palm
from streamlit_extras.add_vertical_space import add_vertical_space

def set_background():
    
    page_bg_img = '''
            <style>
            .stApp {
    background: rgb(2,0,36);
    background: linear-gradient(170deg, rgba(2,0,36,1) 9%, rgba(121,9,71,1) 45%, rgba(0,212,255,1) 100%);
            }
            </style>
            ''' 
    st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Wikipedia Summarizer 💭') #title
#SIDEBAR
with st.sidebar:
    set_background()
    st.markdown('''     
    ## About 🙋🏻‍♂️
    This is a Wikipedia Summarizer
    Where you can upload a Wikipedia Link and download the summary:
                
    -Streamlit
                
    -Python
                
    -Google Palm
                
     ''') 
    add_vertical_space(15)
    st.write('Made with ❤️ by  [Abhishek S](https://github.com/iamA333)')

url=st.text_input("Enter the Wikipedia Link")
# page =requests.get(f"https://en.wikipedia.org/wiki/{url}")
if url:
    response = requests.get(url)

    # A check is performed to see if the request is sent successfully
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content
        content = soup.find('div', {'id': ['mw-content-text']})
        

        # Remove tables
        for table in content.find_all('table'):
            table.decompose()

        # Extract headings and paragraphs

        headings_and_paragraphs = content.find_all(['h1','h2', 'h3', 'p'])
        
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


    palm.configure(api_key="ENTER YOUR API KEY HERE")
    # Setting the prompt template for the AI model
    prompt_template = """
    Summarize the following text and ensure that all the important and key information is included in the summary.

    ```{text}```

    Summary:
    """
    summarized_text1 = {}

    # Generate the summary
    for i in range(len(headings_and_paragraphs)):
        if headings_and_paragraphs[i].name.startswith('h'):
            heading = headings_and_paragraphs[i].get_text()
            text = ''
            for j in range(i + 1, len(headings_and_paragraphs)):
                
                if headings_and_paragraphs[j].name.startswith('h'):
                    break
                else:
                    text = headings_and_paragraphs[j].get_text()
                question = heading + '\n' + text
                prompt = prompt_template.format(text=question)
                summary = palm.generate_text(
                    model='models/text-bison-001',
                    prompt=prompt,
                    # The maximum length of the response
                    max_output_tokens=800,
                    # The lower the temperature, the more predictable the text
                    temperature=0.6,
                )
                text = summary.result
            summarized_text1[heading] = text
    # remove All the sections which do not provide any key information like: 'See also', 'References', 'Notes', 'Citations', 'Sources', 'Further reading', 'External links' from the dictionary
    summarized_text1 = {k:v for k,v in summarized_text1.items() if k not in ['See also', 'References', 'Notes', 'Citations', 'Sources', 'Further reading', 'External links','Bibliography','Politics','Articles','Books','Other','Lists','Official','Audiobooks']}

    with open('alexander_summarized.txt', 'w', encoding='UTF-8') as f:
        for heading, summary in summarized_text1.items():
            f.write(f"\n{heading}\n")
            f.write(f"{summary}\n")
        
    with open('alexander_summarized.txt') as f:
            st.download_button('Download Summary', f)