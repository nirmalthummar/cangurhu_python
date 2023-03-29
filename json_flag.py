import requests,json
# r = requests.get('https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json')
# # print(r.json())
# with open("country_state.json", "w") as outfile:
#     json.dump(r.json(), outfile)
from apps.snippets.models import Country
with open('flag.json') as json_file:
    with open('country_state.json') as country:
        data = json.load(json_file)
        cot= json.load(country)
        for i in cot:
            for j in data:
                if j['name']==i['name']:
                    print(j['name'])
                    print(i['name'])

                    break
