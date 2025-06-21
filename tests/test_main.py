from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_docs_available():
    response = client.get('/docs')
    assert response.status_code == HTTPStatus.OK


def test_coverage_push_no_file():
    response = client.post('/api/coverage/push/')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_coverage_push_fake_file():
    fake_content = b'some,excel,content'
    files = {
        'file': (
            'test.xlsx',
            fake_content,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    }
    response = client.post('/api/coverage/push/', files=files)
    assert response.status_code in {HTTPStatus.OK, HTTPStatus.BAD_REQUEST}
