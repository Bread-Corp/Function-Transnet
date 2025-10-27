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

### 🚀 Express Delivery Deploy
1. **📁 Package**: Containerize your code and dependencies
2. **⬆️ Upload**: Deploy to AWS Lambda with freight-grade settings
3. **⚙️ Configure**: Set up CloudWatch Events for scheduled cargo runs
4. **🎯 Test**: Trigger manually to verify logistics connection

### 🔧 Environment Variables
- `SQS_QUEUE_URL`: Target queue for processed logistics tenders
- `API_TIMEOUT`: Request timeout for Transnet API calls
- `BATCH_SIZE`: Number of tenders per SQS shipment (default: 10)

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
