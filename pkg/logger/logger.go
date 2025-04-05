package logger

import (
	"fmt"
	"os"
	"path"
	"runtime"

	"server-test/intermal/config"

	"github.com/sirupsen/logrus"
)

func NewLogger(config *config.Config) (*logrus.Logger, error) {
	l := logrus.New()

	l.Out = os.Stdout
	l.SetReportCaller(true)

	msg := func(f *runtime.Frame) (string, string) {
		filename := path.Base(f.File)

		return fmt.Sprintf("%s()", f.Function), fmt.Sprintf("%s:%d", filename, f.Line)
	}

	switch config.LoggerFormat {
	case "text":
		l.Formatter = &logrus.TextFormatter{CallerPrettyfier: msg}
	case "json":
		l.Formatter = &logrus.JSONFormatter{CallerPrettyfier: msg}
	}

	return l, nil
}
