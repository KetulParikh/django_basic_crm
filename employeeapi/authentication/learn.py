from rest_framework.views import APIView
from django.db import transaction


class BaseAPIView(APIView):
    required_field_list = []
    ip_address = ""
    user_agent = ""
    api_key = ""
    kp = "advdavdv"
    print(5)

    def validate_required_fields(self, request, partner_api_key):
        print(6)
        """
        Check for mandatory fields in input request and raised exceptions accordingly
        :return:
        """
        try:
            for field in self.required_field_list:
                value = request.data.get(field)
                if not value and not isinstance(value, int):
                    print(value)
                    if not value.strip():
                        print("--------")
        except:
            print("++++++++")
        return True

    def get(self, request, partner_api_key):
        try:
            print("Validating input")
            if self.validate_required_fields(
                request=request, partner_api_key=partner_api_key
            ):
                print(self.required_field_list)
                with transaction.atomic():
                    return self.execute_get(request)
        except Exception as e:
            print(e)

    # def execute_get(self, request):
    #     print("84yt4083yt48ty43t")
    #     pass