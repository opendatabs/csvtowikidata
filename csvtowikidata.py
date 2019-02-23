import pywikibot
import datetime
import csv
import pprint

#set preferred rank for latest year
latest_year = 2018
data_file = "SandboxData.csv"
population_prop_id = 'P1082'
time_prop_id = 'P585'
url_prop_id = 'P854'
retrieved_prop_id = 'P813'
source_url = 'https://www.statistik.bs.ch/dam/jcr:2d711b31-d8c9-4f5d-9151-55ff4ef4028d/t01-1-16.xlsx'
#item_id = "Q4115189" #wikidata sandbox
#item_id = "Q809909" #Basel-Klybeck


Basel_mapping = {
    #Wikidata Sandbox
    '-1': "Q4115189",
    '1' : "Q445565", 
    '2' : "Q809915", 
    '3' : "Q809899",
    '4' : "Q809901", 
    '5' : "Q809913", 
    '6' : "Q809905", 
    '7' : "Q809902", 
    '8' : "Q809900", 
    '9' : "Q809903",
    '10' : "Q809907", 
    '11' : "Q809912", 
    '12' : "Q445588",
    '13' : "Q809904",
    '14' : "Q809916",
    '15' : "Q664993",
    '16' : "Q809914",
    '17' : "Q809911",
    '18' : "Q809909",
    '19' : "Q809908",
    '20' : "Q5262",
    '30' : "Q67530",
    #Gemeinde Basel
    '90' : "Q78",
    #Kanton Basel-Stadt
    '99' : "Q12172"
}

def existing_claim_from_year(item, year):
    try:
        claims = item.claims['P1082']
        time_str = pywikibot.WbTime(year=year, month=12, day=31).toTimestr()
        for claim in claims:
            for qualifier_value in claim.qualifiers['P585']:
                if (qualifier_value.getTarget().toTimestr() == time_str):
                    return claim
    except KeyError:
        pass
    return None


def read_file(path):
    '''
    Returns all rows as dict
    '''
    rows = []
    with open(path, 'rb') as f:
        reader = csv.DictReader(f)
        for row_dict in reader:
            rows.append(row_dict)
    return rows


# connect to WikiData
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

rows = read_file(data_file)
#pprint.pprint(rows)

#exit()

for row in rows:
    year = int(row["Jahr"])
    population_value = row["Einwohner"]
    item_id = Basel_mapping[row['Wohnviertel_id']]
    print(str(year) + ": " + row['Wohnviertel_id'] + " -> " + item_id + ": " + str(population_value) + " Einwohner")
    item = pywikibot.ItemPage(repo, item_id)
    item.get()
    #print(item.claims)
    
    #year_list = range(2018, 2019)
    #for year in year_list:
    population_claim = existing_claim_from_year(item, year)
    #print(population_claim)
    if (population_claim is None):
        population_claim = pywikibot.Claim(repo, population_prop_id)
        population_claim.setTarget(pywikibot.WbQuantity(amount=population_value, site=site))
        item.addClaim(population_claim)
        
        timeQualifier = pywikibot.Claim(repo, time_prop_id)
        yearObj = pywikibot.WbTime(year=year, month=12, day=31)
        timeQualifier.setTarget(yearObj)
        population_claim.addQualifier(timeQualifier)
        
        source = pywikibot.Claim(repo, url_prop_id)
        source.setTarget(source_url)
        retrieved = pywikibot.Claim(repo, retrieved_prop_id)
        today = datetime.datetime.today()
        retrieved_date = pywikibot.WbTime(year=today.year, month=today.month, day=today.day)
        retrieved.setTarget(retrieved_date)
        population_claim.addSources([source, retrieved])
    
        #set preferred rank for latest year only
        if (year == latest_year):
            population_claim.changeRank("preferred")
    else:
        print ("Population claim already exists on %s for year %d, skipping") % (item_id, year)
        #todo: set rank to normal