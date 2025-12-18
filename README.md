# ToDo App

[License: MIT]  
[Docker Enabled]  
[K3s Kubernetes]  
[Jenkins CI/CD]

---

## Project Overview

ToDo App is a full-stack application for managing tasks. Features include:

- Create, edit, update, delete, and mark tasks as done
- Email reminders (alarms) for tasks
- Dynamic alarm updates when task time changes
- Secure user authentication (login/register)

Containerized using Docker, deployed on K3s Kubernetes, with Jenkins CI/CD.

---

## Architecture & Services

### Services
- **todo-service**: Task operations: add, edit, delete, mark as done, set alarms
- **auth-service**: User authentication and email management
- **alarm-service**: Sends email reminders for tasks
- **frontend**: React-based UI for user interaction

**Flow:**
1. User registers/logs in → auth-service
2. User manages tasks → todo-service
3. Alarms sent → alarm-service (fetches email from auth-service and task from todo-service)

---

## Features

- Task Management (CRUD)
- Email Alarms for reminders
- Alarm re-sending on task time updates
- User authentication via email

---
Features

Project Structure
ToDo/
├── alarm-service/
├── auth-service/
├── todo-service/
├── frontend/
├── k8s/
├── docker-compose.yml
└── Jenkinsfile


---

## Deployment Instructions

### 1. Build Docker Images
docker compose build

### 2. Save Docker Images
docker save todo-auth-service:latest -o todo-auth.tar  
docker save todo-todo-service:latest -o todo-todo.tar  
docker save todo-alarm-service:latest -o todo-alarm.tar  
docker save todo-todo-frontend:latest -o todo-frontend.tar

### 3. Import Images to K3s
sudo k3s ctr images import todo-auth.tar  
sudo k3s ctr images import todo-todo.tar  
sudo k3s ctr images import todo-alarm.tar  
sudo k3s ctr images import todo-frontend.tar

### 4. Apply Kubernetes Manifests
cd k8s  
kubectl apply -f .  
kubectl apply -f auth-service/  
kubectl apply -f todo-service/  
kubectl apply -f alarm-service/  
kubectl apply -f frontend/

---

## CI/CD with Jenkins

- Triggered by GitHub webhook on push
- Pipeline:
  1. Clone repository
  2. Build Docker images
  3. Push images to K3s container registry
  4. Apply Kubernetes manifests

---

## Email Configuration

- Uses SMTP account to send task alarms
- User email is registered in auth-service for alarm-service

---

## Deployment Video

[Watch Video](INSERT_YOUR_VIDEO_LINK_HERE)

---

## Contact

Mohanad Hesham El-Sayed Mahmoud  
For questions or support, feel free to reach out.

## Project Structure

