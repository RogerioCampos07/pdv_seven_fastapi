from http import HTTPStatus

from fastapi.testclient import TestClient

from pdv_seven_fastapi.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_hello_world():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'World'}
