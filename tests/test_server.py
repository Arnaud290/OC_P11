""" Test module for the showSummary function """
import json
import pytest
from .. import server

client = server.app.test_client()


@pytest.fixture
def mock_loadClubs_fixture(monkeypatch):
    def mock_loadClubs():
        with open('tests/clubs_test.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    monkeypatch.setattr(
        'Python_Testing.server.clubs',
        mock_loadClubs()
    )

class TestShowSummary:
    """ Class of tests for the showSummary function """
    def test_showSummary_post_email(
        self,
        mock_loadClubs_fixture
    ):
        """
        When posting from '/' to '/showSummary',
        if the email entered is not recognised,
        it redirects to the index (302).
        If the email is good, it returns (200).
        """
        response = client.post(
            '/showSummary',
            data={'email': 'club@test.com'}
        )
        assert response.status_code == 200
        response = server.app.test_client().post(
            '/showSummary',
            data={'email': 'club@test_false.com'}
        )
        assert response.status_code == 302
