import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def load_jobs(job_title, location):
    getVars = {"q": job_title, "l": location, "fromage": "30", "sort": "date"}
    url = "https://ca.indeed.com/jobs?" + urllib.parse.urlencode(getVars)
    page = requests.get(url)
    response = BeautifulSoup(page.content, "html.parser")
    job_result = response.find(id="resultsCol")
    return job_result


def extract_title(job_elem):
    title_elem = job_elem.find("h2", class_="title")
    title = title_elem.text.strip()
    return title


def extract_company_name(job_elem):
    company_elem = job_elem.find("span", class_="company")
    company = company_elem.text.strip()
    return company


def extract_link(job_elem):
    link_elem = job_elem.find("a", ["href"])
    link = link_elem
    return link


def extract_date(job_elem):
    date_elem = job_elem.find("span", class_="date")
    date = date_elem.text.strip()
    return date


def extract_salaries(job_elem):
    salary_elem = job_elem.find("span", class_="salaryText")
    if salary_elem:
        salary = salary_elem.text.strip()
    else:
        salary = "Not shown"


def job_info_indeed(job_result, filters):
    job_elems = job_result.find_all("div", class_="jobsearch-SerpJobCard")

    cols = []
    extracted_data = []
    job_titles = []
    company_names = []
    job_url = []
    salaries = []
    date_posted = []

    if "titles" in filters:
        titles = ["a"]
        cols.append("titles")
        for job in job_elems:
            titles.append(extract_title(job))
        job_titles.append(titles)
        extracted_data.append(titles)

    if "companies" in filters:
        companies = ["a"]
        cols.append("companies")
        for job in job_elems:
            companies.append(extract_company_name(job))
        company_names.append(companies)
        extracted_data.append(companies)

    if "links" in filters:
        links = ["a"]
        cols.append("links")
        for job in job_elems:
            links.append(extract_link(job))
        job_url.append(links)
        extracted_data.append(links)

    if "date_listed" in filters:
        dates = ["a"]
        cols.append("date_listed")
        for job in job_elems:
            dates.append(extract_date(job))
        date_posted.append(dates)
        extracted_data.append(dates)

    if "salary" in filters:
        salary = ["a"]
        cols.append("salary")
        for job in job_elems:
            salary.append(extract_salaries(job))
        salaries.append(salary)
        extracted_data.append(salary)

    job_list = {}

    for n in range(len(cols)):
        job_list[cols[n]] = extracted_data[n]

    num_listings = len(extracted_data[0])

    jobs_df = pd.DataFrame(
        {
            "Job Title": titles,
            "Salary": salary,
            "Company": companies,
            "Post time": dates,
            "Apply url": links,
        }
    )

    return jobs_df, job_list, num_listings


def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame.from_dict(jobs_list, orient="index")
    jobs.transpose()
    jobs.to_excel(
        r"/Users/tmareach/Documents/Python/" + filename, index=False, header=True
    )


def save_jobs_to_excel2(jobs_df, filename):
    path = os.path.join(os.path.expanduser("~"), "Documents", filename)
    jobs_df.to_excel(path, index=False, header=True)


def find_jobs_from(
    job_title,
    location,
    filters,
    filename="results.xlsx",
):
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'Indeed' or 'CWjobs')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .xls file called 'results.xls'
    """

    job_result = load_jobs(job_title, location)
    jobs_df, jobs_list, num_listings = job_info_indeed(job_result, filters)

    save_jobs_to_excel2(jobs_df, filename)

    print(
        "{} new job postings retrieved from indeed. Stored in {}.".format(
            num_listings, filename
        )
    )


find_jobs_from(
    "Data analyst", "canada", ["titles", "companies", "links", "date_listed", "salary"]
)
