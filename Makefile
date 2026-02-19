.PHONY: build run stop deploy

IMAGE_NAME := livekit-agent

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm \
		-p 8888:8888 \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		-e LIVEKIT_URL=$(LIVEKIT_URL) \
		-e LIVEKIT_API_KEY=$(LIVEKIT_API_KEY) \
		-e LIVEKIT_API_SECRET=$(LIVEKIT_API_SECRET) \
		$(IMAGE_NAME)

stop:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE_NAME)) 2>/dev/null || true

deploy:
	bl deploy
