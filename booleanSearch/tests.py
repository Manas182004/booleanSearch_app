#booleanSearch/tests.py


from django.test import TestCase
from rest_framework.test import APIClient
from .models import Candidate

class BooleanSearchTestCase(TestCase):
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        Candidate.objects.create(name="John Doe", profile="Experienced Django and Python developer", email="john@example.com", skills="Django,Python")
        Candidate.objects.create(name="Jane Smith", profile="Frontend developer with React expertise", email="jane@example.com", skills="React,JavaScript")
        Candidate.objects.create(name="Sam Brown", profile="Python backend engineer with Django expertise", email="sam@example.com", skills="Python,Django")

    def test_valid_boolean_query(self):
        """
        Test the boolean search endpoint with a valid query.
        """
        response = self.client.post('/booleanSearch/', {"query": "Django AND Python"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Experienced Django and Python developer", response.data['results'])
        self.assertIn("Python backend engineer with Django expertise", response.data['results'])

    def test_invalid_query(self):
        """
        Test the boolean search endpoint with an empty query.
        """
        response = self.client.post('/booleanSearch/', {"query": ""}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Query cannot be empty.")

    def test_no_results(self):
        """
        Test the boolean search endpoint with a query that returns no results.
        """
        response = self.client.post('/booleanSearch/', {"query": "Java AND Spring"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
