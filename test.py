import pywikibot


def existing_claim_from_year(item, year):
    try:
        claims = item.claims['P1082']
        time_str = pywikibot.WbTime(year=year).toTimestr()
        for claim in claims:
            for qualifier_value in claim.qualifiers['P585']:
                if (qualifier_value.getTarget().toTimestr() == time_str):
                    return claim
    except KeyError:
        pass
    return None


population_prop_id = 'P1082'
time_prop_id = 'P585'
url_prop_id = 'P854'
retrieved_prop_id = 'P813'
source_url = 'https://www.statistik.bs.ch/dam/jcr:2d711b31-d8c9-4f5d-9151-55ff4ef4028d/t01-1-16.xlsx'
item_id = "Q4115189"

# connect to WikiData
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, item_id)
item.get()
#print(item.claims)

year_list = range(2018, 2018)
#for year in year_list:
year = 2018
population_claim = existing_claim_from_year(item, year)
if (population_claim is None):
    
    population_value = 12345
    population_claim = pywikibot.Claim(repo, population_prop_id)
    population_claim.setTarget(pywikibot.WbQuantity(amount=population_value, site=site))
    item.addClaim(population_claim)
    
    timeQualifier = pywikibot.Claim(repo, time_prop_id)
    yearObj = pywikibot.WbTime(year=year)
    timeQualifier.setTarget(yearObj)
    population_claim.addQualifier(timeQualifier)
    
    retrievedQualifier = pywikibot.Claim(repo, retrieved_prop_id)
    today = pywikibot.WbTime(year=2019, month=2, day=23)
    retrievedQualifier.setTarget(today)
    population_claim.addQualifier(retrievedQualifier)
    
    source = pywikibot.Claim(repo, url_prop_id)
    source.setTarget(source_url)
    population_claim.addSource(source)
else:
    print ("Population claim already exists on %s for year %d, skipping") % (item_id, year)
        