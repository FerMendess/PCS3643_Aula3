"""Integration tests for root, docs, and OpenAPI endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestRootView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_root_and_docs_endpoints(self):
        resp_root = self.client.get("/")
        self.assertEqual(resp_root.status_code, 200)
        self.assertEqual(resp_root.json()["status"], "online")
        self.assertEqual(resp_root.json()["arquitetura"], "MVC (Model-View-Controller)")

        resp_openapi = self.client.get("/openapi.json")
        self.assertEqual(resp_openapi.status_code, 200)

        resp_docs = self.client.get("/docs")
        self.assertEqual(resp_docs.status_code, 200)
