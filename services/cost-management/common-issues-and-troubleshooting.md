---
service: Cost Management
category: troubleshooting
difficulty_levels:
  - L2
  - L3
---

# AWS Cost Management - Common Issues and Troubleshooting

## 1. Unattributed or Uncategorized Costs
**Symptoms**: A large portion of the AWS bill appears under "No TagKey" in Cost Explorer.
**Troubleshooting**: Ensure Cost Allocation Tags are actively enabled in the Billing Console (they are not enabled by default, even if they exist on the resources). Note that it can take up to 24 hours for tags to appear in Cost Explorer after activation.

## 2. Savings Plan / RI Underutilization
**Symptoms**: The Savings Plan utilization report shows less than 80% utilization.
**Troubleshooting**: You may have committed to a spend higher than your actual usage, or application teams have migrated to a service not covered by the specific plan (e.g., moving from EC2 to ECS Fargate when holding an EC2 Instance Savings Plan). Always analyze historical usage over 30-90 days before committing.

## 3. Unexpected Spikes in Data Transfer Costs
**Symptoms**: A sudden massive bill for `DataTransfer-Out-Bytes`.
**Troubleshooting**: Data transfer is notoriously difficult to track. Enable VPC Flow Logs, publish them to CloudWatch or S3, and use Athena to identify which IP addresses or ENIs are responsible for the egress traffic. Common culprits are EC2 instances communicating across Availability Zones (which incurs charges) or downloading large amounts of data to the public internet without a CDN like CloudFront.
