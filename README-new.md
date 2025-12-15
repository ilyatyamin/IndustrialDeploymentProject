## Что я делал?

1. Поднять миникуб
```yaml
minikube delete --all --purge 

minikube start --driver=docker
minikube addons enable ingress
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

4. Поднял с помощью Helmfile muffin-currency
```yaml
cd muffin-currency
```

если надо убить helm release: helmfile destroy

5. сделать туннель
```shell
minikube addons enable ingress
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
sudo minikube tunnel
```

6. Устанавливаем istio, включаем автоматическую инжекцию sidecar-прокси
```yaml
brew install istioctl
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled --overwrite
kubectl rollout restart deployment -n default

```

7. Сделал ямлик Istio Gateway (в корневой папке)
```yaml
kubectl apply -f gateway.yaml
```

8. Сделал ямлики VirtualService Wallet и Currency -- надо сделать apply
```yaml
cd muffin-wallet
kubectl apply -f virtual-service-wallet.yaml

cd ..

cd muffin-currency
kubectl apply -f virtual-service-currency.yaml
```