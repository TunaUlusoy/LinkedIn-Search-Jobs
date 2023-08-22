import pandas as pd

from linkedin_api import Linkedin


class Search:

    def __init__(self, username, password, keywords, location, day, limit):
        self.username = username
        self.password = password
        self.keywords = keywords
        self.locations_name = location
        self.day = day
        self.limit = limit

        self.api = Linkedin(username=self.username, password=self.password)

    def search_results(self):
        search_results = self.api.search_jobs(keywords=self.keywords,
                                              experience=["2", "3", "4"],
                                              job_type=["F"],
                                              location_name=self.locations_name,
                                              listed_at=int(self.day * 24 * 60 * 60),
                                              limit=int(self.limit))

        return search_results

    def get_requirements_from_results(self, search_results):
        rows = []

        try:
            job_ids = [result["dashEntityUrn"].split(":")[3] for result in search_results]
            for job_id in job_ids:
                job = self.api.get_job(job_id)
                company_id = job["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["entityUrn"].split(":")[-1]
                company = self.api.get_company(company_id)

                # job title
                job_title = job["title"] if "title" in job.keys() else 'Unknown'

                # job description
                description = job["description"]["text"] if "description" in job.keys() else 'Unknown'

                # remote or not
                # remote = "No" if not job["workRemoteAllowed"] else "Yes" if "workRemoteAllowed" in job.keys() else 'Unknown'
                remote = "No" if "workRemoteAllowed" in job.keys() and not job["workRemoteAllowed"] else "Yes" if "workRemoteAllowed" in job.keys() else 'Unknown'

                # company name
                company_name = company['name'] if "name" in company.keys() else 'Unknown'

                # company description
                company_description = company["description"] if "description" in company.keys() else 'Unknown'

                # company size
                start = company['staffCountRange']['start'] if 'start' in company['staffCountRange'].keys() else 'Unknown'
                end = company['staffCountRange']['end'] if 'end' in company['staffCountRange'].keys() else 'Unknown'
                company_size = f"{start}-{end}"

                # company country
                countries = [i['country'] for i in company['confirmedLocations']] if "confirmedLocations" in company.keys() and "country" in company["confirmedLocations"][0].keys() else 'Unknown'

                # country cities
                cities = [i['city'] for i in company['confirmedLocations']] if "confirmedLocations" in company.keys() and "city" in company["confirmedLocations"][0].keys() else 'Unknown'

                # company url
                url = company["companyPageUrl"] if "companyPageUrl" in company.keys() else 'Unknown'

                # company linkedin url
                linkedin_url = company["url"] if "url" in company.keys() else 'Unknown'

                # company foundation year
                foundation = company["foundedOn"]["year"] if "foundedOn" in company.keys() else 'Unknown'

                rows.append([job_title, description, remote, company_name, company_description, company_size, countries, cities, url, linkedin_url, foundation])

        except KeyError:
            pass

        df = pd.DataFrame(rows, columns=["Job Title", "Job Description", "Remote", "Company Name", "Company Description", "Company Size", "Countries",
                                         "Cities", "Official Website", "Linkedin URL", "Foundation Year"])

        df.to_csv(f"JOBS_{self.keywords.strip().upper()}_{self.locations_name.strip().upper()}.csv", index=False)

        return rows
