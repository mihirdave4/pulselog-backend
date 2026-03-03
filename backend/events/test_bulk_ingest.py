from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
import uuid

# class BulkIngestTest(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="test@test.com",
#             name="Test",
#             password="password"
#         )

#     def test_bulk_ingest(self):
#         self.client.force_authenticate(user=self.user)

#         response = self.client.post(
#             reverse("bulk-ingest"),
#             data=[
#                 {
#                     "event_id": str(uuid.uuid4()),
#                     "event_type": "click",
#                     "payload": {}
#                 }
#             ],
#             format="json"
#         )

#         self.assertEqual(response.status_code, 202)
