# image_processing
Лабораторная работа по параллельным вычислениям
Для запуска kubernetes сперва нужно собрать все микросервисы
```cmd
docker build -t {your_account}/{microservice_name}:latest .
```
Пример:
```cmd
docker build -t f0mbus/frontend:latest
```

После сборки всех микросервисов необходимо добавить их в Dockerhub, так как именно от туда kubernetes достает образы.
```cmd
docker push {your_account}/{microservice_name}:latest
```
Пример:
```cmd
docker push f0mbus/frontend:latest
```

После добавление можно приступать к сборке в kubernetes, но сначала нужно запустить minikube:
```cmd
minikube start
```
Далее собираем все образы в сервисы:
```cmd
kubectl apply -f kube.yaml
```
Чтобы узнать собраны ли сервисы, можно ввести команду:
```cmd
kubectl get pods
```
Когда все сервисы будут успешно собраны, необходимо пробросить порт для использования
```cmd
kubectl port-forward deployment/{microservice_name} 8000:{your_port}
```
Пример:
```cmd
kubectl port-forward deployment/frontend 8000:8000

Далее можно перейти на localhost:{your_port} в браузере
Как выглядит:
![image](https://github.com/user-attachments/assets/a6440dc4-c1fc-4427-b6dd-9387226dc6a3)

![image](https://github.com/user-attachments/assets/e4663f65-b560-4ee4-a66d-8ae01c339593)

