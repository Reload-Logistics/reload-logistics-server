from typing import Union
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


# override class 
class CustomAPIException(APIException):

    def __init__(self, 
                 detail: Union[str, None] = None, 
                 code: int =  HTTP_400_BAD_REQUEST)->None:
        self.status_code = code 
        super().__init__(detail, code)
        


