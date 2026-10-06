from fastapi import FastAPI
from celery.result import AsyncResult

from celery_app import celery_app
from tasks import generate_website_report


app = FastAPI()

@app.post("/reports")
def create_report(url:str):
	
	task = generate_website_report.delay(url)
	return {
		"job_id": task.id,
		"status": "Pending"
	}


@app.get("/reports/{job_id}")
def get_report(job_id:str):

	task = AsyncResult(
		job_id,
		app=celery_app
	)

	response = {
		"job_id":job_id,
		"status":task.status
	}

	if task.successful():
		response["result"] = task.result
	if task.failed():
		response["error"] = str(task.result)

	return response


