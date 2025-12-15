## Что я делал?

1. Поднять миникуб
```yaml
minikube delete --all --purge 

minikube start --driver=docker
```

2. Поднял БД в Docker Базу Данных
```yaml
docker-compose up -d
```

3. Поднял с помощью Helmfile muffin-wallet
```yaml
cd muffin-wallet
helmfile apply
```

если надо убить helm release: helmfile destroy