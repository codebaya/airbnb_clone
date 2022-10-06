from bs4 import BeautifulSoup
import requests


def extract_jobs(term):
	url = f"https://remoteok.com/remote-{term}-jobs"
	request = requests.get(url, headers={ "User-Agent":"Kimchi" })
	if request.status_code == 200:
		soup = BeautifulSoup(request.text, "html.parser")
		jobs = soup.find_all("tr", class_="job")
		print(len(jobs))
		job_datas = []
		for job in jobs:
			job_posts = job.find_all("td", class_="company")
			for post in job_posts:
				anchors = post.find_all("a")
				anchor = anchors[0]
				link = anchor['href']
				position = (post.find_all("h2"))[0].text.strip()
				loca, sal = post.find_all("div", class_="location")
				location = loca.text
				salary = sal.text
				status0 = post.find_all("span")
				status1 = post.find_all("span")[0].text.strip()
				status2 = post.find_all("span")[1].text.strip()
				if (status2 == "verified") and "closed":
					status2 = status2
				else:
					status2 = ""
				if len(status0) == 3:
					status3 = post.find_all("span")[2].text.strip()
					if (status3 == "verified") and "closed":
						status3 = status3
					else:
						status3 = ""
				
				job_data = {
					'position':position,
					'location':location,
					'salary':salary,
					'status':status1 + status2 + status3
				}
				job_datas.append(job_data)
		# print(job_datas)
		for job_data in job_datas:
			print(job_data)
			print("=====================")
	
	else:
		print("Can't get jobs.")


extract_jobs("rust")