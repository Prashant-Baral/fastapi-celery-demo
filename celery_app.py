from celery import Celery 

celery_app = Celery(
	"website_report",
	broker="redis://localhost:6379/0",
	backend="redis://localhost:6379/1"
)

