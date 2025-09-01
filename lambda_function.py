# ==================================================================================================
#
# File: TransnetLambda/lambda_function.py
#
# Description:
# This script contains an AWS Lambda function designed to fetch tender data from the Transnet
# eTenders portal API. It processes the raw data, transforms it into a structured format
# using the TransnetTender model, and then sends it to an Amazon SQS queue for further processing.
#
# The function performs the following steps:
# 1. Fetches tender data from the Transnet API endpoint.
# 2. Handles potential network errors or invalid API responses.
# 3. Extracts the list of tenders from the nested 'result' key in the API response.
# 4. Iterates through each tender item.
# 5. Validates and parses each item into a structured TransnetTender object.
# 6. Skips and logs any items that fail validation.
# 7. Converts the processed tender objects into dictionaries.
# 8. Batches the tender data into groups of 10.
# 9. Sends each batch to a specified SQS FIFO queue with a unique MessageGroupId.
# 10. Logs the outcome of the operation.
#
# ==================================================================================================

# --- Import necessary libraries ---
import json
import requests
import logging
import boto3
from models import TransnetTender # Import the data model for Transnet tenders.

# --- Global Constants and Configuration ---
# The URL of the Transnet eTenders API.
TRANSNET_API_URL = "https://transnetetenders.azurewebsites.net/Home/GetAdvertisedTenders"

# HTTP headers to mimic a web browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
}

# --- Logger Setup ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- AWS Service Client Initialization ---
sqs_client = boto3.client('sqs')
# The URL of the target SQS FIFO queue. This is the same queue used by other lambdas.
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/211635102441/AIQueue.fifo'

# ==================================================================================================
# Lambda Function Handler
# ==================================================================================================
def lambda_handler(event, context):
    """
    The main handler function for the AWS Lambda.
    """
    logger.info("Starting Transnet tenders processing job.")

    # --- Step 1: Fetch Data from the Transnet API ---
    try:
        logger.info(f"Fetching data from {TRANSNET_API_URL}")
        # Make a GET request to the API with a 30-second timeout.
        response = requests.get(TRANSNET_API_URL, headers=HEADERS, timeout=30)
        # Raise an exception for bad status codes (4xx or 5xx).
        response.raise_for_status()
        api_response_dict = response.json()
        
        # The Transnet API response is a dictionary where the actual list of tenders
        # is stored under the 'result' key. We safely get this list, defaulting to an
        # empty list if the key is not found.
        api_data = api_response_dict.get('result', [])
        logger.info(f"Successfully fetched {len(api_data)} tender items from the API.")
        
    except requests.exceptions.RequestException as e:
        # Handle network-related errors.
        logger.error(f"Failed to fetch data from API: {e}")
        return {'statusCode': 502, 'body': json.dumps({'error': 'Failed to fetch data from source API'})}
    except json.JSONDecodeError:
        # Handle cases where the response is not valid JSON.
        logger.error(f"Failed to decode JSON from API response. Response text: {response.text}")
        return {'statusCode': 502, 'body': json.dumps({'error': 'Invalid JSON response from source API'})}

    # --- Step 2: Process and Validate Each Tender Item ---
    processed_tenders = []
    skipped_count = 0

    for item in api_data:
        try:
            # Pass the tender dictionary directly to the model's factory method for processing.
            tender_object = TransnetTender.from_api_response(item)
            
            # The from_api_response method returns None if the item is invalid (e.g., no ID).
            if tender_object:
                processed_tenders.append(tender_object)
            else:
                # If the object is None, it means it was intentionally skipped by the model.
                skipped_count += 1

        except (KeyError, ValueError, TypeError) as e:
            # Catch any other unexpected errors during parsing.
            skipped_count += 1
            tender_id = item.get('rowKey', 'Unknown')
            logger.warning(f"Skipping tender {tender_id} due to a validation/parsing error: {e}.")
            continue

    logger.info(f"Successfully processed {len(processed_tenders)} tenders.")
    if skipped_count > 0:
        logger.warning(f"Skipped a total of {skipped_count} tenders due to errors.")

    # --- Step 3: Prepare Data for SQS ---
    # Convert the list of TransnetTender objects into a list of dictionaries.
    processed_tender_dicts = [tender.to_dict() for tender in processed_tenders]

    # --- Step 4: Batch and Send Messages to SQS ---
    batch_size = 10
    # Split the list of tenders into smaller batches.
    message_batches = [
        processed_tender_dicts[i:i + batch_size]
        for i in range(0, len(processed_tender_dicts), batch_size)
    ]

    sent_count = 0
    for batch_index, batch in enumerate(message_batches):
        entries = []
        for i, tender_dict in enumerate(batch):
            entries.append({
                'Id': f'tender_message_{batch_index}_{i}',
                'MessageBody': json.dumps(tender_dict),
                # Use a specific MessageGroupId for Transnet to maintain order for this source.
                'MessageGroupId': 'TransnetTenderScrape'
            })

        # Skip sending if the batch is empty for any reason.
        if not entries:
            continue

        try:
            # Send the batch of messages to the SQS queue.
            response = sqs_client.send_message_batch(
                QueueUrl=SQS_QUEUE_URL,
                Entries=entries
            )
            sent_count += len(response.get('Successful', []))
            logger.info(f"Successfully sent a batch of {len(entries)} messages to SQS.")
            # Log if any messages within the batch failed.
            if 'Failed' in response and response['Failed']:
                logger.error(f"Failed to send some messages in a batch: {response['Failed']}")
        except Exception as e:
            logger.error(f"Failed to send a message batch to SQS: {e}")

    logger.info(f"Processing complete. Sent a total of {sent_count} messages to SQS.")

    # --- Step 5: Return a Success Response ---
    return {
        'statusCode': 200,
        'body': {'message': 'Tender data processed and sent to SQS queue.'}
    }