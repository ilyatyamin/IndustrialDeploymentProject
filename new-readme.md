helm repo add grafana https://grafana.github.io/helm-charts

helm upgrade --install loki grafana/loki-stack \
--namespace wallet-monitoring \
--create-namespace \
--set promtail.enabled=true \
--set grafana.enabled=true \
--set grafana.adminPassword=admin123 \
--set grafana.service.type=NodePort \
--set loki.persistence.enabled=false \
--set 'promtail.config.clients[0].url=http://loki.wallet-monitoring.svc.cluster.local:3100/loki/api/v1/push'

## сбор currency
docker build -t muffin-currency:1.1.1 .

docker login

docker tag muffin-currency:1.1.1 tyaminilya/muffin-currency:1.1.1

docker push tyaminilya/muffin-currency:1.1.1

## сбор wallet
docker build -t muffin-wallet:1.1.1 .

docker login

docker tag muffin-wallet:1.1.1 tyaminilya/muffin-wallet:1.1.1

docker push tyaminilya/muffin-wallet:1.1.1

## ингресс графана
cd monitoring

kubectl apply -f grafana-ingress.yaml 

minikube tunnel

получить логин пароль
kubectl get secret --namespace wallet-monitoring loki-grafana \
-o jsonpath="{.data.admin-password}" | base64 --decode ; echo

## зипкин
helm repo add zipkin https://zipkin.io/zipkin-helm

helm install zipkin zipkin/zipkin --namespace wallet-monitoring