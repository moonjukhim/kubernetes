### 04. Kubernetes 기본 개념

kubectl 명령을 통해서 쿠버네티스 클러스터 생성

```bash
export my_zone=us-central1-a
export my_cluster=my-cluster1

gcloud container clusters create $my_cluster --num-nodes 3 --zone $my_zone --enable-ip-alias

gcloud container clusters get-credentials $my_cluster --zone $my_zone
```