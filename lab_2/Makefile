build=false

up: down
    ifeq ($(build),true)
		docker-compose up -d --build
    else
		docker-compose up -d
    endif

down:
	docker-compose down -v