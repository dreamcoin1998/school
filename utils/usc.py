import  requests
import re
from utils.UscLogin import UscLogin


class Usc(UscLogin):

    @classmethod
    def usc_login(cls):
        return super().UscLoginNew()

    @classmethod
    def usc_timetable(cls):
        pass
