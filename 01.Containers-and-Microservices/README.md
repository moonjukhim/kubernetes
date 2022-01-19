Container Registry에 Docker Image 저장

```
# 환경 변수 설정
export PROJECT_ID=[CHANGE TO YOUR PROJECT ID]
export CLUSTER_NAME=central
export CLUSTER_ZONE=us-central1-b

gcloud container clusters get-credentials $CLUSTER_NAME \
    --zone $CLUSTER_ZONE --project $PROJECT_ID

docker build -t gcr.io/$PROJECT_ID/app:v1 .
docker push gcr.io/$PROEJCT_ID/app:v1

# kubectl create deployment app --image=gcr.io/$PROJECT_ID/app:v1
kubectl exec --stdin --tty [POD_NAME] -- /bin/bash
```
