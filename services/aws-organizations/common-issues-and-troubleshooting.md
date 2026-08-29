---
service: AWS Organizations
category: Management & Governance
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, Security Specialty
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../aws-organizations/overview.md
---

# AWS Organizations Common Issues & Troubleshooting

## 1. IAM User Cannot Perform Action Despite Having AdministratorAccess
- **Issue**: A user in a member account has `AdministratorAccess` but gets an `AccessDenied` error when trying to provision an RDS instance.
- **Cause**: An SCP attached to the account, its parent OU, or the Root is denying the action (e.g., denying all actions outside of `us-east-1`, or explicitly denying RDS creation). SCPs always override IAM policies.
- **Troubleshooting**: Check CloudTrail for the specific deny reason, and review the effective SCPs in the AWS Organizations console from the Management Account.

## 2. Cannot Leave an Organization
- **Issue**: A member account attempts to leave an organization but the action is blocked.
- **Cause**: The account might not have the necessary payment information (credit card), phone number verification, or a support plan configured, which are required to operate as a standalone account.
- **Solution**: Complete the standalone account sign-up steps in the Billing console before attempting to leave.

## 3. SCP Too Large (Size Limit Exceeded)
- **Issue**: Cannot save an SCP because it exceeds the maximum size limit (5,120 bytes).
- **Solution**: 
  - Remove whitespaces (minify the JSON).
  - Combine statements with similar effects.
  - Split the policy into multiple SCPs and attach them to the same OU/Account.

## 4. Savings Plans/RIs Applying to the Wrong Account
- **Issue**: Compute capacity discounts bought by Team A are being consumed by Team B.
- **Cause**: Consolidated billing shares RI and Savings Plan benefits across all accounts in the Organization by default.
- **Solution**: Disable discount sharing for specific accounts or groups of accounts in the Billing console.
