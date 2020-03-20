from yonghu.models import Yonghu


class GetPersonal:
    def get_person(self, request):
        # yonghu_pk = request.session['pk']
        yonghu_pk = 'test'
        yonghu_obj = Yonghu.objects.get(pk=yonghu_pk)
        return yonghu_obj