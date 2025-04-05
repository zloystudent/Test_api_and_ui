package config

import "github.com/spf13/viper"

type Config struct {
	HTTPPort     int
	LoggerFormat string
	DB           DB
}

type DB struct {
	User     string
	Password string
	DB       string
	Host     string
	Port     int
}

func NewConfig() *Config {
	v := viper.New()
	v.AutomaticEnv()

	return &Config{
		HTTPPort:     v.GetInt("HTTP_PORT"),
		LoggerFormat: v.GetString("LOGGER_FORMAT"),
		DB: DB{
			User:     v.GetString("POSTGRES_USER"),
			Password: v.GetString("POSTGRES_PASSWORD"),
			DB:       v.GetString("POSTGRES_DB"),
			Host:     v.GetString("POSTGRES_HOST"),
			Port:     v.GetInt("POSTGRES_PORT"),
		},
	}
}
