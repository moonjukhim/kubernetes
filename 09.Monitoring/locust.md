1. 환경변수 설정

```bash
REGION=us-central1
ZONE=${REGION}-a
PROJECT=$(gcloud config get-value project)
CLUSTER=gke-load-test
TARGET=${PROJECT}.appspot.com
SCOPE="https://www.googleapis.com/auth/cloud-platform"

gcloud config set compute/zone ${ZONE}
gcloud config set project ${PROJECT}
```

2. 환경설정

```bash
git clone https://github.com/GoogleCloudPlatform/distributed-load-testing-using-kubernetes
cd distributed-load-testing-using-kubernetes
```

3. GKE 클러스터 만들기

```
gcloud container clusters create $CLUSTER \
   --zone $ZONE \
   --scopes $SCOPE \
   --enable-autoscaling --min-nodes "1" --max-nodes "3" \
   --num-nodes 1 \
   --scopes=logging-write,storage-ro \
   --addons HorizontalPodAutoscaling,HttpLoadBalancing

gcloud container clusters get-credentials $CLUSTER \
   --zone $ZONE \
   --project $PROJECT
```

4. Docker 이미지 빌드

```bash
gcloud builds submit \
    --tag gcr.io/$PROJECT/locust-tasks:latest docker-image

gcloud container images list | grep locust-tasks
```

5. 샘플 애플리케이션 배포

```bash
sed -i -e "s/\[TARGET_HOST\]/$TARGET/g" kubernetes-config/locust-master-controller.yaml
sed -i -e "s/\[TARGET_HOST\]/$TARGET/g" kubernetes-config/locust-worker-controller.yaml
sed -i -e "s/\[PROJECT_ID\]/$PROJECT/g" kubernetes-config/locust-master-controller.yaml
sed -i -e "s/\[PROJECT_ID\]/$PROJECT/g" kubernetes-config/locust-worker-controller.yaml

kubectl apply -f kubernetes-config/locust-master-controller.yaml
kubectl apply -f kubernetes-config/locust-master-service.yaml
kubectl apply -f kubernetes-config/locust-worker-controller.yaml
kubectl get pods -o wide

kubectl get services
kubectl get svc locust-master --watch
EXTERNAL_IP=$(kubectl get svc locust-master -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
```


```bash
kubectl scale deployment/locust-worker --replicas=30
```


https://cloud.google.com/architecture/distributed-load-testing-using-gke
