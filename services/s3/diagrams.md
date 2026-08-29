---
service: S3
category: diagrams
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# Amazon S3 - Architecture Diagrams

These Mermaid diagrams illustrate common storage patterns and concepts.

### 1. Secure Static Website Architecture

Using CloudFront and OAC to securely serve content from a private S3 bucket.

```mermaid
graph LR
    User((User)) -->|HTTPS| CF[Amazon CloudFront]
    
    subgraph AWS Cloud
        CF -->|Origin Access Control| S3[(S3 Bucket)]
        
        note1[Block Public Access: ON] -.-> S3
        note2[Bucket Policy: Allow CloudFront ARN] -.-> S3
    end
```

### 2. S3 Lifecycle Data Tiering

Automating cost optimization over time.

```mermaid
graph TD
    A[Day 0: Object Uploaded] --> B(S3 Standard)
    B -->|High Performance, High Cost| C{30 Days Passed?}
    C -->|Yes| D(S3 Standard-IA)
    D -->|Lower Storage Cost, Retrieval Fees| E{90 Days Passed?}
    E -->|Yes| F(S3 Glacier Flexible Retrieval)
    F -->|Lowest Cost, Minutes/Hours to Retrieve| G{365 Days Passed?}
    G -->|Yes| H[Object Deleted / Expired]
```

### 3. S3 Cross-Region Replication with KMS

Illustrating the IAM permissions required to replicate KMS-encrypted objects.

```mermaid
sequenceDiagram
    participant App
    participant Source S3 (US-East-1)
    participant KMS Key A
    participant Replication Role
    participant Dest S3 (EU-West-1)
    participant KMS Key B
    
    App->>Source S3: PUT Object (SSE-KMS Key A)
    Source S3->>KMS Key A: Encrypt Data
    
    Note over Replication Role: Asynchronous Process
    
    Source S3->>Replication Role: Trigger Replication
    Replication Role->>KMS Key A: kms:Decrypt
    Replication Role->>KMS Key B: kms:Encrypt
    Replication Role->>Dest S3: s3:ReplicateObject
```

### 4. S3 Object Lambda Dynamic Redaction

Intercepting GET requests to manipulate data on the fly.

```mermaid
graph TD
    Client[Application/User] -->|GET Request| AP_OL[Object Lambda Access Point]
    AP_OL --> L[AWS Lambda Function]
    
    subgraph Data Processing
        L -->|Fetch Raw Data| S3[(S3 Bucket: Standard Access Point)]
        S3 -->|Raw Data: SSNs| L
        L -->|Redact Data: Regex| L
    end
    
    L -->|Return Redacted Data| Client
```
