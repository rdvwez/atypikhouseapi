import os 

from fixtures.category_fixtures import CategoryFixtures
from fixtures.user_fixtures import UserFixtures
from fixtures.thematic_fixtures import ThematicFixtures
from fixtures.property_fixtures import PropertyFixtures
from fixtures.value_fixtures import ValueFixtures
from fixtures.houses_fixture import HouseFixtures
from fixtures.image_fixtures import ImageFixtures

# banned_file = ["__init__.py","__pycache__", "fixtures_loader.py"]



category_fixtures = CategoryFixtures()
thematic_fixtures = ThematicFixtures()
user_fixtures = UserFixtures()
property_fitures = PropertyFixtures()
value_fixtures = ValueFixtures()
house_fixtures = HouseFixtures()
image_fixtures = ImageFixtures()

def load_all_fixtures():
    category_fixtures.load()
    thematic_fixtures.load()
    user_fixtures.load()
    property_fitures.load()
    value_fixtures.load()
    house_fixtures.load()
    image_fixtures.load()
    


    
    # for file in os.listdir(os.getcwd()+"/fixtures"):
    #     if file not in banned_file:
    #         classname = file.split("_",1)[0].capitalize() + "Fixtures"
    #         print(classname)
            # fixture_object = classname()
            # fixture_object.load()
            
   

    