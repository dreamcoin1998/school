from django.contrib.contenttypes.models import ContentType
from images.models import ImagePath
from django.db.models.fields import exceptions


class GetImagePath():
    @property
    def imagePath(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            imgPath_objs = ImagePath.objects.filter(content_type=ct, object_id=self.pk)
            res = []
            for imgPath_obj in imgPath_objs:
                res.append(imgPath_obj.imgPath)
            return res
        except exceptions.ObjectDoesNotExist:
            return []