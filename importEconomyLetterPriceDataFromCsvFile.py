import csv

# this is a base directory where all the data/csv files are kept
dataBaseDirectory = './/data//'

def importEconomyLetterPriceDataFromCsvFile(fileName):
    returnedDictionary = {}
    field_names = 'weight','zone 1','zone 2','zone 3','zone 4', 'zone 5'
    
    with open(dataBaseDirectory + fileName, 'r') as inputFile:
        inputFileReader = csv.DictReader(inputFile,fieldnames=field_names)

        for eachLine in inputFileReader:
            returnedDictionary[eachLine[inputFileReader.fieldnames[0]]] = eachLine[inputFileReader.fieldnames[1]],eachLine[inputFileReader.fieldnames[2]],eachLine[inputFileReader.fieldnames[3]]

    return returnedDictionary

economyLetterPriceData = {}
economyLetterPriceData = importEconomyLetterPriceDataFromCsvFile('Economy Letters Price Guide ($).csv')

print(economyLetterPriceData)
