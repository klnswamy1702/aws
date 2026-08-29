---
service: CodeBuild
category: best-practices
difficulty_levels: [L2, L3]
aws_exam_relevance: DevOps Professional
---

# AWS CodeBuild - Best Practices

- **Use Caching**: Implement local or S3 caching for dependencies like `node_modules` or `.m2` to reduce build times.
- **Docker Layer Caching**: Use the `--cache-from` flag in `docker build` using a previously pushed image.
- **VPC Endpoints**: When running in a private VPC subnet, use VPC endpoints for S3, ECR, and Secrets Manager to avoid NAT Gateway data transfer costs.
