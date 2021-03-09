import requests as r
import pandas as pd



def hotmart_auth():
    basic = "Basic ZjRiODIxZGUtMmRjNC00Nzg2LTgzMDQtMzA1MGRjZWY3MmNkOmVkMWUxNDE3LWM4Y2UtNDM3Mi05MzY0LTg1ZmVhYjg1MzQyNQ=="
    client_id = "f4b821de-2dc4-4786-8304-3050dcef72cd"
    client_secret = "ed1e1417-c8ce-4372-9364-85feab853425"

    url = f"https://api-sec-vlc.hotmart.com/security/oauth/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

    payload = {}
    headers = {
        'Content-Type': 'Application/Json',
        'Authorization': basic,
        'Cookie': 'JSESSIONID=DFEECA0BC88E84CD35A591E514745FE0; AWSALB=KLc5XyVcz3zcMrw9R43RUGAMK2hHZH2XJ002VEFnX31TF3FH8buiPOi0O275e6moyqEoURpLHOZRov1e6hkl+1skJC+x/2KEdFeDL2qX9gfwmeoAY7pW4PbMYeu5; AWSALBCORS=KLc5XyVcz3zcMrw9R43RUGAMK2hHZH2XJ002VEFnX31TF3FH8buiPOi0O275e6moyqEoURpLHOZRov1e6hkl+1skJC+x/2KEdFeDL2qX9gfwmeoAY7pW4PbMYeu5'
    }

    response = r.request("POST", url, headers=headers, data=payload)

    return response.json()['access_token']

bearer = "H4sIAAAAAAAAAB2QyZKqMABFv8iuoCiwREQMkCghjJsuJpkHXzOYfP1re3%2FPqVO3YGaVGll9r03X41DANfyBAzlmGjzBdgp9zVS%2BCmbyaK9ssQtPATNZHFxbWG91fjCn3PDq0N3qOKw22Ixv3KgiphlHF4fZmlnlIRnTv13XZeyPh1Qg2PFNLxTwmbZEo0L550gGMv06amwghoJoi7g6I%2BqBqAYgblpg06qJDTSjPWT4YvaIRyBqEP%2B0RPv3FAdHEO679uOIG1LfL%2FAdG96MetJgDQDMy71Ny0%2FbjLgqIIM0cRAdUI9bOIAvy5GCfMconxewXPv92oe4wGgsmSWOmqRMrCNCB1448Y7ys3zGp02vuqtPVPs7PExyDg9V14g8A49VIscilimINf33gVsCKM2qZ6Ati9tZ0syj58iTx6q1s%2BSfW2paq3xvXbaQ8eV3EuRmfnTT8zU96m6%2F8kVRExOthZh9vwTPkkz1leEXvGzKqhjMHvTrLklLURr%2Bscc2TgyPxTpcv1VnxZFG1c2LTzLS5NS2RN16Oly2hm2XCmcZiyTUXtbPMs8mmd5V0bm4NXwqiP2pKx6Dm0u6G4FlWyRFSohyAPimG887FuObywZM9HF3boULdoPpYE%2BdujozTsCthkbi3H%2F89Vb%2BB8smXkJjAgAA"

url = "https://sandbox.hotmart.com/payments/api/v1/subscriptions?page_token="

payload={}
headers = {
  'Authorization': f'Bearer {bearer}',
  'Content-Type': 'application/json'
}

response = r.request("GET", url, headers=headers, data=payload)

dataframe = pd.DataFrame(response.json()['items'])



