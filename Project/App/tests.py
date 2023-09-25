from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail
class CreateInvoiceTestCase(APITestCase):
    def test_create_invoice(self):
        # Define your request data
        data = {
            "CustomerName": "Test Customer",
            "description": "Test Description",
            "quantity": 2,
            "unit_price": 10.0,
            "price": 20.0
        }

        # Send a POST request to the createInvoice endpoint
        url = reverse("create-invoice")
        response = self.client.post(url, data, format="json")

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response content contains "Invoice created"
        self.assertEqual(response.data, "Invoice created")
        
        
class UpdateInvoiceTestCase(APITestCase):
    def setUp(self):
        # Create some initial data for testing
        self.invoice = Invoice.objects.create(CustomerName="Initial Customer",Date=timezone.now().date())
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Initial Description",
            quantity=1,
            unit_price=10.0,
            price=10.0
        )
    def test_update_invoice(self):
        # Define your request data
        data = {
            "id": self.invoice.Invoice,
            "CustomerName": "Updated Customer",
            "description": "Updated Description",
            "quantity": 2,
            "unit_price": 20.0,
            "price": 40.0
        }

        # Send a POST request to the update-invoice endpoint
        url = reverse("update-invoice")
        response = self.client.post(url, data, format="json")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the Invoice and InvoiceDetail objects were updated
        self.invoice.refresh_from_db()
        self.invoice_detail.refresh_from_db()
        self.assertEqual(self.invoice.CustomerName, "Updated Customer")
        self.assertEqual(self.invoice_detail.description, "Updated Description")
        self.assertEqual(self.invoice_detail.quantity, 2)
        self.assertEqual(self.invoice_detail.unit_price, 20.0)
        self.assertEqual(self.invoice_detail.price, 40.0)

        # Cleanup (if necessary)
        # You may want to delete the objects created during the test to keep the database clean.

class DeleteInvoiceTestCase(APITestCase):
    def setUp(self):
        # Create some initial data for testing
        self.invoice = Invoice.objects.create(CustomerName="Test Customer",Date=timezone.now().date())
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Test Description",
            quantity=1,
            unit_price=10.0,
            price=10.0
        )

    def test_delete_invoice(self):
        # Define your request data
        data = {"id": self.invoice.Invoice}

        # Send a POST request to the delete-invoice endpoint
        url = reverse("delete-invoice")
        response = self.client.post(url, data, format="json")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the Invoice and InvoiceDetail objects were deleted
        with self.assertRaises(Invoice.DoesNotExist):
            Invoice.objects.get(Invoice=self.invoice.Invoice)
        with self.assertRaises(InvoiceDetail.DoesNotExist):
            InvoiceDetail.objects.get(invoice=self.invoice.Invoice)

class GetInvoiceListTestCase(APITestCase):
    def setUp(self):
        # Create some initial data for testing
        self.invoice = Invoice.objects.create(CustomerName="Test Customer",Date=timezone.now().date())
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Test Description",
            quantity=1,
            unit_price=10.0,
            price=10.0
        )

    def test_get_invoice_list(self):
        # Send a GET request to the get-invoice-list endpoint
        url = reverse("invoice-list")
        response = self.client.get(url, format="json")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected data
        self.assertEqual(len(response.data), 1)  # Assuming you expect one item in the list
        self.assertEqual(response.data[0]["description"], "Test Description")