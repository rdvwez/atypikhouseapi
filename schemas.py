from typing import Union
from enum import Enum
from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage
from sqlalchemy.dialects.postgresql import ENUM


####### Category schemas ##############################################
class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    show = fields.Bool(required=True)
    libelle = fields.Str(required=True)

class CategoryUpdateSchema(Schema):
    show = fields.Bool()
    libelle = fields.Str()

class CategorySchema(PlainCategorySchema):
    houses = fields.List(fields.Nested(lambda: HouseLimitedSchema()), dump_only = True)
    properties = fields.List(fields.Nested(lambda: PropertyLimitedSchema()), dump_only = True)

class CategoryLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(required=True)

######Thematic Schema ######################################
class PlainThematicSchema(Schema):
    id = fields.Int(dump_only=True)
    show = fields.Bool(required=True)
    libelle = fields.Str(required=True)

class ThematicUpdateSchema(Schema):
    show = fields.Bool()
    libelle = fields.Str()

class ThematicSchema(PlainThematicSchema):
    houses = fields.List(fields.Nested(lambda: HouseLimitedSchema()), dump_only = True)

class ThematicLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(required=True)


######Property Schema ######################################
class PlainPropertySchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(metadata= {'require': False})
    libelle = fields.Str(required=True)
    is_required = fields.Boolean(required=True)

class PropertyUpdateSchema(Schema):
    libelle = fields.Str()
    description = fields.Str()
    is_required = fields.Boolean()

class PropertySchema(PlainPropertySchema):
    category_id = fields.Int(required = True, load_only = True)
    category = fields.Nested(lambda: CategoryLimitedSchema(), dump_only = True)
    values = fields.List(fields.Nested(lambda: PlainValueSchema()), dump_only = True)

class PropertyLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(required=True)

######Value Schema ######################################
class PlainValueSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(required=True)

class ValueUpdateSchema(Schema):
    libelle = fields.Str()

class ValueSchema(PlainValueSchema):
    user_id = fields.Int(required = True, load_only = True)
    property_id = fields.Int(required = True, load_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
    propty_object = fields.Nested(lambda: PropertyLimitedSchema(), dump_only = True)

class ValueLimitedSchema(Schema):
    id = fields.Int(dump_only=True)


#########user schemas########################################

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    firstname = fields.Str(required=False)
    username = fields.Str(required=False)
    phone_number = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only =True)
    is_custom = fields.Boolean(required=True)
    is_owner = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)
    is_activated = fields.Boolean(required=True, dump_only=True)
    birth_date = fields.Date(required=True)
    gender = fields.Boolean(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

class UserRegisterSchema(Schema):
    id = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only =True)

class UserSchema(PlainUserSchema):
    houses = fields.List(fields.Nested(lambda: PlainHouseSchema()), dump_only = True)
    values = fields.List(fields.Nested(lambda: PlainValueSchema()), dump_only = True)
    images = fields.List(fields.Nested(lambda: ImageSchema()), dump_only = True)

class UserLimitedSchema(Schema):
    firstname = fields.Str(required=False)

######### House schemas ###############################################

class PlainHouseSchema(Schema):
    id = fields.Int(
        dump_only=True, 
        error_messages={
            'null': 'Field may not be null.', 
            'required': 'Missing data for required field.', 
            'validator_failed': 'Invalid value.'} )
    show = fields.Bool(required=True)

    libelle = fields.Str(required=True)
    description = fields.Str(metadata= {'require': False})
    # part_number = fields.Integer(required=False)
    bedroom_number = fields.Integer(required=False)
    person_number = fields.Integer(required=False)
    parking_distance = fields.Integer(nullable=False)
    area = fields.Integer(nullable=False)
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(required=False)
    latitude = fields.Float(required= True)
    longitude = fields.Float(required= True)
    address = fields.Str(required=False)
    city = fields.Str(required=False)
    country = fields.Str(required=False)
    # created_at = fields.DateTime(required= True)
    # updated_at = fields.DateTime(required= True)

class HouseUpdateSchema(Schema):
    show = fields.Bool(required=True)
    libelle = fields.Str(required=True)
    description = fields.Str(metadata= {'require': False})
    # part_number = fields.Integer(required=False)
    bedroom_number = fields.Integer(required=False)
    person_number = fields.Integer(required=False)
    parking_distance = fields.Integer(nullable=False)
    area = fields.Integer(nullable=False)
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(required=False)
    latitude = fields.Float(required= True)
    longitude = fields.Float(required= True)
    address = fields.Str(required=False)
    city = fields.Str(required=False)
    country = fields.Str(required=False)
    # created_at = fields.DateTime(required= True)
    # updated_at = fields.DateTime(required= True)

class HouseSchema(PlainHouseSchema):
    category_id = fields.Int(required = True, load_only = True)
    user_id = fields.Int(required = True, load_only = True)
    thematic_id = fields.Int(required = True, load_only = True)
    category = fields.Nested(lambda: CategoryLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
    thematic = fields.Nested(lambda: ThematicLimitedSchema(), dump_only = True)
    images = fields.List(fields.Nested(lambda: ImageSchema()), dump_only = True)

class HouseLimitedSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    libelle = fields.Str(required=True)
    area = fields.Integer(nullable=False)
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(required=False)
    person_number = fields.Integer(required=False)
    parking_distance = fields.Integer(nullable=False)
    description = fields.Str(metadata= {'require': False})

######################### images schemas#######################

class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image"
    }

    def _deserialize(self, value, attr, data) -> Union[FileStorage, None]:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid") #raises Validationerror

        return value

class PlainImageSchema(Schema):
    image = FileStorageField(required=True)
    extension = fields.Str(metadata= {'require': False})
    path = fields.Str(metadata= {'require': False})
    basename = fields.Str(metadata= {'require': False})
    is_avatar = fields.Boolean(required=True)

class ImageSchema(PlainImageSchema):
    house_id = fields.Int(required = False, load_only = True)
    user_id = fields.Int(required = False, load_only = True)
    house = fields.Nested(lambda: HouseLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)

######################### reservations schemas#######################
class ReservationStatus(Enum):
    PENDING = 'pending'
    CANCELED = 'canceled'
    COMPLETED = 'completed'
    FAILED = 'failed'
    DELETED = 'deleted'

class PlainReservationSchema(Schema):
    id = fields.Str(dump_only=True)
    status = fields.Enum(ReservationStatus)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(metadata= {'require': False})

class ReservationUpdateSchema(Schema):
    status = fields.Enum(ReservationStatus)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(metadata= {'require': False})
    

class ReservationSchema(PlainReservationSchema):
    house_id = fields.Int(required = False, load_only = True)
    user_id = fields.Int(required = False, load_only = True)
    house = fields.Nested(lambda: HouseLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)

class ReservationLimitedSchema(Schema):
    id = fields.Str(dump_only=True)
    status = fields.Enum(ReservationStatus)
    amount = fields.Float(nullable=True)








    
