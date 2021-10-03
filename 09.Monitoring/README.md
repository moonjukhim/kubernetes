1. 클러스터 생성

```bash
export my_zone=us-central1-a
export my_cluster=my-cluster1
gcloud container clusters create $my_cluster --num-nodes 3 --zone $my_zone \
    --enable-ip-alias --logging --monitoring
gcloud container clusters get-credentials $my_cluster --zone $my_zone
git clone https://github.com/moonjukhim/kubernetes.git
```

2. 디플로이먼트 배포

