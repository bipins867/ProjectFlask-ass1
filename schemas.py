from extensions import ma
from models import User
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True

user_schema = UserSchema()
