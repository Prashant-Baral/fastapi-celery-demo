import time 
import httpx
from bs4 import BeautifulSoup 
from celery_app import celery_app

@celery_app.task
def generate_website_report(url):
	
	start_time = time.perf_counter()
	response = httpx.get(
		url,
		timeout=10, 
		follow_redirects = True
	)
	end_time = time.perf_counter()
	response_time_ms = round(
		(end_time-start_time)*1000
	)


	soup = BeautifulSoup(
		response.text,
		"html.parser"
	)

	title = soup.title.string if soup.title else None

	return {

		"url":url,
		"status_code":response.status_code,
		"response_time_ms": response_time_ms,
		"title":title,
		"links": len(soup.find_all("a")),
		"images": len(soup.find_all("img"))
	}
