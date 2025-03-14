# Cosmos: A Cost Model for Serverless Workflows in the 3D Compute Continuum

## Overview
Cosmos is a cost model designed to analyze and optimize serverless workflow costs across the Edge-Cloud-Space 3D Compute Continuum. It classifies key cost drivers such as invocation, compute, data transfer, state management, and Backend-as-a-Service (BaaS) to provide a fine-grained breakdown of expenses. The model enables developers to better understand cost-performance trade-offs when deploying serverless functions in heterogeneous environments.

## Features
- **Cost Classification**: Breakdown of serverless workflow costs into fixed and dynamic categories.
- **Compute Layer Differentiation**: Supports cost analysis across edge, cloud, and space computing layers.
- **Workload-Specific Insights**: Identifies how workload characteristics (data-intensive, compute-intensive, AI-driven) influence cost.
- **Provider Cost Comparison**: Evaluates costs across leading cloud platforms (AWS, GCP) based on function execution and BaaS service consumption.
- **Performance vs. Cost Trade-offs**: Integrates Service Level Objectives (SLOs) and budget constraints for optimized function placement.

## Repository Contents
This repository contains the implementation of Cosmos, including:

- **Data Retrieval**: Implemented using AWS Lambda with API Gateway for HTTP endpoint management, DynamoDB for structured data storage, and Amazon S3 for object storage. In GCP, Cloud Functions are used along with Firestore for document storage and Cloud Storage for object retrieval.
- **Data Processing**: AWS uses Lambda for compute tasks, API Gateway for request handling, and AWS Glue for ETL processing, while GCP utilizes Cloud Functions and Dataflow for similar ETL operations.
- **AI Inference**: AWS incorporates Lambda for preprocessing, API Gateway for exposure, and SageMaker Serverless Inference for model execution. GCP employs Cloud Functions with Vertex AI for inference management.

## Results Summary
Key findings from the experiments:
- **Data-intensive workloads**: GCP is up to **77% cheaper** than AWS due to lower storage and retrieval costs.
- **Compute-intensive workloads**: AWS has **36% lower latency** and reduced execution costs.
- **AI-related workloads**: AWS is **77% cheaper** at lower workloads, while GCP becomes **73% more cost-efficient** beyond the break-even point of ~23M requests.
- **Data transfer costs**: Account for **75% of AWS** and **52% of GCP** costs in data-intensive workloads.
- **BaaS costs**: Dominant in compute-heavy workloads, reaching **83% in AWS** and **97% in GCP**.

## Future Work
- **Dynamic Cost Prediction**: Implementing cost estimation for various workload types.
- **Adaptive Workload Placement**: Automated decision-making framework to optimize cost and performance trade-offs.
- **Edge and Space Integration**: Expanding experiments to include real-world edge and satellite-based processing.

