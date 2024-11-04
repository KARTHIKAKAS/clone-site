import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

headers = {
    "authority": "www.ghmc.gov.in",
    "method": "POST",
    "path": "/Search.aspx",
    "scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Content-Length": "24864",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.ghmc.gov.in",
    "Priority": "u=1, i",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Gpc": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Microsoftajax": "Delta=true",
    "X-Requested-With": "XMLHttpRequest"
}

circles = {
    "1049": "1-Kapra",
    "1057": "2-Uppal",
    "1051": "3-Hayathnagar",
    "1062": "4-L B Nagar",
    "1064": "5-Saroornagar",
    "1004": "6-Malakpet",
    "1063": "7-Santoshnagar",
    "1065": "8-Chandrayangutta",
    "1005": "9-Charminar",
    "1066": "10-Falaknuma",
    "1054": "11-Rajendra Nagar",
    "1007": "12-Mehdipatnam",
    "1060": "13-Karwan",
    "1008": "14-Gosha Mahal",
    "1009": "15-Musheerabad",
    "1059": "16-Amberpet",
    "1010": "17-Khairatabad",
    "1058": "18-Jubilee Hills",
    "1067": "19-Yousufguda",
    "1055": "20-Serilingampally",
    "1012": "21-Chanda Nagar",
    "1013": "22-R C Puram and Patancheruvu",
    "1050": "23-Moosapet",
    "1061": "24-Kukatpally",
    "1053": "25-Qutbullapur",
    "1068": "26-Gajularamaram",
    "1047": "27-Alwal",
    "1052": "28-Malkajigiri",
    "1018": "29-Secunderabad"
}

def get_details(circle,name="",door=""):
    initial_url = "https://www.ghmc.gov.in/Search.aspx"
    initial_response = requests.get(initial_url)
    url = initial_url
    # Parse the initial response to get VIEWSTATE and other dynamic values
    soup = BeautifulSoup(initial_response.text, 'html.parser')
    viewstate = soup.find(id="__VIEWSTATE")['value']
    viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
    eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
    data = {
        "ctl00$ContentPlaceHolder1$ddlcircle": circle,  # Example value
        "ctl00$ContentPlaceHolder1$txtowner": name,  # Example value
        "ctl00$ContentPlaceHolder1$txtdoorno": door,  # Example value (empty in this case)
        "__VIEWSTATE": viewstate,  # Example value
        "__VIEWSTATEGENERATOR": viewstategenerator,  # Example value
        "__EVENTVALIDATION": eventvalidation,  # Example value
        "ctl00$ContentPlaceHolder1$btnsubmitotp": "Submit"
    }
    response = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
    
def filter_results(soup):
    pattern = re.compile(r'^ContentPlaceHolder1_grd')

    # Extracting all the relevant data
    results = []
    for tag in soup.find_all(id=pattern):
        results.append((tag.name, tag.get('id'), tag.text.strip()))

    table_data = []
    # Print the extracted data
    for result in results:
        if "span" in result:
            table_data.append(result)
    return table_data

def print_table(table_data):
    organized_data = []
    temp_data = {}
    for tag, id, text in table_data:
        index = id.split('_')[-1]
        key = id.split('_')[-2]
        if index not in temp_data:
            temp_data[index] = {}
        temp_data[index][key] = text

    for index in sorted(temp_data.keys(), key=int):
        organized_data.append((
            temp_data[index].get('lblPTINNO', ''),
            temp_data[index].get('lblowner', ''),
            temp_data[index].get('lbldoor', ''),
            temp_data[index].get('Label3', ''),
            temp_data[index].get('Label4', '')
        ))

    # Define the column names
    columns = ['PTIN NO', 'Owner Name', 'Door Number', 'Locality', 'Circle']

    # Print the data as a table
    # print(tabulate(organized_data, headers=columns, tablefmt='grid'))
    return organized_data