from django.contrib.contenttypes.models import ContentType
from readAndReplyNumAndLikes.models import ReadAndReplyNum
from django.db.models.fields import exceptions


class GetReadAndReplyAndLikesNum():
    @property
    def read_num(self):
        try:
            ct =ContentType.objects.get_for_model(self)
            GetReadAndReplyAndLikesNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return GetReadAndReplyAndLikesNum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    @property
    def reply_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            GetReadAndReplyAndLikesNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return GetReadAndReplyAndLikesNum.reply_num
        except exceptions.ObjectDoesNotExist:
            return 0

    @property
    def main_floor_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            GetReadAndReplyAndLikesNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return GetReadAndReplyAndLikesNum.main_floor_num
        except exceptions.ObjectDoesNotExist:
            return 0
    @property
    def like_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            GetReadAndReplyAndLikesNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return GetReadAndReplyAndLikesNum.like_num
        except exceptions.ObjectDoesNotExist:
            return 0

