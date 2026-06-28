from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)



TEST_API_KEY = os.getenv(
    "API_KEY",
    "test-key"
)

def test_create_asset():

    response = client.post(
        "/assets/",
        json={
            "type": "domain",
            "value": "testpytest.com",
            "status": "active",
            "source": "test",
            "tags": [
                "testing"
            ],
            "metadata": {}
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["value"] == "testpytest.com"



def test_get_assets():

    response = client.get(
        "/assets/"
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )
def test_import_dedup():

    import io
    import json


    data = [
        {
            "type": "domain",
            "value": "dedup-test.com",
            "status": "active",
            "source": "test",
            "tags": ["one"],
            "metadata": {
                "key": "old"
            }
        }
    ]


    response1 = client.post(
        "/import/",
        files={
            "file": (
                "data.json",
                io.BytesIO(
                    json.dumps(data).encode()
                ),
                "application/json"
            )
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    )


    assert response1.status_code == 200


    response2 = client.post(
        "/import/",
        files={
            "file": (
                "data.json",
                io.BytesIO(
                    json.dumps(data).encode()
                ),
                "application/json"
            )
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    )


    assert response2.status_code == 200

    result = response2.json()

    assert result["updated_assets"] == 1

def test_filter_assets():

    response = client.get(
        "/assets/?type=domain"
    )


    assert response.status_code == 200


    assets = response.json()


    for asset in assets:
        assert asset["type"] == "domain"
def test_create_relationship():

    asset1 = client.post(
        "/assets/",
        json={
            "type": "domain",
            "value": "source-test.com",
            "status": "active",
            "source": "test",
            "tags": [],
            "metadata": {}
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    ).json()


    asset2 = client.post(
        "/assets/",
        json={
            "type": "domain",
            "value": "target-test.com",
            "status": "active",
            "source": "test",
            "tags": [],
            "metadata": {}
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    ).json()


    response = client.post(
        "/relationships/",
        params={
            "source_id": asset1["id"],
            "target_id": asset2["id"]
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    )


    assert response.status_code == 200


    relation = client.get(
        f"/relationships/{asset1['id']}"
    )


    assert relation.status_code == 200


    ids = [
        asset["id"]
        for asset in relation.json()
    ]


    assert asset2["id"] in ids
def test_import_relationships():

    import io
    import json

    data = [
        {
            "id": "test1",
            "type": "domain",
            "value": "test-domain.com",
            "status": "active",
            "source": "scan",
            "tags": [],
            "metadata": {}
        },
        {
            "id": "test2",
            "type": "subdomain",
            "value": "api.test-domain.com",
            "status": "active",
            "source": "scan",
            "tags": [],
            "metadata": {},
            "parent": "test1"
        }
    ]

    response = client.post(
        "/import/",
        files={
            "file":(
                "data.json",
                io.BytesIO(json.dumps(data).encode()),
                "application/json"
            )
        },
        headers={
            "x-api-key": TEST_API_KEY
        }
    )

    assert response.status_code == 200


    relation = client.get(
        "/relationships/test1"
    )

    assert relation.status_code == 200

    assert relation.json()[0]["id"] == "test2"