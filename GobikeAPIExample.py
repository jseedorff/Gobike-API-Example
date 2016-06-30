#Gobike API access from Python 2.7
#Jakob Seedorff, Gobike A/S
#Login to the Gobike API requires login, password and AppId
#AccessToken is assigned at authentification/login and must
#be kept for later use

#Import Python libraries for HTTP requests and JSON.
#Note that some libraries must be installed before they can
#be imported and used (search Google to figure out how) 
import requests
import json

#Prompt user for identity, password amd AppId
API_Identity = "xxxx"
API_Password = "xxxx"
App_ID = "xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx"

#Gobike API authentification, prepare url, JSON payload and headers
url = 'http://api.gobike.com/auth'
payload = {'Identity':API_Identity, 'Password':API_Password}
headers = {'Content-Type': 'text/json',
           'Host': 'api.gobike.com',
           'Authorization': 'OAuth AppId='+App_ID,
           'Content-Length': '52'
           }

#Login by HTTP POST and retract AccessToken from JSON response
#Token is needed for later user specific requests and logout
response = requests.post(url, data=json.dumps(payload), headers=headers)
API_Token = json.loads(response.text)["Data"]["AccessToken"]["Token"]
print("API Login Success")
print("Token is: "+API_Token+"\n\r")

#Get list of all docking stations. Page is first record, while pagezise
#is the number of records returned in a single payload
#There are currently 100 docking stations
#Prepare url, JSON payload and headers
#AccessToken (provided at authentication) is required as info is user related
url = 'http://api.gobike.com/docking-stations?page=0&pagesize=101'
payload = {'Identity':API_Identity, 'Password':API_Password}
headers = {'Content-Type': 'text/json',
           'Host': 'api.gobike.com',
           'Authorization': 'OAuth AppId='+App_ID+' AccessToken='+API_Token,
           'Content-Length': '52'
           }

#Read JSON response payload by HTTP GET and decode specific information
#about Docking Station name, number of docking points at station and
#free docking points
response = requests.get(url, data=json.dumps(payload), headers=headers)
decoded = json.loads(response.text)

#Print Station name with latitude and longitude
print('Complete list of all Docking Stations')
print('-------------------------------------')
for element in decoded['Data']['List']:
    print element['Name']+","+str(element['Location']['Latitude'])+","+str(element['Location']['Longitude'])
print

#Get list of 10 docking points near Copenhagen centrqal station
#is the number of records returned in a single payload
#Prepare url, JSON payload and headers
#AccessToken (provided at authentication) is required as info is user related
url = 'http://api.gobike.com/docking-stations/book?latitude=55.672718&longitude=12.564710&page=0'
payload = {'Identity':API_Identity, 'Password':API_Password}
headers = {'Content-Type': 'text/json',
           'Host': 'api.gobike.com',
           'Authorization': 'OAuth AppId='+App_ID+' AccessToken='+API_Token,
           'Content-Length': '52'
           }

#Read JSON response payload by HTTP GET and decode specific information
#about Docking Station name, number of docking points at station and
#free docking points
response = requests.get(url, data=json.dumps(payload), headers=headers)
decoded = json.loads(response.text)

#Print Station name with latitude and longitude
print('Complete list 10 nearest Docking Station around CPH H')
print('-----------------------------------------------------')
for element in decoded['Data']['List']:
    print element['DockingStation']['Name'],element['DockingStation']['Location']['Latitude'],element['DockingStation']['Location']['Longitude'],element['AvailableBikesForBooking'],element['Distance']
print

#Gobike API Logout, prepare url, JSON payload and headers
#AccessToken (provided at authentication) is required to logout
url = 'http://api.gobike.com/auth/logout'
payload = {'Identity':API_Identity, 'Password':API_Password}
headers = {'Content-Type': 'text/json',
           'Host': 'api.gobike.com',
           'Authorization': 'OAuth AppId='+App_ID+' AccessToken='+API_Token,
           'Content-Length': '52'
           }
#Logout and report success or failure
response = requests.post(url, data=json.dumps(payload), headers=headers)
if json.loads(response.text)["IsSuccess"] == True:
   print("API Logout Success")
else:
   print("API Logout Failure")
