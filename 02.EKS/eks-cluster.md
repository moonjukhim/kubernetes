```bash
eksctl create cluster \
--name dev-cluster \
--nodegroup-name dev-nodes \
--node-type t3.small \
--nodes 3 \
--nodes-min 1 \
--nodes-max 4 \
--version 1.21 \
--region ${AWS_REGION}
```