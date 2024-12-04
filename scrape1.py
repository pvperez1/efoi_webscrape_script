from bs4 import BeautifulSoup
import requests
import csv
import time
import urllib3

# Introducing myself and getting the website
url = input("Type in URL:")
header = {"User-Agent": "Paul Jason Perez (pvperez1@uw.edu)"}
request = urllib3.request(url, None, header)
response = urllib3.urlopen(request)
soup = BeautifulSoup(response.read())

#Create CSV file
csv_file = open('foi_scrape11272024-2.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title','Agency','Initial','Purpose','Coverage','Req ID','Status','Date Requested','Request Link'])


#get the total number of records as displayed from the website
no_of_rec_h = soup.find('header', class_='section-subheader')
spans_in_h = no_of_rec_h.find_all('b') 
no_of_recs = int(spans_in_h[1].text) #second span contains total number of records
no_of_pages = no_of_recs // 15 #because there are 15 records per page


#Get all record in first page
records = soup.find_all('div',class_='component-panel')

next_page = 11540
try:
    #then do the loop
    while no_of_pages > 0:
        #Get the div containing the record
        for record in records:
            #Get the column values
            rec_title = record.h4.a.text.strip()
            rec_description = record.find_all('span')
            rec_agency = rec_description[0].text
            rec_agency_initial = rec_description[1].text
            rec_purpose = rec_description[3].text
            rec_tracking = rec_description[4].text
            rec_status = record.label.text.strip()
            rec_request_date = record.p['title']
            rec_link = 'https://www.foi.gov.ph' + record.h4.a['href']
            #write to CSV file
            csv_writer.writerow([rec_title, rec_agency, rec_agency_initial, rec_requestor,rec_purpose, rec_tracking, rec_status, rec_request_date, rec_link])
            #end of for loop
        #continuing the while loop
        next_link = 'https://www.foi.gov.ph/requests/page/' + str(next_page) + '/'
        next_page += 1
        print(next_link)
        print(no_of_pages)
        no_of_pages -= 1
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