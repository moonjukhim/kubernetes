### 04. Kubernetes 기본 개념

User A : kubectl 명령을 통해서 쿠버네티스 클러스터 생성

```bash
export my_zone=us-central1-a
export my_cluster=my-cluster1
gcloud container clusters create $my_cluster --num-nodes 3 --zone $my_zone --enable-ip-alias
gcloud container clusters get-credentials $my_cluster --zone $my_zone
```

User A : 네임스페이스 생성하기

```bash
kubectl create namespace rbac-test
```


user B : 접속 정보 가져오기

```bash
export my_zone=us-central1-a
export my_cluster=standard-cluster-1
gcloud container clusters get-credentials $my_cluster --zone $my_zone
```