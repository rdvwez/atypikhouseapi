import os 
import importlib.util

from fixtures.category_fixtures import CategoryFixtures
from fixtures.user_fixtures import UserFixtures
from fixtures.thematic_fixtures import ThematicFixtures
from fixtures.property_fixtures import PropertyFixtures
from fixtures.value_fixtures import ValueFixtures
from fixtures.houses_fixture import HouseFixtures
from fixtures.image_fixtures import ImageFixtures
from fixtures.reservation_fixtures import ReservationFixtures

# banned_file = ["__init__.py","__pycache__", "fixtures_loader.py"]



category_fixtures = CategoryFixtures()
thematic_fixtures = ThematicFixtures()
user_fixtures = UserFixtures()
property_fitures = PropertyFixtures()
value_fixtures = ValueFixtures()
house_fixtures = HouseFixtures()
image_fixtures = ImageFixtures()
reservation_fixtures = ReservationFixtures()

def load_all_fixtures():
    category_fixtures.load()
    thematic_fixtures.load()
    user_fixtures.load()
    property_fitures.load()
    value_fixtures.load()
    house_fixtures.load()
    image_fixtures.load()
    reservation_fixtures.load()
    


    

# directory_path = './fixtures_modules'

# for file_name in os.listdir(directory_path):
#     if file_name.endswith('.py'):
#         module_name = file_name[:-3]
#         module_path = os.path.join(directory_path, file_name)
#         spec = importlib.util.spec_from_file_location(module_name, module_path)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         if hasattr(module, 'load'):
#             module.load()
            
   

    