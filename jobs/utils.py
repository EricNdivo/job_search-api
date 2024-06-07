import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings
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

def scrape_jobs_from_website():
    url = 'https://www.indeed.com/q-python-developer-jobs.html'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')
        return job_listings
    else:
        print("Error fetching website:", response.text)
        return[]

def store_jobs_in_db(jobs):
    from .models import Job
    new_jobs = []
    for job_data in jobs:
        job, created = Job.objects.get_or_create(
            title=job_data['title'],
            description=job_data['description'],
            company=job_data['company'],
        )
        if created:
            new_jobs.append(job)
    return new_jobs

def send_new_jobs_email(user, jobs):
    subject = 'New Freelance Jobs Available'
    messge = f'Hello {user.username},\n\nNew freelnce jobs have been posted:\n'
    for job in jobs:
        message += f"-{job.title} at {job.company} in {job.location}\n"
    message += '\nBest regards, \nYour Job Portal Team'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silenty=False,
    )    