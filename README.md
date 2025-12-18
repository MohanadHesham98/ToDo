--test webhook--
docker compose build

cd k8s

docker save todo-auth-service:latest -o todo-auth.tar
docker save todo-todo-service:latest -o todo-todo.tar
docker save todo-alarm-service:latest -o todo-alarm.tar
docker save todo-todo-frontend:latest -o todo-frontend.tar

sudo k3s ctr images import todo-auth.tar
sudo k3s ctr images import todo-todo.tar
sudo k3s ctr images import todo-alarm.tar
sudo k3s ctr images import todo-frontend.tar

kubectl apply -f .
kubectl apply -f auth-service/
kubectl apply -f todo-service/
kubectl apply -f alarm-service/
