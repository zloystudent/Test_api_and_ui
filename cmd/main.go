package main

import (
	"log"
	"server-test/intermal/config"
	"server-test/intermal/db"
	"server-test/intermal/handlers"
	"server-test/intermal/server"
	"server-test/intermal/storage"
	"server-test/pkg/logger"
)

func main() {
	cfg := config.NewConfig()

	logger, err := logger.NewLogger(cfg)
	if err != nil {
		log.Fatal(err)
	}

	conn, err := db.NewConnection(cfg)
	if err != nil {
		log.Fatal(err)
	}

	stor := storage.NewStorage(&storage.StorageSetup{
		Conn: conn,
	})

	h := handlers.NewHandler(handlers.HandlerSetup{
		Storage: stor,
		Logger:  logger,
	})

	if err := server.NewHTTPServer(cfg, h); err != nil {
		log.Fatal(err)
	}
}
