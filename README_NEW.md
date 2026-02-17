# Илья Тямин
## Что я делал?

> P.S. Это шаблон с большого ДЗ-2 и ДЗ-1 с второго семестра. Поэтому тут много лишних файлов, также я не стал удалять часть с istio, ее можно просто пропустить

1. Поднять миникуб
```yaml
minikube delete --all --purge 

minikube start --driver=docker
minikube addons enable ingress
```

2. Поднял БД в k8s Базу Данных (почему-то в 2 часа ночи она умерла и host.minikube.internal перестал резолвиться)
Важно! В /etc/hosts должен быть резолв muffin-wallet.com.

```yaml
helm install postgres bitnami/postgresql \
-n default \
--set auth.username=postgres \
--set auth.password=postgres \
--set auth.database=postgres
kubectl port-forward svc/postgres-postgresql 5432:5432


docker-compose up -d
```

3. Как собрать образы и запушить все в Docker Hub:
```shell
docker build -t muffin-currency:2.0.2 .

docker login

docker tag muffin-currency:2.0.2 tyaminilya/muffin-currency:2.0.2

docker push tyaminilya/muffin-currency:2.0.2
```

Аналогично, мне требовалось пересобрать muffin-wallet:
```shell
docker build -t muffin-wallet:2.0.2 .

docker login

docker tag muffin-wallet:2.0.2 tyaminilya/muffin-wallet:2.0.2

docker push tyaminilya/muffin-wallet:2.0.2
```

3. Поднял с помощью Helmfile muffin-wallet
```yaml
cd muffin-wallet
helmfile apply
```

ПЕРЕД ЭТИМ (!!!!!) я добавил в muffin-wallet/values.yaml в раздел env
```yaml
  - name: MANAGEMENT_ZIPKIN_TRACING_ENDPOINT
    value: "http://zipkin.wallet-monitoring.svc.cluster.local:9411/api/v2/spans"
  - name: MANAGEMENT_ZIPKIN_TRACING_CONNECT_TIMEOUT
    value: 5s
  - name: MANAGEMENT_ZIPKIN_TRACING_READ_TIMEOUT
    value: 5s
  - name: MANAGEMENT_ZIPKIN_TRACING_MESSAGE_TIMEOUT
    value: 5s
```
Это нужно для корректной работы трейсинга (его настраивать будем позже)

если надо убить helm release: helmfile destroy

4. Поднял с помощью Helmfile muffin-currency
```yaml
cd muffin-currency
helmfile apply
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
kubectl apply -f muffin-wallet/virtual-service-wallet.yaml
kubectl apply -f muffin-currency/virtual-service-currency.yaml
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

10. Поставим Grafana Stack в k8s: в этот раз я развертывал все локально, не через grafana-loki chart. 
```yaml
kubectl apply -f monitoring/loki.yaml -n wallet-monitoring

helm upgrade --install grafana grafana/grafana \
-n wallet-monitoring \
-f monitoring/values-grafana.yaml
```

Поднялась графана и к ней еще Loki. Есть 2 пути как отобразить ее UI (легкий и простой):

Легкий -- сделать port-forward:
```shell
kubectl port-forward deployment/grafana 3000 3000 -n wallet-monitoring
```

Сложный -- сделать Ingress:
```shell
kubectl apply -f monitoring/grafana-ingress.yaml 
minikube tunnel
```
В /etc/hosts надо будет добавить `192.168.49.2 grafana.local`

Вот она, графана (пароль admin123):
![](images/1.png)

Необходимо будет добавить Loki в DataSource. URL: loki.wallet-monitoring.svc.cluster.local:3100
Loki настроен! Логи можно посмотреть в разделе Explore:

![](images/3.png)

11. Развернем Zipkin (как и в прошлом ДЗ):
```shell
helm repo add zipkin https://zipkin.io/zipkin-helm
helm install zipkin zipkin/zipkin --namespace wallet-monitoring
```

Сделаем port-forward на порт 9411:
```shell
kubectl port-forward deployment/zipkin 9411 9411 -n wallet-monitoring
```

В Grafana добавим Data Source (Zipkin) с URL = http://zipkin.wallet-monitoring.svc.cluster.local:9411

11. В прошлом ДЗ я разворачивал prometheus в докере. В этом прийдется поправить ошбки и развернуть в k8s:
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prometheus prometheus-community/prometheus \
  --namespace wallet-monitoring \
  -f monitoring/values-prometheus.yaml


kubectl port-forward deployment/prometheus-server 9090 9090 -n wallet-monitoring
```

12. Начнем разворачивать `Otel Collector`:
```shell
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update

helm install opentelemetry-collector open-telemetry/opentelemetry-collector \
   --set image.repository="otel/opentelemetry-collector-k8s" \
   --set mode=deployment \
   -n wallet-monitoring \
   -f otel/values.yaml


# Если есть изменения: применить это (апргрейд)
helm upgrade opentelemetry-collector open-telemetry/opentelemetry-collector \
  -n wallet-monitoring \
  -f otel/values.yaml

```