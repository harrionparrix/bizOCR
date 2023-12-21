
import easyocr
import pandas as pd
reader = easyocr.Reader(['en'], gpu=True)
import spacy
nlp = spacy.load("en_core_web_trf")
import re


phone_pattern = r'\b(?:Phone:|Cell:|Cellular:|Tel:|Fax:|fFtT)?\s*([0-9+-]{6,12})\b'
name_pattern = r"^(?:Mr\.|Mrs\.|Dr\.|[a-zA-Z'\-,.][^0-9_!¡?÷?¿/\\+=@#$%^&*(){}|~<>;:[\]]{2,})$"
website_pattern = r"^(?:www\.[^\s.]+\.[a-zA-Z]{2,}|[^\s]+\.(?:com))$"
address_pattern = r"^[0-9A-Za-z\s,.-]+$"
designation_pattern = re.compile(r'(?i)\b(manager|director|engineer|analyst|supervisor|specialist|coordinator|administrator|consultant|executive)\b')


def checkName(val):
    if re.match(name_pattern, val):
        return True
    return False
def checkPhone(val):
    if re.match(phone_pattern, val):
        return True
    return False
def checkPhoneTwo(val):
    phone_pattern = re.compile(r'\b(?:Phone|Cell|Tel|P|T)?\s*(?:\+?\d{1,2}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    if re.findall(phone_pattern,val):
        return True 
    return False
def checkEmail(val):
    return '@' in val
def checkWebsite(val):
    if re.search(website_pattern, val):
        return True
    return False
def checkAddress(val):
    if re.search(address_pattern, val):
        return True
    return False
def checkDesignation(val):
    return bool(designation_pattern.search(val))

def getInfo(e):
    company_names = []
    person_names = []
    phone_numbers = []
    emails = []
    addresses = []
    designation = []
    txt=""
    for val in e:
        doc = nlp(val)
        txt += val
        if checkEmail(val):
            split_result = val.split(" : ", 1)
            if len(split_result) > 1:
                result = split_result[1]
            else:
                result = val
                emails.append(result)
        if checkDesignation(val):
            designation.append(val)   
        for ent in doc.ents:
                if ent.label_ == 'ORG':
                    company_names.append(val)
                if ent.label_ == 'PERSON' and checkName(val) and not checkEmail(val):
                    person_names.append(val)
                if ent.label_ == 'GPE' and not checkDesignation(val):
                    addresses.append(val)
                if ent.label_ == 'CARDINAL' and checkPhone(val):
                    phone_numbers.append(val)
        if(checkName(val) and val.isupper()):
            person_names.append(val) 
        if(checkPhoneTwo(val) and phone_numbers.count(val)==0):
                    phone_numbers.append(val)
        disable_pipe= [pipe for pipe in nlp.pipe_names if pipe!= 'ner']

    return company_names, person_names, phone_numbers,emails,addresses,designation


def process_ocr(filename):
    img=filename
    dfs = []
    result = reader.readtext(img)
    img_id = img.split('/')[-1].split('.')[0]
    img_df = pd.DataFrame(result, columns=['bbox','text','conf'])
    img_df['img_id'] = img_id
    dfs.append(img_df)
    easyocr_df = pd.concat(dfs)
    company,person_name,phone,email,address,designation=getInfo(easyocr_df['text'])
    return (filename,company,person_name,phone,email,address,designation)
