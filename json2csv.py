import json
import csv
 
# Opening JSON file and loading the data
# into the variable data
with open('cameras.json') as json_file:
    data = json.load(json_file)
 
features = data['features']
 
# now we will open a file for writing
csv_file = open('cameras.csv', 'w')
 
# create the csv writer object
csv_writer = csv.writer(csv_file)

 # Counter variable used for writing
# headers to the CSV file
count = 0
 
for feature in features:
    properties = feature['properties']
    if count == 0:
        # Writing headers of CSV file
        header = properties.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(properties.values())
 
csv_file.close()