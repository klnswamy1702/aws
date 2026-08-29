---
service: Lambda
category: architecture
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Architecture Interview Questions (L4)

### Q1: Compare Lambda, Fargate, and ECS/EKS. How do you decide which to use for a new microservice?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, Fargate, ECS

> **Quick Answer:** Use Lambda for event-driven, short-lived tasks with bursty traffic; Fargate for long-running, consistent stateless workloads without OS management; and ECS/EKS on EC2 for workloads requiring custom OS tuning, GPUs, or persistent heavy state.

#### Detailed Answer
**Decision Framework:**
1. **Execution Duration**: If the process takes >15 minutes, Lambda is immediately ruled out. Use Fargate.
2. **Traffic Pattern**: If traffic is highly bursty and unpredictable (e.g., 0 requests to 10,000 in seconds), Lambda scales faster than Fargate. Fargate container scaling (ECS Service Auto Scaling) takes minutes.
3. **Cost**: Lambda charges per invocation/millisecond. At very high, constant throughput (e.g., thousands of requests per second 24/7), the cost of Lambda will surpass the cost of keeping a few Fargate tasks running continuously.
4. **Portability**: If the company mandates vendor-neutral containers (Kubernetes), EKS/Fargate is required. Lambda functions are highly tied to AWS ecosystems.

---

### Q2: How do you design a Serverless API to handle 100,000 requests per second securely and reliably?
**Level:** L4 | **Category:** architecture
**Target Services:** API Gateway, Lambda, DynamoDB

> **Quick Answer:** Use a multi-layered architecture: CloudFront for Edge caching, WAF for security, API Gateway with strict throttling/quotas, Provisioned Concurrency on Lambda to prevent cold starts, and DynamoDB for scalable backend storage.

#### Detailed Answer
At 100k RPS, naive serverless architectures will hit account limits and fail catastrophically.
1. **Edge**: Route traffic through CloudFront. Cache GET requests aggressively to offload the backend. Attach AWS WAF to block DDoS.
2. **API Layer**: API Gateway must have Usage Plans, API Keys, and strict throttling limits configured to protect downstream services.
3. **Compute**: Lambda default regional concurrency is 1000. You must request a quota increase. Configure **Provisioned Concurrency** to ensure execution environments are pre-warmed. Use Lambda Powertools for optimized logging (sampling rather than logging every request to avoid massive CloudWatch costs).
4. **Data Layer**: Use DynamoDB with On-Demand capacity (or auto-scaled Provisioned capacity) and DynamoDB Accelerator (DAX) to handle the database read/write volume.

---

### Q3: Explain the Fanout pattern using SNS, SQS, and Lambda.
**Level:** L4 | **Category:** architecture
**Target Services:** SNS, SQS, Lambda

> **Quick Answer:** The Fanout pattern involves an SNS topic broadcasting a single event to multiple SQS queues, each of which is polled by an independent Lambda function, enabling parallel asynchronous processing.

#### Detailed Answer
If a single event (e.g., UserRegistered) requires multiple actions (SendWelcomeEmail, UpdateAnalytics, ProvisionResources), having one Lambda function do all three synchronously is an anti-pattern (brittle, slow, hard to retry).
**Architecture**:
1. Application publishes `UserRegistered` event to an SNS Topic.
2. Three independent SQS Queues are subscribed to the Topic.
3. SNS "fans out" the message, placing a copy in all three queues.
4. Three distinct Lambda functions use Event Source Mapping to poll their respective queues.
If the Email service is down, only the `SendWelcomeEmail` Lambda fails, and its specific SQS queue retains the message for retries, while analytics and provisioning succeed.

---

### Q4: How do you design an Event-Driven architecture to guarantee idempotency in Lambda?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, DynamoDB

> **Quick Answer:** Idempotency ensures that processing the same event multiple times yields the exact same result. It is achieved by extracting a unique idempotency key from the event and tracking its processing state in a fast database like DynamoDB.

#### Detailed Answer
Because AWS services (like SQS, SNS, EventBridge) guarantee "at-least-once" delivery, your Lambda function *will* eventually receive duplicate events.
**Implementation**:
1. Extract a unique ID from the payload (e.g., `transaction_id`).
2. Before processing, Lambda attempts to write the `transaction_id` to a DynamoDB table with a `ConditionExpression` that the ID does not already exist.
3. If the write succeeds, the Lambda processes the event.
4. If the write fails (ConditionalCheckFailedException), it means the event was already processed. The Lambda should gracefully return a 200 OK without re-processing.
AWS Lambda Powertools provides an Idempotency utility that implements this exact pattern out-of-the-box.

---

### Q5: Describe the Saga Pattern using AWS Step Functions and Lambda for distributed transactions.
**Level:** L4 | **Category:** architecture
**Target Services:** Step Functions, Lambda

> **Quick Answer:** The Saga pattern manages distributed transactions by breaking them into a sequence of local transactions (Lambda functions). If one step fails, the Saga executes compensating transactions (rollback functions) to undo the previous steps.

#### Detailed Answer
In microservices, you cannot use traditional ACID database locks across different services (e.g., Inventory DB and Payment DB).
Using AWS Step Functions:
1. **State 1**: Lambda deducts inventory.
2. **State 2**: Lambda processes payment.
3. If Payment fails, the Step Function catches the error and transitions to a **Compensating State**.
4. **Compensating State**: Lambda adds the inventory back.
This ensures eventual consistency without locking databases.

---

### Q6: How do you architect a multi-region Active-Active serverless application?
**Level:** L4 | **Category:** architecture
**Target Services:** Route 53, API Gateway, Lambda, DynamoDB

> **Quick Answer:** Use Route 53 latency-based routing to direct users to the nearest region. Each region has its own API Gateway and Lambda stack, reading/writing to a DynamoDB Global Table that handles cross-region asynchronous replication.

#### Detailed Answer
1. **Routing**: Route 53 with Latency or Geolocation routing policies.
2. **Compute**: Independent stacks of API Gateway and Lambda in `us-east-1` and `eu-west-1`.
3. **Data**: DynamoDB Global Tables provide multi-active replication. Writes in `us-east-1` are asynchronously replicated to `eu-west-1` within a second.
4. **Conflict Resolution**: DynamoDB Global Tables use "last writer wins" based on timestamps to resolve concurrent updates to the same item across regions.
This architecture provides extreme fault tolerance (surviving a full AWS region outage) and minimal latency for global users.

---

### Q7: Compare EventBridge and SNS for routing events to Lambda in complex architectures.
**Level:** L4 | **Category:** architecture
**Target Services:** EventBridge, SNS, Lambda

> **Quick Answer:** SNS is designed for high-throughput, simple pub/sub fanout. EventBridge is designed for complex, schema-based event routing, content-filtering, and integrating third-party SaaS applications.

#### Detailed Answer
- **SNS**: Pushes messages to subscribers. Filtering is limited to message attributes. It is extremely fast and scalable, ideal for internal microservice communication.
- **EventBridge**: An event bus that inspects the entire JSON body of the event. You can write complex routing rules (e.g., route to Lambda A if `detail.department == "sales" && detail.amount > 100`). It natively integrates with AWS CloudTrail events and SaaS providers (Zendesk, Datadog, Shopify). EventBridge is preferred for decoupled, enterprise-wide event choreography.

---

### Q8: How do you handle secrets management in Lambda at a massive scale to avoid API throttling?
**Level:** L4 | **Category:** architecture
**Target Services:** Lambda, Secrets Manager, Parameter Store

> **Quick Answer:** Do not call Secrets Manager on every invocation. Fetch the secret once during the Lambda initialization phase, store it in a global variable in memory, and use the AWS Parameters and Secrets Lambda Extension for local caching.

#### Detailed Answer
Calling `GetSecretValue` inside the Lambda handler results in an API call for every single execution. At high concurrency, this will throttle the Secrets Manager API and drastically increase latency and cost.
**Best Practice**:
1. Use the AWS Parameters and Secrets Lambda Extension. It runs a local HTTP server inside the Lambda execution environment.
2. Your code makes a local HTTP GET request to `localhost:2773`.
3. The extension fetches the secret from AWS, caches it in memory for a configurable TTL (e.g., 5 minutes), and returns it instantly to the function.

---

### Q9: Design a system to process a massive, unpredictable backlog of SQS messages using Lambda while preventing downstream API rate limits.
**Level:** L4 | **Category:** architecture
**Target Services:** SQS, Lambda

> **Quick Answer:** Configure the SQS Event Source Mapping with a specific `BatchSize` and use Lambda Reserved Concurrency to strictly cap the number of concurrent executions, ensuring the downstream API is never overwhelmed.

#### Detailed Answer
If an SQS queue suddenly receives 1 million messages, Lambda will rapidly scale up to 1,000 concurrent executions. If the Lambda calls a third-party API (e.g., Salesforce) that only allows 50 requests per second, the API will reject the requests (HTTP 429), messages will fail, and SQS will redeliver them in a catastrophic loop.
**Solution**:
1. Set **Reserved Concurrency** on the Lambda function to 10 (example).
2. Lambda will only poll SQS enough to keep 10 environments busy.
3. If `BatchSize` is 5, the maximum requests to the downstream API is capped perfectly. The rest of the messages wait safely in SQS.

---

### Q10: How do you architect a WebSocket-based real-time chat application using serverless technologies?
**Level:** L4 | **Category:** architecture
**Target Services:** API Gateway, Lambda, DynamoDB

> **Quick Answer:** Use API Gateway WebSocket APIs to manage persistent client connections, Lambda to handle connection/disconnection events and message routing, and DynamoDB to store active connection IDs and chat history.

#### Detailed Answer
Lambda itself is stateless and short-lived, so it cannot hold a persistent WebSocket connection open.
1. **Connection**: Client connects to API Gateway WebSocket endpoint.
2. **State Management**: API Gateway triggers a `$connect` Lambda function. The function saves the generated `connectionId` (provided by API Gateway) to a DynamoDB table.
3. **Messaging**: Client sends a message. API Gateway triggers a `sendMessage` Lambda. The Lambda queries DynamoDB for all active `connectionId`s in that chat room.
4. **Push**: The Lambda uses the API Gateway Management API SDK to execute `postToConnection`, pushing the message out to all connected clients.
5. **Disconnection**: A `$disconnect` Lambda removes the ID from DynamoDB.
