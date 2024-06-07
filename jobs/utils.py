import requests
from bs4 import BeautifulSoup
def fetch_github_jobs():
    url = "https://jobs.github.com/positions.json?description=developer"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_indeed_jobs():
    url = "https://www.indeed.com/jobs?q=developer&l="
    response = request.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"jobsearch-SerpJobCard"}):
        title = div.find("a", attrs={"data-tn-element": "jobTitle"}).text.strip()
        company = div.find("span", attrs={"class":"company"}).text.strip()
        location = div.find("div", attrs={"class":"recJobLoc"})['data-rc-loc'].strip()
        summary = div.find("div", attrs={"class":"summary"}).text.strip()
        job_url = "https://www.indeed.com" + div.find("a", attrs={"data-tn-element": "jobTitle"})['href']

        jobs.append({
            "title":title,
            "company":company,
            "description":summary,
            "url":job_url
        })
    return jobs

def fetch_linkedin_jobs():
    return[]

def fetch_ebay_jobs():
    api_url = 'https://api.ebay.com/jobs/v1/country/US'
    headers = {
        'Authorization': '#',
        'Accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching eBay jobs:", response.text)

