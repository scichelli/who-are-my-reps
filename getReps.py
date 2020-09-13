import requests
import csv

class Division:
    def __init__(self, divisionDict):
        self.name = divisionDict.get('name')
        self.officeIndices = divisionDict.get('officeIndices',[])


class Office:
    def __init__(self, officeDict):
        self.name = officeDict.get('name')
        self.divisionId = officeDict.get('divisionId')
        self.levels = officeDict.get('levels',[])
        self.roles = officeDict.get('roles',[])
        self.officialIndices = officeDict.get('officialIndices',[])


class Official:
    def __init__(self, officialDict):
        self.name = officialDict.get('name')
        self.address = officialDict.get('address',{})
        self.party = officialDict.get('party')
        self.phones = officialDict.get('phones',[])
        self.urls = officialDict.get('urls',[])
        self.photoUrl = officialDict.get('photoUrl')
        self.channels = officialDict.get('channels',[])


address = {'address': '1100 Congress Ave, Austin, TX 78701'}
myRepsResponse = requests.get('https://www.commoncause.org/wp-json/google_civic/v1/address', params=address)
myRepsJson = myRepsResponse.json()

divisionsJson = myRepsJson['divisions']
divisions = {k:Division(divisionsJson[k]) for k in divisionsJson.keys()}

offices = [Office(x) for x in myRepsJson['offices']]

officials = [Official(x) for x in myRepsJson['officials']]

def printList():
    for office in offices:
        print(office.name)
        print(divisions[office.divisionId].name)
        for i in office.officialIndices:
            print(officials[i].name)
        print('----')

def printCsv():
    with open('MyRepresentatives.csv', 'w', newline='') as csvfile:
        repWriter = csv.writer(csvfile, dialect='excel-tab')
        repWriter.writerow(['Official','Office','Party','Phones','Urls','Twitter'])
        # for each office, make a row for each official, unless it is vacant, in which case make a row for the unfilled office
        for office in offices:
            if not office.officialIndices:
                repWriter.writerow('vacant',office.name,'','','','')
            else:
                for i in office.officialIndices:
                    official = officials[i]
                    phones = ", ".join(official.phones)
                    urls = " ".join(official.urls)
                    twitter = [c['id'] for c in official.channels if c['type'] == 'Twitter']
                    repWriter.writerow([official.name, office.name, official.party, phones, urls, twitter])

printCsv()
