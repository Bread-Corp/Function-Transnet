# 🚂 Transnet Tender Processing Lambda Service

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Amazon SQS](https://img.shields.io/badge/AWS-SQS-yellow.svg)](https://aws.amazon.com/sqs/)
[![Transnet API](https://img.shields.io/badge/API-Transnet-blue.svg)](https://www.transnet.net/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-red.svg)](https://pydantic.dev/)

**Moving South Africa's economy forward, one tender at a time!** 🚛 This AWS Lambda service is the logistics backbone of our tender scraping fleet - one of five specialized crawlers that captures opportunities from Africa's largest freight rail, port, and pipeline company. From massive infrastructure projects to specialized equipment procurement, we track every cargo container of opportunity! 📦

## 📚 Table of Contents

- [🎯 Overview](#-overview)
- [🚂 Lambda Function (lambda_function.py)](#-lambda-function-lambda_functionpy)
- [📊 Data Model (models.py)](#-data-model-modelspy)
- [🏷️ AI Tagging Initialization](#️-ai-tagging-initialization)
- [📋 Example Tender Data](#-example-tender-data)
- [🚀 Getting Started](#-getting-started)
- [📦 Deployment](#-deployment)
- [🧰 Troubleshooting](#-troubleshooting)

## 🎯 Overview

All aboard the opportunity express! 🚆 This service is your direct connection to Transnet's vast logistics ecosystem, capturing multi-billion rand infrastructure projects, rail network expansions, port developments, and critical transportation services that keep South Africa's economy moving! 🌍

**What makes it move mountains?** 🏔️
- 🚛 **Logistics Sector Mastery**: Specialized in freight rail, ports, pipelines, and transportation infrastructure
- 🏗️ **Infrastructure Scale**: From rail sidings to port terminals, pipeline networks to cargo facilities
- 🛡️ **Industrial-Strength Processing**: Built to handle Transnet's complex multi-modal tender structures
- 🌐 **Multi-Location Coverage**: Captures opportunities across South Africa's entire logistics network

## 🚂 Lambda Function (`lambda_function.py`)

The locomotive that powers our data collection! 🚂 The `lambda_handler` orchestrates the entire cargo extraction process with precision engineering:

### 🔄 The Freight Forwarding Journey:

1. **🌐 Fetch Cargo**: Connects to the Transnet eTenders API - the central dispatch for all transportation and logistics procurement across the country.

2. **🛡️ Rock-Solid Error Handling**: Built like a freight locomotive! Handles network delays, API maintenance windows, and response irregularities with industrial-grade resilience. Always on track! 🛤️

3. **📦 Cargo Processing**: The Transnet API wraps its tender treasure in a `result` key - we expertly unload this cargo and sort through every opportunity.

4. **⚙️ Precision Engineering**: Each tender goes through our specialized `TransnetTender` model with custom logic for Transnet's unique date formats (`MM/DD/YYYY HH:MI:SS AM/PM`) and attachment URL extraction.

5. **✅ Quality Control**: Our validation engine ensures only premium-grade tenders make it through. Invalid cargo gets flagged, logged, and rerouted - no derailments in our pipeline! 🚨

6. **📦 Smart Containerization**: Valid tenders are efficiently packed into batches of 10 messages - optimized for maximum SQS throughput like a well-organized freight yard.

7. **🚀 Express Delivery**: Each batch speeds to the central `AIQueue.fifo` SQS queue with the unique `MessageGroupId` of `TransnetTenderScrape`. This keeps our logistics tenders organized and maintains perfect delivery order.

## 📊 Data Model (`models.py`)

Our data architecture is engineered for seamless transportation! 🏗️

### `TenderBase` **(The Universal Chassis)** 🚛
The robust platform that carries all our tender models! This abstract class defines the core framework that connects all transportation opportunities:

**🔧 Core Attributes:**
- `title`: The tender's cargo manifest - what's being transported?
- `description`: Detailed specifications and logistics requirements
- `source`: Always "Transnet" for this logistics powerhouse
- `published_date`: When this opportunity left the depot
- `closing_date`: Final delivery deadline - when the cargo door closes! ⏰
- `supporting_docs`: Critical technical specifications and route maps
- `tags`: Keywords for AI logistics (starts empty, gets loaded by our AI service)

### `TransnetTender` **(The Freight Specialist)** 🚂
This powerhouse inherits all the foundational strength from `TenderBase` and adds Transnet's unique multi-modal logistics features:

**🏭 Transnet-Specific Attributes:**
- `tender_number`: Official Transnet tracking code (e.g., "TFR/2025/10/0019/108317/RFP")
- `institution`: Which Transnet division? (e.g., "TFR" - Transnet Freight Rail)
- `category`: Type of cargo/service (e.g., "Services", "Infrastructure", "Equipment")
- `tender_type`: Procurement method (e.g., "RFP", "RFQ", "EOI")
- `location`: Which province needs the logistics boost (e.g., "Limpopo", "KwaZulu-Natal")
- `email`: Direct line to Transnet's procurement hub
- `contact_person`: Your dedicated logistics coordinator

## 🏷️ AI Tagging Initialization

We're all about intelligent cargo routing! 🤖 Every tender that moves through our system is perfectly prepared for downstream AI enhancement:

```python
# From models.py - Preparing for AI cargo classification! 🚛
return cls(
    # ... other fields
    tags=[],  # Initialize tags as an empty list, ready for the AI service.
    # ... other fields
)
```

This ensures **seamless logistics integration** with our AI pipeline - every tender object arrives with a clean, empty `tags` field just waiting to be loaded with intelligent categorizations! 🧠📦

## 📋 Example Tender Data

Here's what a real Transnet logistics opportunity looks like after our scraper works its magic! 🎩✨

```json
{
  "title": "Trimrfp3Nc Mica",
  "description": "For Leasing Of The Transnet Rail Infrastructure Manager Sidings/Facilities, Siding Number 800805 (Mica) For A Minimum Period Of Ten (10) Years",
  "source": "Transnet",
  "publishedDate": "2025-10-07T19:53:26",
  "closingDate": "2025-11-18T12:00:00",
  "supporting_docs": [
    {
      "name": "Tender Attachment",
      "url": "https://publishedetenders.blob.core.windows.net/publishedetenderscontainer/108317"
    }
  ],
  "tags": [],
  "tenderNumber": "TFR/2025/10/0019/108317/RFP",
  "institution": "TFR",
  "category": "Services",
  "tenderType": "RFP",
  "location": "Limpopo",
  "email": "lolo.sokhela@transnet.net",
  "contactPerson": "Lolo Sokhela          Transnet Freight Rail   Jhb"
}
```

**🚂 What this opportunity delivers:**
- 🏗️ **Infrastructure Leasing**: Long-term rail siding facilities lease (10+ years)
- 🚛 **Strategic Location**: Mica siding in Limpopo - critical mining region connection
- 📋 **TFR Division**: Transnet Freight Rail - the backbone of South African logistics
- 💰 **Long-term Revenue**: Decade-long contract opportunity
- 🌍 **Economic Impact**: Supporting mining and industrial transport in Limpopo
- ⏰ **Current Opportunity**: Live tender with November 2025 deadline

## 🚀 Getting Started

Ready to hop aboard Transnet's logistics express? Let's get your freight moving! 🚛

### 📋 Prerequisites
- AWS CLI configured with appropriate credentials 🔑
- Python 3.9+ with pip 🐍
- Access to AWS Lambda and SQS services ☁️
- Understanding of transportation and logistics terminology 🚛

### 🔧 Local Development
1. **📁 Clone the repository**
2. **📦 Install dependencies**: `pip install -r requirements.txt`
3. **🧪 Run tests**: `python -m pytest`
4. **🔍 Test locally**: Use AWS SAM for local Lambda simulation

## 📦 Deployment

This section covers three deployment methods for the Transnet Tender Processing Lambda Service. Choose the method that best fits your workflow and infrastructure preferences.

### 🛠️ Prerequisites

Before deploying, ensure you have:
- AWS CLI configured with appropriate credentials 🔑
- AWS SAM CLI installed (`pip install aws-sam-cli`)
- Python 3.13 runtime support in your target region
- Access to AWS Lambda, SQS, and CloudWatch Logs services ☁️
- Required Python dependency: `requests`

### 🎯 Method 1: AWS Toolkit Deployment

Deploy directly through your IDE using the AWS Toolkit extension.

#### Setup Steps:
1. **Install AWS Toolkit** in your IDE (VS Code, IntelliJ, etc.)
2. **Configure AWS Profile** with your credentials
3. **Open Project** containing `lambda_function.py` and `models.py`

#### Deploy Process:
1. **Right-click** on `lambda_function.py` in your IDE
2. **Select** "Deploy Lambda Function" from AWS Toolkit menu
3. **Configure Deployment**:
   - Function Name: `TransnetLambda`
   - Runtime: `python3.13`
   - Handler: `lambda_function.lambda_handler`
   - Memory: `128 MB`
   - Timeout: `120 seconds`
4. **Add Layers** manually after deployment:
   - requests-library layer
5. **Set Environment Variables**:
   ```
   SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo
   API_TIMEOUT=30
   BATCH_SIZE=10
   ```
6. **Configure IAM Permissions** for SQS, CloudWatch Logs, and EC2 (for VPC if needed)

#### Post-Deployment:
- Test the function using the AWS Toolkit test feature
- Monitor logs through CloudWatch integration
- Update function code directly from IDE for quick iterations

### 🚀 Method 2: SAM Deployment

Use AWS SAM for infrastructure-as-code deployment with the provided template.

#### Initial Setup:
```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Verify installation
sam --version
```

#### Create Required Layer Directory:
Since the template references a layer not included in the repository, create it:

```bash
# Create layer directory
mkdir -p requests-library/python

# Install requests layer
pip install requests -t requests-library/python/
```

#### Build and Deploy:
```bash
# Build the SAM application
sam build

# Deploy with guided configuration (first time)
sam deploy --guided

# Follow the prompts:
# Stack Name: transnet-lambda-stack
# AWS Region: us-east-1 (or your preferred region)
# Parameter SQSQueueURL: https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo
# Parameter APITimeout: 30
# Parameter BatchSize: 10
# Confirm changes before deploy: Y
# Allow SAM to create IAM roles: Y
# Save parameters to samconfig.toml: Y
```

#### Environment Variables Setup:
Add these parameters to your SAM template or set them after deployment:

```yaml
# Add to template.yml under TransnetLambda Properties
Environment:
  Variables:
    SQS_QUEUE_URL: https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo
    API_TIMEOUT: "30"
    BATCH_SIZE: "10"
```

#### Subsequent Deployments:
```bash
# Quick deployment after initial setup
sam build && sam deploy
```

#### Local Testing with SAM:
```bash
# Test function locally with environment variables
sam local invoke TransnetLambda --env-vars env.json

# Create env.json file:
echo '{
  "TransnetLambda": {
    "SQS_QUEUE_URL": "https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo",
    "API_TIMEOUT": "30",
    "BATCH_SIZE": "10"
  }
}' > env.json
```

#### SAM Deployment Advantages:
- ✅ Complete infrastructure management
- ✅ Automatic layer creation and management
- ✅ IAM permissions defined in template
- ✅ Easy rollback capabilities
- ✅ CloudFormation integration

### 🔄 Method 3: Workflow Deployment (CI/CD)

Automated deployment using GitHub Actions workflow for production environments.

#### Setup Requirements:
1. **GitHub Repository Secrets**:
   ```
   AWS_ACCESS_KEY_ID: Your AWS access key
   AWS_SECRET_ACCESS_KEY: Your AWS secret key
   AWS_REGION: us-east-1 (or your target region)
   ```

2. **Pre-existing Lambda Function**: The workflow updates an existing function, so deploy initially using Method 1 or 2.

#### Deployment Process:
1. **Create Release Branch**:
   ```bash
   # Create and switch to release branch
   git checkout -b release
   
   # Make your changes to lambda_function.py or models.py
   # Commit changes
   git add .
   git commit -m "feat: update Transnet logistics processing logic"
   
   # Push to trigger deployment
   git push origin release
   ```

2. **Automatic Deployment**: The workflow will:
   - Checkout the code
   - Configure AWS credentials
   - Create deployment zip with `lambda_function.py` and `models.py`
   - Update the existing Lambda function code
   - Maintain existing configuration (layers, environment variables, etc.)

#### Manual Trigger:
You can also trigger deployment manually:
1. Go to **Actions** tab in your GitHub repository
2. Select **"Deploy Python Scraper to AWS"** workflow
3. Click **"Run workflow"**
4. Choose the `release` branch
5. Click **"Run workflow"** button

#### Workflow Deployment Advantages:
- ✅ Automated CI/CD pipeline
- ✅ Consistent deployment process
- ✅ Audit trail of deployments
- ✅ Easy rollback to previous commits
- ✅ No local environment dependencies

### 🔧 Post-Deployment Configuration

Regardless of deployment method, configure the following:

#### Environment Variables:
Set these environment variables in your Lambda function:

```bash
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo
API_TIMEOUT=30
BATCH_SIZE=10
USER_AGENT=Mozilla/5.0 (compatible; Transnet-Logistics-Bot/1.0)
```

#### Via AWS CLI:
```bash
aws lambda update-function-configuration \
    --function-name TransnetLambda \
    --environment Variables='{
        "SQS_QUEUE_URL":"https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo",
        "API_TIMEOUT":"30",
        "BATCH_SIZE":"10",
        "USER_AGENT":"Mozilla/5.0 (compatible; Transnet-Logistics-Bot/1.0)"
    }'
```

#### CloudWatch Events (Optional):
Set up scheduled execution:
```bash
# Create CloudWatch Events rule for daily execution
aws events put-rule \
    --name "TransnetLambdaSchedule" \
    --schedule-expression "cron(0 9 * * ? *)" \
    --description "Daily Transnet logistics tender scraping"

# Add Lambda as target
aws events put-targets \
    --rule "TransnetLambdaSchedule" \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:211635102441:function:TransnetLambda"
```

### 🧪 Testing Your Deployment

After deployment, test the function:

```bash
# Test via AWS CLI
aws lambda invoke \
    --function-name TransnetLambda \
    --payload '{}' \
    response.json

# Check the response
cat response.json
```

#### Expected Success Indicators:
- ✅ Function executes without errors
- ✅ CloudWatch logs show successful API calls to Transnet eTenders
- ✅ SQS queue receives tender messages with proper logistics data
- ✅ No timeout or memory errors
- ✅ Valid JSON tender data in queue messages
- ✅ MessageGroupId set to "TransnetTenderScrape"
- ✅ Proper date parsing for Transnet's MM/DD/YYYY format

### 🔍 Monitoring and Maintenance

#### CloudWatch Metrics to Monitor:
- **Duration**: Function execution time (watch for large infrastructure project processing)
- **Error Rate**: Failed invocations
- **Memory Utilization**: RAM usage patterns during batch processing
- **Throttles**: Concurrent execution limits

#### Log Analysis:
```bash
# View recent logs
aws logs tail /aws/lambda/TransnetLambda --follow

# Search for errors
aws logs filter-log-events \
    --log-group-name /aws/lambda/TransnetLambda \
    --filter-pattern "ERROR"

# Search for successful batch deliveries
aws logs filter-log-events \
    --log-group-name /aws/lambda/TransnetLambda \
    --filter-pattern "Successfully sent batch"

# Monitor Transnet-specific patterns
aws logs filter-log-events \
    --log-group-name /aws/lambda/TransnetLambda \
    --filter-pattern "TransnetTenderScrape"
```

### 🚨 Troubleshooting Deployments

<details>
<summary><strong>Layer Dependencies Missing</strong></summary>

**Issue**: `requests` import errors

**Solution**: Ensure the requests layer is properly created and attached:
```bash
# For SAM: Verify layer directory exists and contains packages
ls -la requests-library/python/

# Check for requests module
ls -la requests-library/python/requests/

# For manual deployment: Create and upload layer separately
```
</details>

<details>
<summary><strong>Environment Variables Not Set</strong></summary>

**Issue**: Missing SQS_QUEUE_URL, API_TIMEOUT, or BATCH_SIZE configuration

**Solution**: Set environment variables using AWS CLI or console:
```bash
aws lambda update-function-configuration \
    --function-name TransnetLambda \
    --environment Variables='{
        "SQS_QUEUE_URL":"https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo",
        "API_TIMEOUT":"30",
        "BATCH_SIZE":"10"
    }'
```
</details>

<details>
<summary><strong>IAM Permission Errors</strong></summary>

**Issue**: Access denied for SQS or CloudWatch operations

**Solution**: Verify the Lambda execution role has required permissions:
- `sqs:SendMessage`
- `sqs:GetQueueUrl` 
- `sqs:GetQueueAttributes`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`
- `ec2:CreateNetworkInterface`
- `ec2:DeleteNetworkInterface`
- `ec2:DescribeNetworkInterfaces`
</details>

<details>
<summary><strong>Workflow Deployment Fails</strong></summary>

**Issue**: GitHub Actions workflow errors

**Solution**: Check repository secrets are correctly configured and the target Lambda function exists in AWS. Verify the function ARN matches the workflow configuration.
</details>

<details>
<summary><strong>Transnet API Connection Issues</strong></summary>

**Issue**: Cannot connect to Transnet eTenders API

**Solution**: 
- Verify the API endpoint is accessible
- Check if Transnet's systems are experiencing maintenance
- Consider increasing the API_TIMEOUT environment variable
- Monitor for peak hour traffic delays
</details>

<details>
<summary><strong>Date Parsing Failures</strong></summary>

**Issue**: Transnet's MM/DD/YYYY date format causing validation errors

**Solution**: Ensure your date parsing logic properly handles Transnet's specific date format:
```python
# Example date handling for Transnet format
from datetime import datetime
date_str = "10/07/2025 07:53:26 PM"
parsed_date = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
```
</details>

Choose the deployment method that best fits your development workflow and infrastructure requirements. SAM deployment is recommended for development environments, while workflow deployment excels for production CI/CD pipelines handling large-scale logistics data.

## 🧰 Troubleshooting

### 🚨 Logistics Challenges

<details>
<summary><strong>API Connection Delays</strong></summary>

**Issue**: Cannot connect to Transnet eTenders API during peak hours.

**Solution**: Transnet's systems can experience heavy traffic during business hours. Implement intelligent retry logic with exponential backoff. Even freight trains need to wait for signals! 🚦

</details>

<details>
<summary><strong>Date Format Processing</strong></summary>

**Issue**: Transnet's unique date format causing parsing failures.

**Solution**: Transnet uses `MM/DD/YYYY HH:MI:SS AM/PM` format. Ensure your date parsing logic handles this specific format with proper timezone considerations! 📅

</details>

<details>
<summary><strong>Large Infrastructure Projects</strong></summary>

**Issue**: Lambda timeouts on massive rail and port development tenders.

**Solution**: Transnet deals in continental-scale infrastructure! Increase Lambda timeout and memory allocation. Some rail network expansions have extensive documentation! 🏗️

</details>

<details>
<summary><strong>Multi-Modal Data Complexity</strong></summary>

**Issue**: Complex tenders spanning rail, ports, and pipelines failing validation.

**Solution**: Transnet operates across multiple transport modes. Update validation rules to handle diverse logistics terminology, from rail gauge specifications to port container capacities! ⚙️

</details>

<details>
<summary><strong>Attachment URL Processing</strong></summary>

**Issue**: Transnet's Azure blob storage URLs not processing correctly.

**Solution**: Ensure your URL extraction logic properly handles Transnet's cloud storage paths and maintains document accessibility! 🔗

</details>

---

> Built with love, bread, and code by **Bread Corporation** 🦆❤️💻
