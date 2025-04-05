FROM golang:1.20 AS build
WORKDIR /app
ENV CGO_ENABLED=0
ENV GOPROXY=https://goproxy.io,direct

COPY go.mod go.sum* ./
RUN go mod download
COPY . .
RUN go build -ldflags "-w -s" -o service cmd/main.go

FROM alpine:3.17 AS runtime
COPY --from=build /app/service ./
ENTRYPOINT ["/service"]
