import json
from linkedin_api import Linkedin

api = Linkedin(username= 'tunaeem@gmail.com', password='tunahan1907')

profile = api.search_jobs(experience=["2", "3"],
                          job_type=["F"],
                          location_name="Germany",
                          job_title="3612005251",
                          remote=False,
                          limit=15) # 'büşra-ersoy-126994170'

json_object = json.dumps(profile, indent=4)
with open("sample2.json", "w") as outfile:
    outfile.write(json_object)

# https://linkedin-api.readthedocs.io/en/latest/api.html
# https://github.com/tomquirk/linkedin-api/tree/master