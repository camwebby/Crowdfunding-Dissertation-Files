from datetime import datetime
import pandas as pd
import requests
import json
import csv

print('Reading URLS')

#retrieve projects to scrape
with open('project urls.csv') as f:
    reader = csv.reader(f)
    projects = [row for row in list(reader)][0]

#read the existing data file
datafile = pd.read_csv('flow_data.csv')

number_of_rows = len(datafile.index)
new_row_count = 0

print('Starting scraping')

#Iterature through the projcets scraping the data
for i, project in enumerate(projects):
    stats_json_response = requests.get(project+'/stats.json')

    data = stats_json_response.json()

    column_to_write = number_of_rows + 1 + new_row_count
    
    #write data to new row
    datafile.at[column_to_write, 'id'] = data['project']['id']
    datafile.at[column_to_write, 'link'] = project
    datafile.at[column_to_write, 'state'] = data['project']['state']
    datafile.at[column_to_write, 'backers_count'] = data['project']['backers_count']
    datafile.at[column_to_write, 'comments_count'] = data['project']['comments_count']
    datafile.at[column_to_write, 'comments_for_display_count'] = data['project']['comments_for_display_count']
    datafile.at[column_to_write, 'pledged'] = data['project']['pledged']
    datafile.at[column_to_write, 'datetime'] = datetime.now()

    new_row_count += 1

#write to csv
datafile.to_csv('flow_data.csv', index=False)

print('{} new rows added. Scraping finished'.format(new_row_count - number_of_rows))