---
service: Lambda
category: diagrams
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
---

# AWS Lambda - Architecture Diagrams

These Mermaid diagrams illustrate common serverless patterns and concepts.

### 1. The Fanout Pattern

This pattern allows asynchronous parallel processing of a single event.

```mermaid
graph LR
    A[Client App] -->|Publish Event| B(Amazon SNS Topic)
    B -->|Fanout| C(SQS Queue: Emails)
    B -->|Fanout| D(SQS Queue: Analytics)
    B -->|Fanout| E(SQS Queue: Provisioning)
    
    C --> F[Lambda: Send Email]
    D --> G[Lambda: Update Data Warehouse]
    E --> H[Lambda: Provision Resources]
    
    F -.->|Failure| I(DLQ)
    G -.->|Failure| J(DLQ)
```

### 2. SQS Batch Processing with Partial Failures

Illustrating how Lambda handles batches and returns partial failures.

```mermaid
sequenceDiagram
    participant SQS
    participant Lambda ESM as Event Source Mapping
    participant Lambda code as Function Code
    
    Lambda ESM->>SQS: Poll for messages
    SQS-->>Lambda ESM: Returns Batch of 5 (A, B, C, D, E)
    Lambda ESM->>Lambda code: Synchronous Invocation (Batch)
    
    Note over Lambda code: Message C throws exception
    
    Lambda code-->>Lambda ESM: Return { batchItemFailures: [{ itemIdentifier: "C" }] }
    
    Lambda ESM->>SQS: Delete A, B, D, E from Queue
    Note over SQS: Message C remains visible for retry
```

### 3. API Gateway Serverless Backend

A highly scalable synchronous web application backend.

```mermaid
graph TD
    User((User)) -->|HTTPS| CF[Amazon CloudFront]
    CF -->|Cached Content| S3[S3 Static Website]
    CF -->|Dynamic API Calls| WAF{AWS WAF}
    WAF --> API[API Gateway]
    API -->|Proxy Integration| L_Auth[Lambda Authorizer]
    L_Auth -.->|Verify JWT| Cognito[Amazon Cognito]
    API -->|Proxy Integration| L_Logic[Lambda: Business Logic]
    
    L_Logic <-->|Read/Write| DDB[(DynamoDB)]
    L_Logic -->|Get Secret| SM[Secrets Manager]
```

### 4. Step Functions Saga Pattern

Handling distributed transactions and rollbacks.

```mermaid
stateDiagram-v2
    [*] --> BookFlight
    BookFlight --> BookHotel: Success
    BookFlight --> [*]: Failure
    
    BookHotel --> ProcessPayment: Success
    BookHotel --> CancelFlight: Failure
    
    ProcessPayment --> CompleteTransaction: Success
    ProcessPayment --> CancelHotel: Failure
    
    CancelHotel --> CancelFlight
    CancelFlight --> [*]: Transaction Rolled Back
    
    CompleteTransaction --> [*]: Transaction Successful
```
