## Environment Settings
import os
os.environ["IS_TEST"] = "TRUE"

import unittest
from fastapi.testclient import TestClient
from myapplication.database.crud import ItemCrud
from myapplication.database.schema import ItemSchema
from myapplication.database.model import ItemModel
from myapplication.database.connection import get_db, init_db
from myapplication import app
from fastapi import status

import json


class DummyItem:
    title = "test item"
    description = "this is a test item"

    @classmethod
    def get_title(cls, number=None):
        return f"{cls.title}" if number is None else f"{cls.title}_{number}"
    
    @classmethod
    def get_description(cls, number=None):
        return f"{cls.description}" if number is None else f"{cls.description}_{number}"
    
    @classmethod
    def to_dict(cls, number=None):
        return {"title": cls.get_title(number), "description": cls.get_description(number)}
    
    @classmethod
    def dump_json(cls, number=None):
        return json.dumps(cls.to_dict(number))

class TestCaseV1(unittest.TestCase):
    print("TestCase API V1")
    
    TEST_DB_HOST = os.getenv("TEST_DB_HOST")
    BACKEND_PORT = os.getenv("BACKEND_PORT")
    base_url = f"http://{TEST_DB_HOST}:{BACKEND_PORT}/api/v1"
    
    assert os.getenv("IS_TEST") == "TRUE"

    def setUp(self):
        init_db()
        self.client = TestClient(app=app.app_instance, base_url=self.base_url)
    
    def tearDown(self):
        session = next(get_db())
        session.query(ItemModel).delete()
        session.commit()

    def test_health_check(self):
        response = self.client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status" : "ok"}

    def test_create_item(self):
        response = self.client.post("/items", json=DummyItem.to_dict())
        assert response.status_code == status.HTTP_200_OK

        item_id = response.json()["id"]
        db_item = ItemCrud.read_item(item_id, next(get_db()))
        assert db_item.title == DummyItem.title
        assert db_item.description == DummyItem.description

    def test_read_item(self):
        response = self.client.get("/items/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.get(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == DummyItem.title

    def test_read_items(self):
        CREATE_ITEM = 1000
        SKIP = 100
        LIMIT = 200
        assert CREATE_ITEM - SKIP > LIMIT

        response = self.client.get("/items")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

        items = [ItemSchema.NeedCreate(**DummyItem.to_dict(i)) for i in range(CREATE_ITEM)]
        db_items = ItemCrud._create_items(items, next(get_db()))
        response = self.client.get("/items", params={"skip": SKIP, "limit": LIMIT})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["title"] == db_items[SKIP].title
        assert response.json()[-1]["title"] == db_items[SKIP + LIMIT -1].title

        response = self.client.get("/items")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 100      ## default limit check

        response = self.client.get("/items", params={"skip": 2, "limit": "a"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_item_title(self):
        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.put(f"/items/{db_item.id}", params={"new_title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
        new_title = "new title"
        new_description = "new description"
        response = self.client.put(f"/items/{db_item.id}", params={"new_title": new_title, "new_description": new_description})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == new_title
        assert response.json()["description"] == new_description
    
    def test_delete_item(self):
        response = self.client.delete("/items/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.delete(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_200_OK

        response = self.client.get(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
