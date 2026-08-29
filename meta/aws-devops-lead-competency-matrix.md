---
service: Meta
category: Competency Matrix
difficulty_levels: ["L1", "L2", "L3", "L4"]
aws_exam_relevance: ["All"]
maturity_tier: N/A
last_validated_date: "2026-08-29"
version: "1.0"
cross_references:
  - ../meta/study-schedule.md
---

# AWS DevOps Lead Competency Matrix

This matrix is designed to help you self-assess your readiness for Senior (L3) and Principal/Lead (L4) DevOps & Cloud Architecture roles.

## Assessment Pillars

### 1. IaC & GitOps
- **L1 (Junior):** Can read CloudFormation/Terraform and make minor updates. Understands basic git commands.
- **L2 (Mid):** Can write templates from scratch. Understands state management. Sets up simple CI/CD pipelines.
- **L3 (Senior):** Modules design, terragrunt, complex state manipulations, automated testing of IaC (checkov, tfsec). CI/CD at scale.
- **L4 (Lead):** Enterprise GitOps architecture, cross-account automated deployments, defining IDP (Internal Developer Platforms).

### 2. Observability
- **L1:** Can search logs in CloudWatch. Sets up basic alarms.
- **L2:** Creates dashboards. Uses CloudTrail for auditing. Understands metrics vs logs.
- **L3:** Configures distributed tracing (X-Ray/OpenTelemetry). APM integrations. Automated remediation based on alarms.
- **L4:** Designs holistic enterprise observability strategy. SLO/SLI/SLA definitions and tracking. Cost-effective telemetry architectures.

### 3. Multi-Account Security
- **L1:** Understands IAM users, groups, roles, and basic policies.
- **L2:** Uses cross-account roles. Implements KMS encryption. Understands security groups vs NACLs.
- **L3:** SCPs, AWS Organizations, Control Tower customization, IAM permission boundaries, identity federation (OIDC/SAML).
- **L4:** Zero-trust architecture, automated incident response (GuardDuty/Macie/Security Hub), compliance-as-code.

### 4. Kubernetes & Containers
- **L1:** Can run docker containers. Understands ECS basics.
- **L2:** Deploys apps to EKS/ECS. Writes Dockerfiles. Understands Fargate.
- **L3:** EKS cluster administration, Helm, ingress controllers, pod security, cluster autoscaler/Karpenter.
- **L4:** Multi-cluster/multi-region mesh (Istio), platform engineering, tenant isolation, advanced GitOps with ArgoCD/Flux.

### 5. Reliability & Disaster Recovery (DR)
- **L1:** Understands Multi-AZ vs Multi-Region. Can restore an RDS snapshot.
- **L2:** Implements Auto Scaling. Sets up basic backup policies.
- **L3:** Implements Pilot Light/Warm Standby DR. RTO/RPO calculation. RDS Multi-Region replication, DynamoDB Global Tables.
- **L4:** Chaos Engineering, Active-Active multi-region architectures, Route 53 complex routing policies, resilience at enterprise scale.

### 6. FinOps & Cost Optimization
- **L1:** Views Cost Explorer. Understands basics of EC2 pricing.
- **L2:** Implements tagging strategies. Sets up budget alerts.
- **L3:** Savings Plans, Spot instances, automated rightsizing, Graviton migrations.
- **L4:** Enterprise chargeback models, Unit Economics, FinOps culture implementation, architectural redesigns for cost efficiency.

---

## Self-Assessment Rubric

Rate yourself 1-4 on each pillar:
- **Total Score 6-11:** Junior DevOps
- **Total Score 12-17:** Mid-Level DevOps
- **Total Score 18-22:** Senior DevOps Engineer / Cloud Architect (L3 ready)
- **Total Score 23-24:** Principal / Lead (L4 ready)

## Sample Behavioral Questions by Pillar

- **IaC/GitOps:** "Tell me about a time you had to refactor a large monolithic IaC codebase. How did you handle state migration without downtime?"
- **Observability:** "Describe a complex production incident you resolved. How did your observability tools help or hinder you, and what did you improve afterward?"
- **Security:** "How have you balanced developer velocity with strict security and compliance requirements?"
- **Kubernetes:** "Explain your strategy for upgrading a production EKS cluster with zero downtime."
- **Reliability:** "Tell me about a time an architecture you designed failed in production. What was the root cause and how did you fix it?"
- **FinOps:** "Describe a scenario where you significantly reduced cloud spend. How did you identify the waste and implement the change?"
