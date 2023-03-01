# dataharvest
### create postgres container for database
```
docker run --restart=always --name container_dataharvest -e POSTGRES_DB=dataharvest -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=dataharvest -p 5432:5432 -d postgres