---
service: ECR
category: hands-on
difficulty_levels: L2-L3
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ecs/hands-on-labs.md
---
# Amazon ECR - Hands-on Labs

## Lab 1: Create, Authenticate, and Push a Docker Image to ECR

**Objective:** Learn the basic lifecycle of an ECR repository using the AWS CLI.

**Steps:**
1. Create an ECR repository:
   ```bash
   aws ecr create-repository --repository-name my-web-app --image-scanning-configuration scanOnPush=true
   ```
2. Authenticate Docker with your ECR registry:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   ```
3. Pull a sample image and tag it for your ECR repo:
   ```bash
   docker pull nginx:alpine
   docker tag nginx:alpine <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/my-web-app:v1
   ```
4. Push the image:
   ```bash
   docker push <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/my-web-app:v1
   ```
5. Verify the image and its vulnerability scan results in the AWS Console.

## Lab 2: Configure ECR Lifecycle Policies

**Objective:** Automate cost savings by expiring old container images.

**Steps:**
1. Create a file named `policy.json`:
   ```json
   {
       "rules": [
           {
               "rulePriority": 1,
               "description": "Keep last 5 tagged images, expire others",
               "selection": {
                   "tagStatus": "any",
                   "countType": "imageCountMoreThan",
                   "countNumber": 5
               },
               "action": {
                   "type": "expire"
               }
           }
       ]
   }
   ```
2. Apply the policy to your repository:
   ```bash
   aws ecr put-lifecycle-policy \
       --repository-name my-web-app \
       --lifecycle-policy-text file://policy.json
   ```

## Lab 3: Setup Cross-Region Replication

**Objective:** Replicate images automatically for disaster recovery.

**Steps:**
1. Navigate to Amazon ECR in the AWS Console.
2. Go to **Private registry** -> **Replication configuration**.
3. Click **Add replication rule**.
4. Set the destination region (e.g., `us-west-2`).
5. Add a repository filter (e.g., Prefix: `my-web-app`).
6. Save the rule.
7. Push a new tag to the primary region and verify it appears in the destination region.
