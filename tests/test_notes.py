import pytest


@pytest.fixture()
def mock_note():
    return {"title": "something", "description": "something else"}


@pytest.fixture()
def mock_post(mocker):
    return mocker.patch("app.api.notes.crud.post")


@pytest.fixture()
def mock_get(mocker):
    return mocker.patch("app.api.notes.crud.get")


@pytest.fixture()
def mock_get_all(mocker):
    return mocker.patch("app.api.notes.crud.get_all")


@pytest.fixture()
def mock_put(mocker):
    return mocker.patch("app.api.notes.crud.put")


@pytest.fixture()
def mock_delete(mocker):
    return mocker.patch("app.api.notes.crud.delete")


def test_create_note(test_app, mock_note, mock_post):
    note_id = 1
    test_request_payload = mock_note
    test_response_payload = {"id": note_id, **mock_note}
    mock_post.return_value = note_id

    response = test_app.post("/notes/", json=test_request_payload)
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", json={"title": "something"})
    assert response.status_code == 422

    response = test_app.post("/notes/", json={"title": "1", "description": "2"})
    assert response.status_code == 422


def test_read_note(test_app, mock_note, mock_get):
    note_id = 1
    test_data = {"id": note_id, **mock_note}
    mock_get.return_value = test_data

    response = test_app.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, mock_get):
    mock_get.return_value = None

    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notes/0")
    assert response.status_code == 422


def test_read_notes(test_app, mock_note, mock_get_all):
    note_id = 1
    test_data = [{"id": note_id, **mock_note}]
    mock_get_all.return_value = test_data

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, mock_note, mock_get, mock_put):
    note_id = 1
    test_update_data = {"id": note_id, **mock_note}
    mock_get.return_value = note_id
    mock_put.return_value = note_id

    response = test_app.put(f"/notes/{note_id}/", json=test_update_data)
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "note_id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, mock_get, note_id, payload, status_code):
    mock_get.return_value = None

    response = test_app.put(f"/notes/{note_id}/", json=payload)
    assert response.status_code == status_code


def test_remove_note(test_app, mock_note, mock_get, mock_delete):
    note_id = 1
    test_data = {"id": note_id, **mock_note}
    mock_get.return_value = test_data
    mock_delete.return_value = note_id

    response = test_app.delete(f"/notes/{note_id}/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, mock_get):
    mock_get.return_value = None

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == 422
