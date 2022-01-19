Container Registry에 Docker Image 저장

```
export PROJECT_ID=[CHANGE TO YOUR PROJECT ID]
docker build -t gcr.io/$PROJECT_ID/app:v1 .
docker push gcr.io/$PROEJCT_ID/app:v1

# kubectl create deployment app --image=gcr.io/$PROJECT_ID/app:v1
kubectl exec --stdin --tty [POD_NAME] -- /bin/bash
```
