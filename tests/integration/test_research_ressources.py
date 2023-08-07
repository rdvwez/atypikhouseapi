import pytest
from .test_order import pytestmark

pytestmark = pytest.mark.run(order=9)

def test_research(client,init_database):
    research_data = {
    "category_id": 1,
    "thematic_id": 2,
    "start_date": "2023-03-10T00:00:00",
    "end_date":"2023-04-01T00:00:00",
    "person_nbr": 1
    }
    response = client.post("/api/research", json=research_data, )

    assert response.status_code == 201