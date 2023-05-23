import requests
from csv import writer
from bs4 import BeautifulSoup as bs
from time import sleep
from tqdm import tqdm
import random
from dotenv import load_dotenv, find_dotenv
import os

crawl_ID = input("Crawl_ID:")

try:
    load_dotenv(find_dotenv())
except:
    print("File .env mancante")

def apiReq(crawl_ID, api_key):
    url = "https://partner.archive-it.org/api/reports/crawled-detail/" + crawl_ID + "?format=csv&mimetype=text/html"
    payload={}
    api_headers = {
        'Authorization': api_key
    }
    api_res = requests.request("GET", url, headers=api_headers, data=payload)
    api_data = bs(api_res.text, 'html.parser')
    return api_data

def docReq(doc_url):
    user_agents = [
        "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    ]
    random_user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': random_user_agent,
        'lang': 'it-IT',
        'Connection': 'Close'
    }
    try:
        page = requests.request("GET", doc_url, headers=headers, timeout=3)
    except:
        raise Exception()
    soup = bs(page.text, 'html.parser')
    return soup

with open(crawl_ID + '_document_metadata.csv', 'w+', encoding='utf8') as csv_file:
    
    api_key = os.environ.get("API_KEY")

    thewriter = writer(csv_file)
    headerow = ['Identifier', 'Title', 'Creator', 'Publisher', 'Date', 'Description', 'Language', 'Subjects', 'Format', 'Type', 'Relation', 'Rights', 'Source', 'PDF', 'DOI']
    thewriter.writerow(headerow)
    
    try:
        rows = apiReq(crawl_ID, api_key).text.split('\n')
    except:
        print('Errore di connessione')

    for record in tqdm(rows, desc="Crawl "+ crawl_ID, bar_format='{l_bar}{bar} {n_fmt}/{total_fmt} [~{remaining}{postfix}]'):
        
        try:
            doc_url = record.split(',')[0]
            doc_source = record.split(',')[3].replace('\n', "").strip()
        except:
            continue

        if (record.split(',')[2] == '0' and doc_source in doc_url):

            title = ""
            creator = ""
            publisher = ""
            date = ""
            description = ""
            language = ""
            subject = ""
            dc_type = ""
            relation = ""
            rights = ""
            pdf = ""
            doi = ""

            try:
                soup = docReq(doc_url)
            except:
                continue

            # DC:TITLE
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'citation_title'})]
                    title = ", ".join(title)               
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'DC.Title'})]
                    title = ", ".join(title)
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'DC.title'})]
                    title = ", ".join(title)               
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'dcterms.title'})]
                    title = ", ".join(title)               
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'DCTERMS.title'})]
                    title = ", ".join(title)              
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'property':'og:title'})]
                    title = ", ".join(title)         
                except: title = ""
            if title == "":
                try:
                    title = [title['content'] for title in soup.find_all("meta", attrs={'name':'title'})]
                    title = ", ".join(title)             
                except: title = "" 
            if title == "":
                try:
                    title = soup.title.text.replace("\r\n", " ").replace("&nbsp;", "").replace('<br>', '').strip()
                except: title = ""
            if title == "":
                continue


            # DC:CREATOR
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'DC.Creator.PersonalName'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'DC.Creator'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'DC.creator'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'dcterms.creator'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'DCTERMS.creator'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'DCterms.creator'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'citation_author'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'property':'article:author'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'author'})]
                    creator = ", ".join(creator)
                except: creator = ""
            if creator == "":
                try:
                    creator = [creator['content'] for creator in soup.find_all("meta", attrs={'name':'creator'})]
                    creator = ", ".join(creator)
                except: creator = ""        
            
            # DC:PUBLISHER
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'name':'DC.Publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'name':'DC.publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'name':'dcterms.publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'name':'DCTERMS.publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'name':'citation_publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'property':'article:publisher'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""
            if publisher == "":
                try:
                    publisher = [publisher['content'] for publisher in soup.find_all("meta", attrs={'property':'og:site_name'})]
                    publisher = ", ".join(publisher)
                except: publisher = ""


            # DC:DATE
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'DC.Date.created'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'DC.Date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'DC.date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'dcterms.date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'DCTERMS.date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'citation_publication_date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'name':'citation_date'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'property':'article:published_time'})['content']
                except: date = ""
            if date == "":
                try:
                    date = soup.find("meta", attrs={'property':'article:modified_time'})['content']
                except: date = ""
            

            # DC:DESCRIPTION
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'DC.Description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'DC.description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'DC.description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'dcterms.description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'DCTERMS.description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'dcterms.description', 'xml:lang':'it'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'dcterms.abstract'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'DCTERMS.abstract'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'property':'og:description'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'description'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            if description == "":
                try:
                    description = soup.find("meta", attrs={'name':'citation_abstract'})['content'].replace("&#xD;&#xA;", " ").replace("\r\n", " ").strip()
                except: description = ""
            
            
            # DC:LANGUAGE
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'DC.Language'})['xml:lang'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'DC.language'})['xml:lang'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'DC.Language'})['content'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'DC.Language'})['content'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'dcterms.language'})['xml:lang'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'dcterms.language'})['content'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'citation_language'})['content'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'name':'og:locale'})['content'].strip()
                except: language = ""
            if language == "":
                try:
                    language = soup.find("meta", attrs={'http-equiv':'content-language'})['content'].strip()
                except: language = ""  


            # DC:SUBJECTS
            if subject == "":
                try:
                    subject = [subject['content'] for subject in soup.find_all("meta", attrs={'name':'DC.Subject', 'xml:lang':'it'})]
                    subject = ", ".join(subject)
                except:
                    subject = ""
            if subject == "":
                try:
                    subject = [subject['content'] for subject in soup.find_all("meta", attrs={'name':'DC.subject', 'xml:lang':'it'})]
                    subject = ", ".join(subject)
                except:
                    subject = ""
            if subject == "":
                try:
                    subject = [subject['content'] for subject in soup.find_all("meta", attrs={'name':'DC.Subject'})]
                    subject = ", ".join(subject)
                except:
                    subject = ""
            if subject == "":
                try:
                    subject = [subject['content'] for subject in soup.find_all("meta", attrs={'name':'DC.subject'})]
                    subject = ", ".join(subject)
                except:
                    subject = ""
            if subject == "":
                try:
                    subject = soup.find("meta", attrs={'name':'citation_keywords'})['content'].strip()
                except:
                    subject = ""
            if subject == "":
                try:
                    subject = soup.find("meta", attrs={'name':'keywords'})['content'].strip()
                except:
                    subject = ""

            # DC:FORMAT
            try:
                dc_format = doc_url.split(".")[1].upper()
            except:
                dc_format = "HTML"

            # DC:TYPE
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'name':'DC.Type'})['content'].strip()
                except:
                    dc_type = ""
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'name':'DC.type'})['content'].strip()
                except:
                    dc_type = ""
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'name':'dcterms.type'})['content'].strip()
                except:
                    dc_type = ""
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'name':'DCTERMS.type'})['content'].strip()
                except:
                    dc_type = ""
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'name':'DC.Type.articleType'})['content'].strip()
                except:
                    dc_type = ""
            if dc_type == "":
                try:
                    dc_type = soup.find("meta", attrs={'property':'og:type'})['content'].strip()
                except:
                    dc_type = ""


            # DC:RELATION
            if relation == "":
                try:
                    relation = soup.find("meta", attrs={'name':'DC.Relation'})['content'].strip()
                except:
                    relation = ""
            if relation == "":
                try:
                    relation = soup.find("meta", attrs={'name':'DC.relation'})['content'].strip()
                except:
                    relation = ""
            if relation == "":
                try:
                    relation = soup.find("meta", attrs={'name':'dcterms.relation'})['content'].strip()
                except:
                    relation = ""
            if relation == "":
                try:
                    relation = soup.find("meta", attrs={'name':'DCTERMS.relation'})['content'].strip()
                except:
                    relation = ""
            if relation == "":
                try:
                    relation = soup.find("meta", attrs={'name':'citation_journal_title'})['content'].strip()
                except:
                    relation = ""

            # DC:RIGHTS
            if rights == "":
                try:
                    rights = [rights['content'] for rights in soup.find_all("meta", attrs={'name':'DC.Rights'})]
                    rights = ", ".join(rights)
                except:
                    rights = ""
            if rights == "":
                try:
                    rights = [rights['content'] for rights in soup.find_all("meta", attrs={'name':'DC.rights'})]
                    rights = ", ".join(rights)
                except:
                    rights = ""
            if rights == "":
                try:
                    rights = [rights['content'] for rights in soup.find_all("meta", attrs={'name':'dcterms.rights'})]
                    rights = ", ".join(rights)
                except:
                    rights = ""
            if rights == "":
                try:
                    rights = [rights['content'] for rights in soup.find_all("meta", attrs={'name':'DCTERMS.rights'})]
                    rights = ", ".join(rights)
                except:
                    rights = ""

            
            # DC:SOURCE
            try:
                source = soup.find("meta", attrs={'name':'DC.Source'})['content'].strip()
            except: source = ""
            if source == "":
                try:
                    source = soup.find("meta", attrs={'name':'DC.source'})['content'].strip()
                except: source = ""
            if source == "":
                try:
                    source = soup.find("meta", attrs={'name':'dc.source'})['content'].strip()
                except: source = ""
            if source == "":
                source = doc_source


            # PDF LINK
            if pdf == "":
                try:
                    pdf = soup.find("meta", attrs={'name':'citation_pdf_url'})['content'].strip()
                except: pdf = ""

            # DOI
            if doi == "":
                try:
                    doi = soup.find("meta", attrs={'name':'DC.Identifier.DOI'})['content'].strip()
                except: doi = ""
            if doi == "":
                try:
                    doi = soup.find("meta", attrs={'name':'citation_doi'})['content'].strip()
                except: doi = ""

            metadata = [
                doc_url, 
                title.replace(u'\n', u' ').replace(u'\t', u''), 
                creator.replace(u'\xa0', u' '), 
                publisher, 
                date, 
                description.replace(u'\n', u' ').replace(u'\t', u' '), 
                language, 
                subject, 
                dc_format, 
                dc_type, 
                relation, 
                rights, 
                source, 
                pdf, 
                doi
            ]
            thewriter.writerow(metadata)
            
            if pdf != "":
                pdf_url = pdf
                dc_pdf_format = "PDF"
                pdf_metadata = [pdf_url, title, creator, publisher, date, description, language, subject, dc_pdf_format, dc_type, relation, rights, source, "", doi]
                thewriter.writerow(pdf_metadata)

            sleep(0.1)
        else:
            continue

print("Operazione completata")




