package server

import (
	"fmt"
	"log"
	_ "server-test/docs"
	"server-test/intermal/config"
	"server-test/intermal/handlers"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/swagger"
)

func NewHTTPServer(cfg *config.Config, handler *handlers.Handler) error {
	app := fiber.New()

	r := app.Group("/api")
	r.All("/_/docs/swagger/*", swagger.HandlerDefault)

	handler.Use(r)

	go func() {
		if err := app.Shutdown(); err != nil {
			log.Fatal(err)
		}
	}()

	if err := app.Listen(fmt.Sprintf(":%d", cfg.HTTPPort)); err != nil {
		return err
	}

	return nil
}
