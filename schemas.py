from typing import Union
from enum import Enum
from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage
from sqlalchemy.dialects.postgresql import ENUM


####### Category schemas ##############################################
class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    show = fields.Bool(metadata= {'require': True})
    libelle = fields.Str(metadata= {'require': True})

class CategoryUpdateSchema(Schema):
    show = fields.Bool()
    libelle = fields.Str()

class CategorySchema(PlainCategorySchema):
    houses = fields.List(fields.Nested(lambda: HouseLimitedSchema()), dump_only = True)
    properties = fields.List(fields.Nested(lambda: PropertyLimitedSchema()), dump_only = True)

class CategoryLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(metadata= {'require': True})

######Thematic Schema ######################################
class PlainThematicSchema(Schema):
    id = fields.Int(dump_only=True)
    show = fields.Bool(metadata= {'require': True})
    libelle = fields.Str(metadata= {'require': True})

class ThematicUpdateSchema(Schema):
    show = fields.Bool()
    libelle = fields.Str()

class ThematicSchema(PlainThematicSchema):
    houses = fields.List(fields.Nested(lambda: HouseLimitedSchema()), dump_only = True)

class ThematicLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(metadata= {'require': True})


######Property Schema ######################################
class PlainPropertySchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(metadata= {'require': False})
    libelle = fields.Str(metadata= {'require': True})
    is_required = fields.Boolean(metadata= {'require': True})

class PropertyUpdateSchema(Schema):
    category_id = fields.Int()
    libelle = fields.Str()
    description = fields.Str()
    is_required = fields.Boolean()

class PropertySchema(PlainPropertySchema):
    category_id = fields.Int(required = True, load_only = True)
    category = fields.Nested(lambda: CategoryLimitedSchema(), dump_only = True)
    property_values = fields.List(fields.Nested(lambda: PlainValueSchema()), dump_only = True)

class PropertyLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(metadata= {'require': True})

######Value Schema ######################################
class PlainValueSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(metadata= {'require': True})

class ValueUpdateSchema(Schema):
    libelle = fields.Str()
    property_id = fields.Int()

class ValueSchema(PlainValueSchema):
    # user_id = fields.Int(required = True, load_only = True)
    property_id = fields.Int(required = True, load_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
    property_object = fields.Nested(lambda: PropertyLimitedSchema(), dump_only = True)

class ValueLimitedSchema(Schema):
    id = fields.Int(dump_only=True)


#########user schemas########################################

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(metadata= {'require': True})
    firstname = fields.Str(metadata= {'require': False})
    username = fields.Str(metadata= {'require': False})
    phone_number = fields.Str(metadata= {'require': True})
    email = fields.Str(metadata= {'require': True})
    password = fields.Str(metadata= {'require': True}, load_only =True)
    is_customer = fields.Boolean(metadata= {'require': True})
    is_owner = fields.Boolean(metadata= {'require': True})
    is_admin = fields.Boolean(metadata= {'require': True})
    is_activated = fields.Boolean(metadata= {'require': True}, dump_only=True)
    birth_date = fields.Date(metadata= {'require': True})
    gender = fields.Boolean(metadata= {'require': True})
    created_at = fields.DateTime(metadata= {'require': True})
    updated_at = fields.DateTime(metadata= {'require': True})

class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(metadata= {'require': False})
    username = fields.Str(metadata= {'require': False})
    password = fields.Str(metadata= {'require': True}, load_only =True)
class UserPasswordSetSchema(Schema):
    password = fields.Str(metadata= {'require': True}, load_only =True)

class UserRefreshTokenSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()

class UserSchema(PlainUserSchema):
    houses = fields.List(fields.Nested(lambda: PlainHouseSchema()), dump_only = True)
    values = fields.List(fields.Nested(lambda: PlainValueSchema()), dump_only = True)
    images = fields.List(fields.Nested(lambda: ImageLimitedSchema()), dump_only = True)

class UserLoginSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
class UserLogoutSchema(Schema):
    message = fields.Str()
class UserLimitedSchema(Schema):
    id = fields.Str(dump_only=True)
    firstname = fields.Str(metadata= {'require': False})
    name = fields.Str(metadata= {'require': True})

class UserSuperLimitedSchema(Schema):
    firstname = fields.Str(metadata= {'require': False})
    name = fields.Str(metadata= {'require': True})

######### House schemas ###############################################

class PlainHouseSchema(Schema):
    id = fields.Int(
        dump_only=True, 
        error_messages={
            'null': 'Field may not be null.', 
            'required': 'Missing data for required field.', 
            'validator_failed': 'Invalid value.'} )
    show = fields.Bool(metadata= {'require': True})
    libelle = fields.Str(metadata= {'require': True})
    description = fields.Str(metadata= {'require': False})
    bedroom_number = fields.Integer(metadata= {'require': False})
    person_number = fields.Integer(metadata= {'require': False})
    parking_distance = fields.Integer(metadata= {'nullable': False})
    area = fields.Integer(metadata= {'nullable': False})
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(metadata= {'require': False})
    latitude = fields.Float(required= True)
    longitude = fields.Float(required= True)
    address = fields.Str(metadata= {'require': False})
    city = fields.Str(metadata= {'require': False})
    country = fields.Str(metadata= {'require': False})
    created_at = fields.DateTime(metadata= {'require': True})

class HouseUpdateSchema(Schema):
    libelle = fields.Str(metadata= {'require': True})
    description = fields.Str(metadata= {'require': False})
    bedroom_number = fields.Integer(metadata= {'require': False})
    person_number = fields.Integer(metadata= {'require': False})
    parking_distance = fields.Integer(metadata= {'nullable': False})
    area = fields.Integer(metadata= {'nullable': False})
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(metadata= {'require': False})
    latitude = fields.Float(required= True)
    longitude = fields.Float(required= True)
    address = fields.Str(metadata= {'require': False})
    city = fields.Str(metadata= {'require': False})
    country = fields.Str(metadata= {'require': False})
    created_at = fields.DateTime(metadata= {'require': True})
    updated_at = fields.DateTime(metadata= {'require': True})

class HouseSchema(PlainHouseSchema):
    category_id = fields.Int(required = True, load_only = True)
    user_id = fields.Int(required = True, load_only = True)
    thematic_id = fields.Int(required = True, load_only = True)
    category = fields.Nested(lambda: CategoryLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
    thematic = fields.Nested(lambda: ThematicLimitedSchema(), dump_only = True)
    images = fields.List(fields.Nested(lambda: ImageLimitedSchema()), dump_only = True)

class HouseCitiesSchema(Schema):
    city = fields.Str(metadata= {'require': True})

class HouseLimitedSchema(Schema):
    id = fields.Int(metadata= {'require': True}, dump_only=True)
    libelle = fields.Str(metadata= {'require': True})
    area = fields.Integer(metadata= {'nullable': False})
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(metadata= {'require': False})
    person_number = fields.Integer(metadata= {'require': False})
    parking_distance = fields.Integer(metadata= {'nullable': False})
    description = fields.Str(metadata= {'require': False})
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
    created_at = fields.DateTime(metadata= {'require': True})

class HouseLimitedSchemaForResearch(Schema):
    id = fields.Int(metadata= {'require': True}, dump_only=True)
    libelle = fields.Str(metadata= {'require': True})
    area = fields.Integer(metadata= {'nullable': False})
    water = fields.Bool(required= True)
    power = fields.Bool(required= True)
    price = fields.Integer(metadata= {'require': False})
    person_number = fields.Integer(metadata= {'require': False})
    parking_distance = fields.Integer(metadata= {'nullable': False})
    description = fields.Str(metadata= {'require': False})
    user = fields.Nested(lambda: UserSuperLimitedSchema(), dump_only = True)
    category = fields.Nested(lambda: CategoryLimitedSchema(), dump_only = True)
    thematic = fields.Nested(lambda: ThematicLimitedSchema(), dump_only = True)
    images = fields.List(fields.Nested(lambda: ImageWithoutHousesSchema()), dump_only = True)
    created_at = fields.DateTime(metadata= {'require': True})

class HouseFilterSchema(Schema):
    category_id= fields.Int()
    thematic_id= fields.Int()
    city = fields.Str() 

######################### images schemas#######################

class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image"
    }

    def _deserialize(self, value, attr, data, **kwargs) -> Union[FileStorage, None]:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid") #raises Validationerror

        return value
    
class UploadImageSchema(Schema):
    image = FileStorageField(metadata= {'required': True,})
    # house_id = fields.Int(required = False, load_only = True)
    # user_id = fields.Int(required = True, load_only = True)

class PlainImageSchema(Schema):
    id = fields.Int(dump_only=True)
    # image = FileStorageField(metadata= {'require': True})
    extension = fields.Str(metadata= {'require': False})
    path = fields.Str(metadata= {'require': False})
    basename = fields.Str(metadata= {'require': False})
    is_avatar = fields.Boolean(metadata= {'require': True})
    type_mime = fields.Str(metadata= {'require': False}) 
    size = fields.Int(metadata= {'require': False})

class PlainImageUpdateSchema(Schema):
    # image = FileStorageField(metadata= {'require': True})
    # extension = fields.Str(metadata= {'require': False})
    path = fields.Str(metadata= {'require': False})
    basename = fields.Str(metadata= {'require': False})
    is_avatar = fields.Boolean(metadata= {'require': True})
    type_mime = fields.Str(metadata= {'require': False}) 
    size = fields.Int(metadata= {'require': False})
    house_id = fields.Int(required = False, load_only = True)

class ImageLimitedSchema(Schema):
    path = fields.Str(metadata= {'require': False})
class ImageSchema(PlainImageSchema):
    house_id = fields.Int(required = False, load_only = True)
    user_id = fields.Int(required = True, load_only = True)
    house = fields.Nested(lambda: HouseLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)

class ImageWithoutHousesSchema(PlainImageSchema):
    user_id = fields.Int(required = False, load_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)

class ImageWithoutUsersSchema(PlainImageSchema):
    house_id = fields.Int(required = False, load_only = True)
    house = fields.Nested(lambda: HouseLimitedSchema(), dump_only = True)

######################### reservations schemas#######################
class ReservationStatus(Enum):
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    DELETED = 'DELETED'

class PlainReservationSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Enum(ReservationStatus)
    start_date = fields.DateTime(metadata= {'require': True})
    end_date = fields.DateTime(metadata= {'require': True})
    card_number = fields.Str(metadata= {'require': True})
    card_exp_month = fields.Int(metadata= {'require': True})
    card_exp_year = fields.Int(metadata= {'require': True})
    cvc = fields.Str(metadata= {'require': True})
    amount = fields.Float(metadata= {'require': True})

class ReservationUpdateSchema(Schema):
    status = fields.Enum(ReservationStatus)
    start_date = fields.DateTime(metadata= {'require': True})
    end_date = fields.DateTime(metadata= {'require': True})
    

class ReservationSchema(PlainReservationSchema):
    house_id = fields.Int(required = False, load_only = True)
    user_id = fields.Int(required = False, load_only = True)
    house = fields.Nested(lambda: HouseLimitedSchema(), dump_only = True)
    user = fields.Nested(lambda: UserLimitedSchema(), dump_only = True)
class ReservationCreationSchema(Schema):
    start_date = fields.DateTime(metadata= {'require': True})
    end_date = fields.DateTime(metadata= {'require': True})
    card_number = fields.Str(metadata= {'require': True})
    card_exp_month = fields.Int(metadata= {'require': True})
    card_exp_year = fields.Int(metadata= {'require': True})
    cvc = fields.Str(metadata= {'require': True})
    amount = fields.Float(metadata= {'require': True})
    house_id = fields.Int(required = False, load_only = True)

class ReservationLimitedSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Enum(ReservationStatus)
    amount = fields.Float(metadata= {'nullable': True})

class ResearchSchema(Schema):
    category_id= fields.Int()
    thematic_id= fields.Int()
    start_date=fields.DateTime(metadata= {'require': True})
    end_date = fields.DateTime(metadata= {'require': True})
    person_nbr= fields.Int()








    
