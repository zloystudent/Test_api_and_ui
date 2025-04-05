run:
	docker-compose down
	docker-compose up --build -d

swagger:
	find $(PWD) \( -path "*/docs" \) -exec rm -rf {} +
	# go install github.com/swaggo/swag/cmd/swag@latest
	swag init -g ./cmd/main.go -o ./docs --parseInternal