# ToDo App

## Project Overview

ToDo App is a full-stack application that allows users to manage their tasks with functionalities including create, edit, update, delete, and mark as done. It also sends email reminders (alarms) to users about their tasks. If a task's alarm is sent and its time is updated, the alarm will be re-sent according to the new schedule.

The application is containerized using Docker, deployed on K3s Kubernetes, and integrated with Jenkins CI/CD.

## Architecture & Services

### Services

* 📝 **todo-service**: Handles task operations (add, edit, delete, mark as done, set alarms)
* 🔐 **auth-service**: Manages user authentication (login/register) and stores user emails
* ⏰ **alarm-service**: Sends email reminders by fetching user email from auth-service and task details from todo-service
* 💻 **frontend**: React-based user interface

### Interaction Flow

1. 👤 User registers/logs in → auth-service
2. 📝 User manages tasks → todo-service
3. ⏰ Alarms sent → alarm-service

## Features

* ✅ Task management (CRUD)
* 📧 Email reminders for tasks
* ⏱️ Alarm re-sending when task time is updated
* 🔐 User authentication via email

## Project Structure

```
ToDo/
├── alarm-service/
├── auth-service/
├── todo-service/
├── frontend/
├── k8s/
├── docker-compose.yml
└── Jenkinsfile
```

## Deployment Instructions

### 1. Build Docker Images

```
docker compose build
```

### 2. Save Docker Images

```
docker save todo-auth-service:latest -o todo-auth.tar
docker save todo-todo-service:latest -o todo-todo.tar
docker save todo-alarm-service:latest -o todo-alarm.tar
docker save todo-todo-frontend:latest -o todo-frontend.tar
```

### 3. Import Images to K3s

```
sudo k3s ctr images import todo-auth.tar
sudo k3s ctr images import todo-todo.tar
sudo k3s ctr images import todo-alarm.tar
sudo k3s ctr images import todo-frontend.tar
```

### 4. Apply Kubernetes Manifests

```
cd k8s
kubectl apply -f .
kubectl apply -f auth-service/
kubectl apply -f todo-service/
kubectl apply -f alarm-service/
kubectl apply -f frontend/
```

## CI/CD with Jenkins

* 🔄 Triggered by GitHub webhook on push
* ⚙️ Pipeline steps:

  1. Clone repository
  2. Build Docker images
  3. Push images to local K3s container registry
  4. Apply Kubernetes manifests

## Email Configuration

* 📧 Uses SMTP account to send task alarms
* 👤 User email is registered in auth-service for alarm-service

## Deployment Video

[▶️ Watch Video](INSERT_YOUR_VIDEO_LINK_HERE)

## Contact

✉️ Mohanad Hesham El-Sayed Mahmoud
For questions or support, feel free to reach out.
