from flask_jwt import current_identity
from models.user import UserModel
from werkzeug.security import safe_str_cmp
import helper

def authenticate(merchantUser,password):
    merchant_code=merchantUser.split()[0]
    username=merchantUser.split()[1]
    user=UserModel.find_by_name(username,merchant_code)
    #if user and user.password==password:
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)

def isSelf(merchant_code,user_id):
    isSelf= (current_identity.merchant_code == merchant_code and
                    current_identity.id == user_id)
    return isSelf

def isAuthorized(merchant_code,username):
    isAuthorized= (current_identity.merchant_code == merchant_code and
                   (current_identity.user_type >= helper.userTypeStaffThreshold()  or
                    current_identity.username == username))
    return isAuthorized

def isStaff(merchant_code):
    isStaff= (current_identity.merchant_code == merchant_code and
                   current_identity.user_type >= helper.userTypeStaffThreshold())
    return isStaff

def isAdmin(merchant_code):
    isAdmin= (current_identity.merchant_code == merchant_code and
                   current_identity.user_type >= helper.userTypeAdminThreshold())
    return isAdmin

def isCorrectMerchant(merchant_code):
    isCorrectMerchant= (current_identity.merchant_code == merchant_code)
    return isCorrectMerchant