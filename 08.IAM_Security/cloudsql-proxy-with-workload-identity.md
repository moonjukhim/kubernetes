0. Cloud SQL 인스턴스 생성

```bash
gcloud sql instances create my-instance1 --tier=db-n1-standard-2 --region=us-central1
export SQL_NAME=my-instance1
gcloud sql connect my-instance1
gcloud sql instances describe INSTANCE_ID
```

1. Google Service Account 생성

```bash
gcloud iam service-accounts create gsa-for-gke \
    --description="gsa-for-gke" \
    --display-name="gsa-for-gke"
```



2. GKE Cluster 생성 

```bash
export my_zone=us-central1-a
export my_cluster=my-cluster2
export PROJECT_ID=$(gcloud config get-value core/project) 
export KSA="ksa-for-cloudsql"
export GSA="gsa-for-gke"
gcloud container clusters create $my_cluster --num-nodes 3 --zone $my_zone \
  --scopes=sql-admin,default  

#gcloud container clusters update ${my_cluster} \
# --workload-pool=${PROJECT_ID}.svc.id.goog \
# --zone ${my_zone}
```


3. Kubernetes Service Account 생성

```bash
cat <<'EOF' >> ksa-for-cloudsql.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ksa-for-cloudsql
EOF
kubectl apply -f ksa-for-cloudsql.yaml
```


4. KSA와 GSA 연결

```bash
export KSA="ksa-for-cloudsql"
export GSA="gsa-for-gke"
gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${PROJECT_ID}.svc.id.goog[default/${KSA}]" \
  ${GSA}@${PROJECT_ID}.iam.gserviceaccount.com
```


5. KSA와 GSA 어노테이션 설정

```bash
kubectl annotate serviceaccount \
   --overwrite=true \
   ${KSA} \
   iam.gke.io/gcp-service-account=${KSA}@${PROJECT_ID}.iam.gserviceaccount.com 
##  --namespace default \
```


6. 읽기/쓰기 권한 설정

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
--member=serviceAccount:${GSA}@${PROJECT_ID}.iam.gserviceaccount.com \
--role=roles/cloudsql.client
```

7. 테스트

```bash
#kubectl run -it \
#  --image google/cloud-sdk:slim \
#  --serviceaccount ${KSA} \
#  --namespace default \
#  workload-identity-test
```

8. 컨테이너에서 수행

```bash
# gsutil ls
```


9. WordPress 애플리케이션 배포

```bash
export SQL_NAME=fluent-optics-321005:us-central1:my-instance1 # 사용자의 CONNECTION NAME으로 변경 !!!
sed -i 's/<INSTANCE_CONNECTION_NAME>/'"${SQL_NAME}"'/g'\
   proxy-with-workload-identity.yaml
kubectl apply -f proxy-with-workload-identity.yaml
```


10. 리소스 정리

```bash
export my_zone=us-central1-a
export my_cluster=my-cluster1
export PROJECT_ID=$(gcloud config get-value core/project) 

gcloud container clusters delete $my_cluster --zone $my_zone
gcloud iam service-accounts delete ${GSA}@${PROJECT_ID}.iam.gserviceaccount.com
```


