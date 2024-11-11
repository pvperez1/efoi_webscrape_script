from bs4 import BeautifulSoup
import requests
import csv
import time


#Create CSV file
csv_file = open('foi_scrape11062019_Denied.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title','Agency','Requestor','Purpose','Coverage','Req ID','Status','Date Requested','Request Link'])
#Get website
url = input("Type in URL:")
source = requests.get(url).text
#with open('test.html') as source:
soup = BeautifulSoup(source,'lxml')

no_of_rec_h = soup.find('header', class_='section-subheader')
spans_in_h = no_of_rec_h.find_all('span')
no_of_recs = int(spans_in_h[0].text)
no_of_pages = no_of_recs // 50


#Get all record in first page
records = soup.find_all('div',class_='component-panel')

try:
    #then do the loop
    while no_of_pages > 0:
        #Get the div containing the record
        for record in records:
            #Get the column values
            rec_title = record.h4.a.text.strip()
            rec_description = record.find_all('span')
            rec_agency = rec_description[0].text
            rec_requestor = rec_description[1].text
            rec_purpose = rec_description[2].text
            rec_coverage = rec_description[3].text
            rec_tracking = rec_description[4].text
            rec_status = record.label.text.strip()
            rec_request_date = record.p['title']
            rec_link = 'https://www.foi.gov.ph' + record.h4.a['href']
            #write to CSV file
            csv_writer.writerow([rec_title, rec_agency, rec_requestor, rec_purpose, rec_coverage, rec_tracking, rec_status, rec_request_date, rec_link])
            #end of for loop
        #continuing the while loop    
        tab_pane = soup.find('div',class_='col-xxs-12 col-xs-12 col-sm-8')
        links = tab_pane.find_all('a')
        for link in links:pass
        next_link = 'https://www.foi.gov.ph' + link['href']
        print(next_link)
        print(no_of_pages)
        no_of_pages = no_of_pages - 1
        time.sleep(0.1)
        url = next_link
        source = requests.get(url).text
        soup = BeautifulSoup(source,'lxml')
        records = soup.find_all('div',class_='component-panel')
        #end of while loop
except:
    print("Something went wrong")
    csv_file.close()
finally:
    #Close CSV File
    csv_file.close()