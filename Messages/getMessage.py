from django.contrib.contenttypes.models import ContentType
from Messages.models import Message
from django.db.models.fields import exceptions


class GetMessage():
    @property
    def message(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            message_objs = Message.objects.filter(content_type=ct, object_id=self.pk)
            res = []
            for message_obj in message_objs:
                res.append(message_obj)
            return res
        except exceptions.ObjectDoesNotExist:
            return []