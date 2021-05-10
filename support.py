import requests
import pandas as pd
browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
base_url = "https://cdn-api.co-vin.in/api"
def get_states():
    global base_url
    global browser_header
    state_url = "/v2/admin/location/states"
    response = requests.get(base_url+state_url, headers=browser_header)
    if response.status_code != 200:
        raise Exception("API ERROR")
    else:
        states = response.json()['states']
        state_names = []
        state_id = []
        for state in states:
            state_id.append(state['state_id'])
            state_names.append(state['state_name'])
        return (state_id,state_names)
def get_district(state_id):
    global base_url
    global browser_header
    district_url = f"/v2/admin/location/districts/{state_id}"
    response = requests.get(base_url+district_url, headers=browser_header)
    if response.status_code != 200:
        raise Exception("API ERROR")
    else:
        districts = response.json()['districts']
        district_names = []
        district_id = []
        for district in districts:
            district_id.append(district['district_id'])
            district_names.append(district['district_name'])
        return (district_id, district_names)
def get_full_data(district_id, date):
    find_url = f"/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"
    response = requests.get(base_url+find_url, headers=browser_header)
    if response.status_code != 200:
            raise Exception("API ERROR")
    else:
        centers = []
        for center in response.json()['centers']:
            n_c = {}
            n_c["center_id"] = center["center_id"]
            n_c["name"] = center["name"]
            n_c["address"] = center["address"] + "," + center['district_name'] + "," + center['state_name'] + "," + str(center['pincode'])
            n_c["pincode"] = center["pincode"]
            n_c["fee_type"] = center["fee_type"]
            n_c["sessions"] = center["sessions"]
            centers.append(n_c)
        return centers
def filter_data(data, min_age_limit=None):
    if min_age_limit != None:
        centers = []
        for center in data:
            add_data = False
            for sessions in center["sessions"]:
                if sessions['min_age_limit'] == min_age_limit and sessions['available_capacity'] > 0:
                    add_data = True
            if add_data:
                n_c = {}
                n_c["name"] = center["name"]
                n_c["address"] = center["address"]
                n_c["pincode"] = center["pincode"]
                n_c["fee_type"] = center["fee_type"]
                centers.append(n_c)
    else:
        centers = data
    centers = pd.DataFrame(centers, index=[x for x in range(1,len(centers)+1)])
    return centers