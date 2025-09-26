api:
	docker build -f Dockerfile_api -t city_cleaning_api:1.0 .  
	docker run --env-file .env -p 8080:8080 city_cleaning_api:1.0

app:
	docker build -f Dockerfile_app -t city_cleaning_app:1.0 .  
	docker run --env-file .env -p 8000:8000 city_cleaning_app:1.0