## Что я делал?
У меня в Docker (ДЛЯ СЕБЯ): muffin-wallet-database-1 с первой домашки
postgres/postgres/postgres

### Сгенерировал файлы
```shell
helm create muffin-wallet
```

### Helm Install
```shell
helm install muffin-wallet ./muffin-wallet
```

### Helm Upgrade
```shell
helm upgrade --install muffin-wallet ./muffin-wallet
```

### С helmfile
```shell
helmfile apply
helmfile destroy
```