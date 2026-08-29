---
service: EBS
category: hands-on
difficulty_levels: [L2, L3]
---
# EBS Hands-on Labs

## Lab 1: Seamless Migration from gp2 to gp3
**Objective:** Migrate an active root volume from gp2 to gp3 using the CLI with zero downtime.
<details>
<summary>Step-by-Step</summary>
1. Identify Volume ID: `aws ec2 describe-volumes`
2. Modify volume: 
   `aws ec2 modify-volume --volume-id vol-0abcd1234 --volume-type gp3`
3. Monitor status: 
   `aws ec2 describe-volumes-modifications --volume-id vol-0abcd1234`
The volume remains available and usable during the `optimizing` state.
</details>

## Lab 2: EBS Snapshot Lifecycle with DLM
**Objective:** Create a DLM policy to snapshot instances daily and retain for 7 days.
<details>
<summary>Step-by-Step</summary>
1. Tag instances: `Backup=Daily`.
2. Create IAM Role for DLM.
3. Use `aws dlm create-lifecycle-policy` with a JSON schedule targeting the `Backup=Daily` tag, setting `Interval: 24`, `RetainRule: {Count: 7}`.
</details>
