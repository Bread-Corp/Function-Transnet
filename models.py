# ==================================================================================================
#
# File: TransnetLambda/models.py
#
# Description:
# This module defines the data structures (models) for representing tender information
# sourced specifically from the Transnet eTenders portal. It provides a structured way
# to handle, validate, and serialize this specific type of tender data.
#
# The classes defined here are:
#   - SupportingDoc: A simple class to represent a downloadable document linked to a tender.
#   - TenderBase: An abstract base class defining the common interface and core attributes
#     for any tender. This promotes consistency across different tender types.
#   - TransnetTender: A concrete class that inherits from TenderBase and adds fields
#     specific to the data provided by the Transnet API. It includes logic for parsing
#     the raw API response into a clean, usable object.
#
# ==================================================================================================

# Import necessary built-in modules.
# abc (Abstract Base Classes) is used to define the basic structure of a tender.
# datetime is used for handling and formatting date/time information.
# logging is used to record warnings or errors during data parsing.
from abc import ABC, abstractmethod
from datetime import datetime
import logging

# ==================================================================================================
# Class: SupportingDoc
# Purpose: Represents a single supporting document associated with a tender.
# ==================================================================================================
class SupportingDoc:
    """
    A simple data class to hold information about a supporting document.
    """
    def __init__(self, name: str, url: str):
        """
        Initializes a new instance of the SupportingDoc class.

        Args:
            name (str): The human-readable name of the document.
            url (str): The direct URL where the document can be downloaded.
        """
        # --- Instance Attributes ---
        self.name = name
        self.url = url

    def to_dict(self):
        """
        Serializes the SupportingDoc instance into a dictionary format.

        Returns:
            dict: A dictionary containing the document's name and URL.
        """
        return {"name": self.name, "url": self.url}

# ==================================================================================================
# Class: TenderBase (Abstract Base Class)
# Purpose: Defines the fundamental structure and contract for all tender types.
# ==================================================================================================
class TenderBase(ABC):
    """
    An abstract base class that serves as a template for all specific tender models.
    """
    def __init__(self, title: str, description: str, source: str, published_date: datetime, closing_date: datetime, supporting_docs: list = None, tags: list = None):
        """
        Initializes the base attributes of a tender.

        Args:
            title (str): The official title of the tender.
            description (str): A detailed description of the tender's scope.
            source (str): The name of the platform where the tender was found.
            published_date (datetime): The date and time the tender was published.
            closing_date (datetime): The submission deadline for the tender.
            supporting_docs (list, optional): A list of SupportingDoc objects. Defaults to an empty list.
            tags (list, optional): A list of keywords. Defaults to an empty list for later AI processing.
        """
        # --- Instance Attributes ---
        self.title = title
        self.description = description
        self.source = source
        self.published_date = published_date
        self.closing_date = closing_date
        self.supporting_docs = supporting_docs if supporting_docs is not None else []
        # Initialize tags as an empty list, as they will be added by a separate AI service.
        self.tags = tags if tags is not None else []

    @classmethod
    @abstractmethod
    def from_api_response(cls, response_item: dict):
        """
        An abstract factory method that must be implemented by all subclasses.
        Its purpose is to create a tender object from a raw API response item.
        """
        pass

    def to_dict(self):
        """
        Serializes the common tender attributes into a dictionary.
        """
        return {
            "title": self.title,
            "description": self.description,
            "source": self.source,
            # Convert datetime objects to ISO 8601 format string for JSON compatibility.
            "publishedDate": self.published_date.isoformat() if self.published_date else None,
            "closingDate": self.closing_date.isoformat() if self.closing_date else None,
            "supporting_docs": [doc.to_dict() for doc in self.supporting_docs],
            # In the base model, this assumes tags are objects with a to_dict method.
            # For this project, tags are simple strings, so this will be overridden or adjusted.
            "tags": [tag.to_dict() for tag in self.tags]
        }

# ==================================================================================================
# Class: TransnetTender
# Purpose: A concrete implementation of TenderBase for Transnet-specific tenders.
# ==================================================================================================
class TransnetTender(TenderBase):
    """
    Represents a tender sourced from Transnet. It adds fields unique to the Transnet API.
    """
    def __init__(
        self,
        # --- Base fields required by TenderBase ---
        title: str, description: str, source: str, published_date: datetime, closing_date: datetime, supporting_docs: list, tags: list,
        # --- Child fields specific to TransnetTender ---
        tender_number: str,
        institution: str,
        category: str,
        tender_type: str,
        location: str,
        email: str,
        contact_person: str,
    ):
        """
        Initializes a new TransnetTender instance.
        """
        # Call the parent class's __init__ method to set up the common fields.
        super().__init__(title, description, source, published_date, closing_date, supporting_docs, tags)
        # --- Transnet-specific Instance Attributes ---
        self.tender_number = tender_number
        self.institution = institution
        self.category = category
        self.tender_type = tender_type
        self.location = location
        self.email = email
        self.contact_person = contact_person

    @classmethod
    def from_api_response(cls, response_item: dict):
        """
        Factory method to create a TransnetTender object from a raw API response.
        This method handles data extraction, cleaning, and validation.

        Args:
            response_item (dict): A dictionary containing a single tender's data from the Transnet API.

        Returns:
            TransnetTender or None: An instance of the class, or None if validation fails.
        """
        # The unique identifier for the tender in the Transnet system.
        tender_id = response_item.get('rowKey')
        # If there is no ID, the item is invalid, so we return None to skip it.
        if not tender_id:
            return None

        # --- Document Handling ---
        doc_list = []
        attachment_url = response_item.get('attachment')
        if attachment_url:
            # If an attachment URL exists, create a SupportingDoc object for it.
            doc_list.append(SupportingDoc(name="Tender Attachment", url=attachment_url))

        # --- Date Parsing ---
        # The Transnet API uses a specific date format (Month/Day/Year Hour:Minute:Second AM/PM).
        date_format = '%m/%d/%Y %I:%M:%S %p'
        pub_date, close_date = None, None
        try:
            pub_date_str = response_item.get('publishedDate')
            if pub_date_str:
                # Convert the string to a datetime object using the specified format.
                pub_date = datetime.strptime(pub_date_str, date_format)
        except (TypeError, ValueError):
            # Log a warning if the date is missing or in an incorrect format.
            logging.warning(f"Tender {tender_id} has invalid publishedDate: {response_item.get('publishedDate')}")
        try:
            close_date_str = response_item.get('closingDate')
            if close_date_str:
                close_date = datetime.strptime(close_date_str, date_format)
        except (TypeError, ValueError):
            logging.warning(f"Tender {tender_id} has invalid closingDate: {response_item.get('closingDate')}")

        # --- Object Creation and Data Cleaning ---
        # Create and return an instance of the class, cleaning up string fields.
        # .strip() removes leading/trailing whitespace.
        # .title(), .upper(), .lower() standardize the case of the text.
        return cls(
            title=response_item.get('nameOfTender', '').replace('\n', ' ').replace('\r', '').strip().title(),
            description=response_item.get('descriptionOfTender', '').replace('\n', ' ').replace('\r', '').strip().title(),
            source="Transnet", # Hardcoded source.
            published_date=pub_date,
            closing_date=close_date,
            supporting_docs=doc_list,
            tags=[], # Initialize with an empty list for the AI service.
            tender_number=response_item.get('tenderNumber', '').replace('\n', ' ').replace('\r', '').strip().upper(),
            institution=response_item.get('nameOfInstitution', '').replace('\n', ' ').replace('\r', '').strip().upper(),
            category=response_item.get('tenderCategory', '').replace('\n', ' ').replace('\r', '').strip().title(),
            tender_type=response_item.get('tenderType', '').replace('\n', ' ').replace('\r', '').strip().upper(),
            location=response_item.get('locationOfService', '').replace('\n', ' ').replace('\r', '').strip().title(),
            email=response_item.get('contactPersonEmailAddress', '').replace('\n', ' ').replace('\r', '').strip().lower(),
            contact_person=response_item.get('contactPersonName', '').replace('\n', ' ').replace('\r', '').strip().title()
        )

    def to_dict(self):
        """
        Serializes the TransnetTender object to a dictionary.

        Returns:
            dict: A complete dictionary representation of the Transnet tender.
        """
        # Get the dictionary of base fields from the parent class.
        data = super().to_dict()
        # Add the Transnet-specific fields to the dictionary.
        data.update({
            "tenderNumber": self.tender_number,
            "institution": self.institution,
            "category": self.category,
            "tenderType": self.tender_type,
            "location": self.location,
            "email": self.email,
            "contactPerson": self.contact_person
        })
        return data