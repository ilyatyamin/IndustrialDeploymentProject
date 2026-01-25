## Что я делал?
> P.S. Это шаблон с большого ДЗ-2. Поэтому тут много лишних файлов, также я не стал удалять часть с istio, ее можно просто пропустить

> P.S.2. Я изначально пытался делать оператор в k8s, но у меня не сильно много чего получилось, поэтому я сделал Docker. Поэтому тут где-то есть остатки решения из Кубера.

1. Поднять миникуб
```yaml
minikube delete --all --purge 

minikube start --driver=docker
minikube addons enable ingress
```

2. Поднял БД в Docker Базу Данных и Prometheus и Grafana. 
Важно! В /etc/hosts должен быть резолв muffin-wallet.com. Я в Docker Compose подшаманил, чтобы под мог резолвить muffin-wallet.com/actuator/prometheus.

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

5. Устанавливаем istio, включаем автоматическую инжекцию sidecar-прокси
```yaml
brew install istioctl

-- В Demo Prometheus, Grafana, Kiali, Jaeger!! автоматом все установилось
istioctl install --set profile=demo -y

kubectl label namespace default istio-injection=enabled --overwrite
kubectl rollout restart deployment -n default

```

6. Сделал ямлик Istio Gateway (в корневой папке)
```yaml
kubectl apply -f gateway/gateway.yaml
```

7. Сделал ямлики VirtualService Wallet и Currency -- надо сделать apply
```yaml
cd muffin-wallet
kubectl apply -f virtual-service-wallet.yaml

cd ..

cd muffin-currency
kubectl apply -f virtual-service-currency.yaml
```

8. сделать туннель
```shell
minikube addons enable ingress
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
sudo minikube tunnel
```

9. Маршрутизация готова:
```yaml
muffin-wallet.com
muffin-currency.com
```

10. Настроим в графане подключение к прометеусу