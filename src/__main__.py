# from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase
from business_object.user import User
import datetime

reseter = ResetDatabase()
reseter.ResetTEST()
