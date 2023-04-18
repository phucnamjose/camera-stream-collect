import csv
import json

# Function to convert a CSV to JSON
# Takes the file paths as arguments
def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8-sig') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader:
            data = {
                "properties" : row
            }
            #add this python dict to json array
            jsonArray.append(data)
            
        features = {
                "features": jsonArray
                }
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(features, indent=4)
        jsonf.write(jsonString)
         
# Decide the two file paths according to your
# computer system
csvFilePath = r'cameras_filtered_poorview.csv'
jsonFilePath = r'cameras_filtered_poorview.json'
 
# Call the make_json function
csv_to_json(csvFilePath, jsonFilePath)