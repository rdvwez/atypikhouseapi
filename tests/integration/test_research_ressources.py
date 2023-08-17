import pytest
from .test_order import pytestmark

pytestmark = pytest.mark.run(order=9)

def test_research(client,init_database):
    research_data = {
    "category_id": 2,
    "thematic_id": 2,
    "start_date": "2023-06-10T00:00:00",
    "end_date":"2023-06-13T00:00:00",
    "person_nbr": 3
    }
    response = client.post("/api/research", json=research_data, )

    assert response.status_code == 201
    assert response.json == [{'area': 12, 'category': {'id': 2, 'libelle': 'cabane'}, 'description': 'Good second house', 'id': 3, 'images': [], 'libelle': 'third house', 'parking_distance': 5, 'person_number': 3, 'power': True, 'price': 60, 'thematic': {'id': 2, 'libelle': 'familial'}, 'user': {'firstname': 'Jannete', 'name': 'Dhoe'}, 'water': False}]    