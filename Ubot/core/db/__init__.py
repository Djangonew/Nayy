
from ubotlibs.ubot.database import cli
from .usersdb import *
from .accesdb import *
from .notesdb import *

import logging
import motor.motor_asyncio
import codecs
import pickle

from string import ascii_lowercase
from typing import Dict, List, Union

from config import MONGO_URL


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db_x = mongo_client["Naya"]