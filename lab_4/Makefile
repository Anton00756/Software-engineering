build=false

up: down
    ifeq ($(build),true)
		docker-compose up -d --build
    else
		docker-compose up -d
    endif

down:
	docker-compose down -v

get_openapi:
	docker exec user_service python3 get_openapi.py
	mv user_service/openapi.yaml user_openapi.yaml
	docker exec message_service python3 get_openapi.py
	mv message_service/openapi.yaml message_openapi.yaml