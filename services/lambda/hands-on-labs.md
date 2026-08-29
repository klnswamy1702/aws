---
service: Lambda
category: practical
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: High
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ./overview.md
---

# AWS Lambda - Hands-on Labs

These labs are designed to take you from a basic serverless API to a complex, resilient event-driven architecture.

## Lab 1: Serverless REST API with API Gateway and Lambda (L2)
**Objective**: Build a basic CRUD API using API Gateway (HTTP API) and a Python Lambda function connecting to DynamoDB.

1. **DynamoDB**: Create a table named `Users` with partition key `user_id` (String).
2. **IAM**: Create a Lambda execution role with `AWSLambdaBasicExecutionRole` and an inline policy allowing `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Scan`.
3. **Lambda**: Write a Python function using `boto3` that parses the `event['routeKey']`.
   - `POST /users`: Parse `event['body']`, write to DynamoDB.
   - `GET /users/{user_id}`: Fetch from DynamoDB.
4. **API Gateway**: Create an HTTP API, configure routes mapping to the Lambda function.
5. **Testing**: Use `curl` or Postman to test the CRUD operations.

---

## Lab 2: S3 Event-Driven Image Resizer (L3)
**Objective**: Automatically resize images uploaded to S3.

1. **S3**: Create two buckets: `image-upload-source` and `image-processed-dest`.
2. **Lambda Layer**: Create a Lambda Layer containing the Python `Pillow` (PIL) library, as it requires compiled C binaries compatible with Amazon Linux 2.
3. **Lambda**: 
   - Parse the S3 event from the `event` payload.
   - Download the image from the source bucket to `/tmp`.
   - Resize the image using PIL.
   - Upload the resized image to the destination bucket.
4. **Trigger**: Configure the source bucket to trigger the Lambda on `s3:ObjectCreated:*` with a `.jpg` suffix.
5. **Testing**: Upload a large image and verify the thumbnail appears in the destination bucket. *Crucial: Ensure the Lambda does NOT write back to the source bucket to prevent infinite loops.*

---

## Lab 3: Resilient SQS Consumer with DLQ (L3)
**Objective**: Process messages from an SQS queue robustly, handling failures.

1. **SQS**: Create a standard queue `OrderQueue` and a Dead Letter Queue `OrderDLQ`.
2. **Redrive Policy**: Configure `OrderQueue` to send messages to `OrderDLQ` after 3 failed receives.
3. **Lambda**: Write code that deliberately fails (throws an exception) if the message body contains the word "FAIL".
4. **Event Source Mapping**: Connect Lambda to `OrderQueue` with a batch size of 5. Enable `ReportBatchItemFailures`.
5. **Testing**: Send 5 messages (3 normal, 2 containing "FAIL"). Observe CloudWatch logs. Verify the 2 failed messages end up in the DLQ while the others succeed.

---

## Lab 4: Step Functions Orchestration (L4)
**Objective**: Coordinate a multi-step workflow using AWS Step Functions.

1. **Lambda Functions**: Create three simple functions: `CheckInventory`, `ProcessPayment`, `ShipOrder`.
2. **Step Function**: Create a State Machine in ASL (Amazon States Language).
   - Start -> `CheckInventory`.
   - Choice State: If inventory > 0, go to `ProcessPayment`. Else, go to `Fail`.
   - `ProcessPayment` -> `ShipOrder`.
3. **Error Handling**: Modify `ProcessPayment` to randomly throw a `PaymentDeclinedException`. Configure the Step Function to catch this exception and transition to a `CancelOrder` Lambda function (Compensating transaction).
4. **Testing**: Execute the State Machine with different inputs and visualize the execution graph in the AWS Console.

---

## Lab 5: Edge Computing with Lambda@Edge (L4)
**Objective**: Manipulate HTTP headers at the edge using CloudFront.

1. **CloudFront**: Create a distribution pointing to an S3 static website.
2. **Lambda**: Create a Node.js function in the `us-east-1` region (required for Lambda@Edge).
   - Code: Intercept the viewer response and inject security headers like `Strict-Transport-Security` and `X-Content-Type-Options`.
3. **Permissions**: The execution role must trust both `lambda.amazonaws.com` and `edgelambda.amazonaws.com`.
4. **Deploy**: Publish a version of the Lambda function and associate it with the CloudFront distribution's "Viewer Response" event.
5. **Testing**: Access the CloudFront URL and inspect the HTTP headers using browser dev tools.
