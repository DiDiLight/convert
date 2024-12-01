import requests
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Converter(APIView):
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'

    def get(self, request):
        params = ('from', 'to', 'value')
        errors = []
        for param in params:
            if param not in request.query_params:
                errors.append({
                    "code": f"required_parameter",
                    "detail": "Отсутствует требуемый параметр",
                    "attr": f"{param}"
                })
        if errors:
            return Response({
                "type": "request_error",
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)

        valuta_from = request.query_params.get('from')
        valuta_to = request.query_params.get('to')
        valuta_value = request.query_params.get('value')
        data = requests.get(self.url).content
        bs_data = BeautifulSoup(data, 'xml')
        from_v = bs_data.find(string=valuta_from)
        to_v = bs_data.find(string=valuta_to)
        if from_v and to_v and valuta_value.isnumeric():
            result = float(from_v.find_parent().find_parent().find('Value').text.replace(',', '.')) / float(
                to_v.find_parent().find_parent().find('Value').text.replace(',', '.')) * float(valuta_value)
            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            return Response({
                "type": "parameters_error",
                "errors": [
                    {
                        "code": f"check_parameter",
                        "detail": "Проверьте правильность введеных параметров",
                        "attr": f"parameters"

                    }
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
