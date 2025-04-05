package db

import (
	"context"
	"fmt"
	"server-test/intermal/config"

	"github.com/jackc/pgx/v5/pgxpool"
)

func NewConnection(cfg *config.Config) (*pgxpool.Pool, error) {
	dns := fmt.Sprintf("postgres://%s:%s@%s:%d/%s", cfg.DB.User, cfg.DB.Password, cfg.DB.Host, cfg.DB.Port, cfg.DB.DB)

	config, err := pgxpool.ParseConfig(dns)
	if err != nil {
		return nil, err
	}

	config.MaxConns = 20

	return pgxpool.NewWithConfig(context.Background(), config)
}
