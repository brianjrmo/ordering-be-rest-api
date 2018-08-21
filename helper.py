import helper
import os
from db import db
from flask_jwt import current_identity
from datetime import datetime
from models.audit import AuditModel

DATEYMD='%Y-%m-%d'
DATEYMDHMS='%Y-%m-%d %H:%M:%S'
USER_TYPE_TYPICAL=1
USER_TYPE_STAFF_THRESHOLD=50
USER_TYPE_ADMIN_THRESHOLD=100

IMAGE_SIZE_LIMIT = 600000

def dateYMD():
    return DATEYMD
def dateYMDHMS():
    return DATEYMDHMS
def userTypeTypical():
    return USER_TYPE_TYPICAL
def userTypeStaffThreshold():
    return USER_TYPE_STAFF_THRESHOLD
def userTypeAdminThreshold():
    return USER_TYPE_ADMIN_THRESHOLD
def imageSizeLimit():
    return IMAGE_SIZE_LIMIT

def writelog(message):
    # for debug only, no action in production
    if os.environ.get('DATABASE_URL') is None:
        f = open('message.txt','a')
        f.write(str(message)+'\n')
        f.close()    

def formatString(dataIn):
    if(type(dataIn)==datetime):
        return dataIn.strftime(dateYMDHMS())
    elif(type(dataIn)==bytes):
        return '<bytes>'
    else:
        return str(dataIn)     
    
def valid_date(s):
    return datetime.strptime(s, dateYMD())

def valid_datetime(s):
    return datetime.strptime(s, dateYMDHMS())

def selectFirst(data1,data2):
    if data1 is None:
        return data2
    else:
        return data1
    
def json(dataRow):
    jsonObj= {c.name: helper.formatString(getattr(dataRow, c.name))\
            for c in dataRow.__table__.columns}
    if 'password' in jsonObj:
        jsonObj['password']='********'
    return jsonObj
    
def save_to_db(dataRow):
    toAudit(dataRow,'save')
    db.session.add(dataRow)
    db.session.commit()

def delete_from_db(dataRow):
    toAudit(dataRow,'delete')
    db.session.delete(dataRow)
    db.session.commit()
    
def toAudit(dataRow,action):
    dictData=json(dataRow)
    if dataRow.__tablename__ == 'merchant':
        merchant_code=dictData['code']
    else:
        merchant_code=dictData['merchant_code']
    logRec=AuditModel(merchant_code,\
                      current_identity.username,\
                      action,\
                      dataRow.__tablename__,
                      formatString(datetime.now()),\
                      str(dictData))
    db.session.add(logRec)
            
            
