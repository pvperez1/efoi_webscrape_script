from bs4 import BeautifulSoup
import requests
import csv
import time


#read CSV File containing all the chat links
csv_filename = input("Type in CSV Filename:")
with open(csv_filename, mode='r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    #save the csv into a list
    link_list = list(reader)
    f.close()

#check number of links
print(len(link_list))

#Create CSV file
csv_file = open('foi_scrape_chats_denied_6_Nov_2019.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Req ID','Client Chats','Agency Chats','Final Agency Chat'])
#for debugging
print("Now entering loop")



try:
    for i in range(len(link_list)):
        #Get website
        url = link_list[i][8]
        print(url)
        print(i)
        source = requests.get(url).text
        soup = BeautifulSoup(source,'lxml')
        
        #get all chats divs
        chats = soup.find('div', class_='col-xxs-12 col-xs-12 col-sm-8')
        
        #Get all four important components from the chats div
        #chat_awaiting = chats.find('div', class_='component-panel awaiting mb10')
        chat_info = chats.find('div', class_='component-panel denied mb10')
        chat_client = chats.find_all('div',class_='component-message -client')
        chat_agency = chats.find_all('div',class_='component-message -agency')
        chat_denied = chats.find_all('div',class_='alert alert-danger')
        
        #get chat info
        print("getting info")
        #print(chat_info)
        chat_description = chat_info.find_all('span')
        chat_tracking = chat_description[4].text
        
        #write to CSV file
        csv_writer.writerow([chat_tracking, chat_client, chat_agency, chat_denied])
        
        #add delay
        time.sleep(1)

except:
    print("Something went wrong")
    csv_file.close()
finally:
    #Close CSV File
    csv_file.close()