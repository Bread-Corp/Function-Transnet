import unittest
from datetime import datetime
from models import TransnetTender, SupportingDoc

class TestTransnetModels(unittest.TestCase):

    def test_from_api_response_valid(self):
        sample = {
            "rowKey": "abc123",
            "nameOfTender": "Upgrade of Rail",
            "descriptionOfTender": "Full overhaul of rail infrastructure",
            "publishedDate": "10/01/2025 09:00:00 AM",
            "closingDate": "10/31/2025 04:00:00 PM",
            "attachment": "https://example.com/doc.pdf",
            "tenderNumber": "TN123",
            "nameOfInstitution": "Transnet Freight Rail",
            "tenderCategory": "Infrastructure",
            "tenderType": "Open",
            "locationOfService": "Durban",
            "contactPersonEmailAddress": "contact@transnet.co.za",
            "contactPersonName": "John Doe"
        }

        tender = TransnetTender.from_api_response(sample)
        self.assertIsNotNone(tender)
        self.assertEqual(tender.tender_number, "TN123")
        self.assertEqual(tender.location, "Durban")
        self.assertEqual(tender.email, "contact@transnet.co.za")
        self.assertEqual(len(tender.supporting_docs), 1)

    def test_from_api_response_missing_id(self):
        sample = {
            "nameOfTender": "Upgrade of Rail"
        }
        tender = TransnetTender.from_api_response(sample)
        self.assertIsNone(tender)

    def test_to_dict_structure(self):
        tender = TransnetTender(
            title="Rail Upgrade",
            description="Fix tracks",
            source="Transnet",
            published_date=datetime(2025, 10, 1, 9, 0),
            closing_date=datetime(2025, 10, 31, 16, 0),
            supporting_docs=[SupportingDoc("Doc", "https://example.com")],
            tags=[],
            tender_number="TN123",
            institution="Transnet",
            category="Infrastructure",
            tender_type="Open",
            location="Durban",
            email="contact@transnet.co.za",
            contact_person="John Doe"
        )
        data = tender.to_dict()
        self.assertEqual(data["title"], "Rail Upgrade")
        self.assertEqual(data["supporting_docs"][0]["url"], "https://example.com")
        self.assertEqual(data["email"], "contact@transnet.co.za")

if __name__ == '__main__':
    unittest.main()
