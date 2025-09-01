# Transnet Tender Processing Lambda Service
## 1. Overview
This service contains an AWS Lambda function responsible for scraping tender information from the Transnet eTenders portal API. Its primary function is to fetch raw tender data, process and validate it against a defined data model, and then dispatch it as messages to an Amazon SQS (Simple Queue Service) queue for further downstream processing.

This service acts as another entry point into the data pipeline, allowing the system to ingest tenders from Transnet alongside other sources like Eskom and the National Treasury.

## 2. Lambda Function (`lambda_function.py`)    
The lambda_handler is the main entry point for the service. It executes the following logic:
1. **Fetch Data**: It sends an HTTP GET request to the Transnet eTenders API.
2. **Error Handling**: It includes robust error handling for network issues and invalid API responses.
3. **Data Extraction**: The Transnet API response is a dictionary with a `result` key that holds the list of tenders. The function safely extracts this list.
4. **Data Parsing**: It iterates through the list of tenders. Each tender is passed to the `TransnetTender` model for parsing. This includes logic for handling a specific date format (`MM/DD/YYYY HH:MI:SS AM/PM`) and extracting attachment URLs.
5. **Validation & Logging**: If a tender is invalid (e.g., missing its unique ID), the model returns `None`, and the tender is skipped. Other parsing errors are caught and logged in CloudWatch.
6. **Batching**: The successfully processed tenders are grouped into batches of 10 to comply with SQS API limits.
7. **Queueing**: Each batch of tender data is sent to the central `AIQueue.fifo` SQS queue. A `MessageGroupId` of `TransnetTenderScrape` is used to ensure all tenders from this source are processed in order.

## 3. Data Model (`models.py`)
The service uses a set of Python classes to define the structure of the tender data, ensuring consistency with the other data sources.

`TenderBase` **(Abstract Class)**   
This is a foundational class that defines the common attributes for any tender, regardless of its source.
- **Core Attributes**:
    - `title`: The title of the tender.
    - `description`: A detailed description.
    - `source`: The origin of the tender (hardcoded to `"Transnet"`).
    - `published_date`: The date the tender was published.
    - `closing_date`: The submission deadline.
    - `supporting_docs`: A list of `SupportingDoc` objects.
    - `tags`: A list of keywords or categories.

`TransnetTender` **(Concrete Class)**   
This class inherits from `TenderBase` and adds fields that are specific to the data provided by the Transnet API.
- **Inherited Attributes**: All attributes from TenderBase.
- **Transnet-Specific Attributes**:
    - `tender_number`: The unique tender number.
    - `institution`: The name of the institution issuing the tender.
    - `category`: The category of the tender.
    - `tender_type`: The type of procurement.
    - `location`: The location where the service is required.
    - `email`: Contact email address.
    - `contact_person`: The name of the contact person for inquiries.

## AI Tagging Initialization
A crucial design choice in the `TransnetTender` model is the handling of the `tags` attribute. In the `from_api_response` method, the `tags` field is **always initialized to an empty list (`[]`)**.

```
# From models.py
return cls(
    # ... other fields
    tags=[],  # Initialize with an empty list for the AI service.
    # ... other fields
)
```

This is done intentionally because the Transnet API does not provide any tags or categories. The responsibility of generating relevant tags is delegated to a downstream AI service that will consume the messages from the SQS queue. By initializing `tags` as an empty list, we provide a consistent and predictable data structure for the AI service to populate.