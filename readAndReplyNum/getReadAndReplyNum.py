from django.contrib.contenttypes.models import ContentType
from readAndReplyNum.models import ReadAndReplyNum
from django.db.models.fields import exceptions


class GetReadAndReplyNum():
    @property
    def read_num(self):
        try:
            ct =ContentType.objects.get_for_model(self)
            readAndReplyNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return readAndReplyNum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    @property
    def reply_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readAndReplyNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return readAndReplyNum.reply_num
        except exceptions.ObjectDoesNotExist:
            return 0

    @property
    def main_floor_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readAndReplyNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return readAndReplyNum.main_floor_num
        except exceptions.ObjectDoesNotExist:
            return 0