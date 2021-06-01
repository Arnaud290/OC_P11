""" Test module for the showSummary function """
import json
import pytest
from .. import server
from ..config_server import POINTS_PER_PLACE

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


@pytest.fixture
def mock_loadCompetitions_fixture(monkeypatch):
    def mock_loadCompetitions():
        with open('tests/competitions_test.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
    monkeypatch.setattr(
        'Python_Testing.server.competitions',
        mock_loadCompetitions()
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


class TestPurchasePlaces:
    """ Class of tests for the purchasePlaces function """
    def test_purchasePlaces_more_points_allowed(
        self,
        mock_loadClubs_fixture,
        mock_loadCompetitions_fixture
    ):
        """
        When the user indicates more registration places
        than points, it does not deduct points.
        """
        response = client.post(
            '/purchasePlaces',
            data={
                'club': 'Club Test',
                'competition': 'Test Competition',
                'places': '21'
            }
        )
        assert response.status_code == 200
        assert server.clubs[0]['points'] == 20

    def test_purchasePlaces_more_than_12_places_per_competition(
        self,
        mock_loadClubs_fixture,
        mock_loadCompetitions_fixture
    ):
        """
        Checking if a club reserves more than 12 places
        """
        response = client.post(
            '/purchasePlaces',
            data={
                'club': 'Club Test',
                'competition': 'Test Competition',
                'places': '13'
            }
        )
        assert response.status_code == 200
        assert server.competitions[0]['numberOfPlaces'] == 50
        assert server.clubs[0]['points'] == 20

    def test_book_places_in_past_competitions(
        self,
        mock_loadClubs_fixture,
        mock_loadCompetitions_fixture
    ):
        response = client.get(
            '/book/Test Competition/Club Test'
        )
        assert response.status_code == 200
        assert b'Event is too old!' in response.data

    def test_book_places_in_future_competitions(
        self,
        mock_loadClubs_fixture,
        mock_loadCompetitions_fixture
    ):
        response = client.get(
            '/book/Test Future Competition/Club Test'
        )
        assert response.status_code == 200
        assert b'Event is too old!' not in response.data

    def test_purchasePlaces_points_deducted(
        self,
        mock_loadClubs_fixture,
        mock_loadCompetitions_fixture
    ):
        """
        Checking for deduction of club points at registration
        """
        response = client.post(
            '/purchasePlaces',
            data={
                'club': 'Club Test',
                'competition': 'Test Competition',
                'places': '1'
            }
        )
        assert response.status_code == 200
        assert server.clubs[0]['points'] == 20 - 1 * POINTS_PER_PLACE


class TestClubsPoints:
    def test_ClubsPoints(
        self,
        mock_loadClubs_fixture,
    ):
        response = client.get('/clubsPoints')
        assert response.status_code == 200


class TestIndex:
    def test_index(self):
        response = client.get('/')
        assert response.status_code == 200
