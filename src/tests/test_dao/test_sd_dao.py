import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.sd_dao import UserDAO
from business_object.user import User  