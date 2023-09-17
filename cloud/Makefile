hello :
	echo "Hello World"

run_api_local :
	uvicorn fast:app --reload

build :
	docker build -t casestudy .

run_interactive :
	docker run -it  casestudy sh

run_api_docker :
	docker run -p 8000:8000 -e PORT=8000 casestudy

build_gcp:
	docker build -t $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

push :
	docker push $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)

deploy :
	gcloud run deploy --image $(GCR_MULTI_REGION)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME) --platform managed --region $(GCR_REGION)
