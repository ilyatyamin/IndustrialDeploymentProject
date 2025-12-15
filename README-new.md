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

-- В Demo Prometheus, Grafana, Kiali, Jaeger!! автоматом все установилось
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

9. Маршрутизация готова:
```yaml
muffin-wallet.com
muffin-currency.com
```

Когда создавать аккаунты, четко типы из кода Muffin currency!!! тогда будут работать транзакции

10. Kiali
```yaml
-- https://istio-cheatsheet.tetratelabs.io/istioctl

-- скачать istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.28.1
export PATH=$PWD/bin:$PATH

kubectl apply -f samples/addons/prometheus.yaml
kubectl apply -f samples/addons/kiali.yaml
kubectl apply -f samples/addons/grafana.yaml
kubectl apply -f samples/addons/jaeger.yaml

-- Дашборд
istioctl dashboard kiali

-- Графану можно поставить так
istioctl dashboard grafana

-- внутри сделал подключение к http://prometheus.istio-system:9090
-- это можно посмотреть в service mesh kiali (все адреса)

-- Ягер можно посмотреть вот так
istioctl d jaeger
-- http://tracing.istio-system.svc.cluster.local

```

11. Трейсинг (дальше боль и страдания)
```yaml
kubectl apply -f tracing.yaml  -- Включил трейсинг в самом istio: tracing/tracing.yaml
```

Далее поправил в samples/addons/jaeger.yaml: там включил трейсинг и указал gRPC путь
https://kiali.io/docs/configuration/p8s-jaeger-grafana/tracing/jaeger/
```yaml
enabled: true
internal_url: "http://tracing.istio-system:16685/jaeger"
use_grpc: true
# Public facing URL of Jaeger
external_url: "http://jaeger.muffin-wallet.com"
```

Обновил:
```yaml
 kubectl apply -f samples/addons/kiali.yaml
 kubectl rollout restart deploy kiali -n istio-system
```

## Авторизация
12. Создадим Service Account для muffin-wallet. Нужно для похода в muffin-currency
```yaml
kubectl apply -f security/muffin-wallet-account.yaml
```