from app import db
import enum
from app import security as scr
import datetime


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    dadsName = db.Column(db.String(120))
    phone = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dateOfBurn = db.Column(db.Date)
    sitizenshipOfRussia = db.Column(db.Boolean)
    animals = db.Column(db.Integer)
    photo = db.Column(db.String(120))
    qr = db.Column(db.String(120))
    dateOfRegistration = db.Column(db.Date)
    token = db.Column(db.String(120))
    checkCode = db.Column(db.String(120))
    isVerified = db.Column(db.Boolean)
    rating = db.Column(db.Float)
    child = db.Column(db.Float)
    passwordHash = db.Column(db.String(120))
    passportId = db.Column(db.Integer)

    def setData(self, json):
        '''
        Вручную вбивать нужно _passport, dateOfRegistration, token
        '''
        for el in json:
            if el == '_passport':
                continue
            if el == 'photo':
                if self.photo == None:
                    setattr(self, 'photo',
                            scr.sendImageToMediaServer(json[el]))
                    continue
                else:
                    remImageFromMediaServer(json[el])
                    setattr(self, 'photo',
                            scr.sendImageToMediaServer(json[el]))
                    continue
            if el == 'password':
                setattr(self, 'passwordHash',
                        scr.generatePasswordHash(json[el]))
                continue
            if el == 'dateOfBurn':
                self.dateOfBurn = datetime.datetime.strptime(
                    json[el], "%Y-%m-%d").date()
                continue
            setattr(self, el, json[el])

    def getData(self):
        fieldsOfClass = list(filter(lambda x: x.find('_') == -1, dir(self)))
        myDict = {}
        for el in fieldsOfClass:
            if el == 'metadata' or el == 'getData' or el == 'setData' or el == 'query' or el == 'passwordHash' or el == 'registry':
                continue
            if el == 'dateOfBurn':
                myDict[el] = getattr(self, el[0:16])
                continue
            myDict[el] = getattr(self, el)
        return myDict
