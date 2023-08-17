

import pytest

pytestmark = [
    pytest.mark.run(order=1),  # Marqueur pour la catégorie "category"
    pytest.mark.run(order=2),  # Marqueur pour la catégorie "thematic"
    pytest.mark.run(order=3),  # Marqueur pour la catégorie "user"
    pytest.mark.run(order=4),  # Marqueur pour la catégorie "property"
    pytest.mark.run(order=5),  # Marqueur pour la catégorie "value"
    pytest.mark.run(order=6),  # Marqueur pour la catégorie "house"
    pytest.mark.run(order=7),  # Marqueur pour la catégorie "image"
    pytest.mark.run(order=8),  # Marqueur pour la catégorie "reservation"
    pytest.mark.run(order=9),  # Marqueur pour la catégorie "researche"
    # Autres marqueurs pour les catégories suivantes...
]
