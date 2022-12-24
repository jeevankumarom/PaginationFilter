
import os
import random
import datetime
import pandas as pd
from django.http import QueryDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .models import categories, category_list
from .serializers import categorySerializer, category_list_serializer


class Queryeditor:

    def __init__(self):
        super(Queryeditor, self).__init__()

    def JSON_query(self, *args, **kwargs):
        data = kwargs["data"]

        query_dict_1 = QueryDict("", mutable=True)

        query_dict_1.update(data)

        return query_dict_1


class post_category(APIView):

    def post(self, request):
        categories_files = os.listdir("F:\\siamCompany\\flipkart_data\\")
        
        json_data = Queryeditor()

        post_list = post_cat_list()

        for categoryname in categories_files:

            if "csv" in categoryname.split(".")[1]:

                cat_name = categoryname.split(".")[0]

                json_data1 = json_data.JSON_query(
                    data={"category_name": cat_name, "date": datetime.datetime.now()}
                )

                if categories.objects.filter(category_name=cat_name).exists() == False:

                    serializer = categorySerializer(data=json_data1)

                    if serializer.is_valid():

                        serializer.save()

                        id = serializer.data["id"]

                else:
                    id = categories.objects.filter(category_name=cat_name).values("id")[0]["id"]

                res = post_list.read_post_data(file=categoryname, id=id)
        return res

class post_cat_list:

    def __init__(self):
        super(post_cat_list, self).__init__()

    def read_post_data(self, **kwargs):
        
        categorylistdataframe = pd.read_csv(
            "F:\\siamCompany\\flipkart_data\\" + kwargs["file"]
        )
        categorylistdataframe = categorylistdataframe.fillna(0)
        foreignkeyvalidation = categories.objects.get(id=kwargs["id"])

        new_list = []
        for key, values in categorylistdataframe.iterrows():

            values["Price"] = str(values["Price"]).replace(",", "")

            values["Original Prices"] = str(values["Original Prices"]).replace(",", "")

            new_list.append(
                category_list(
                    cat_id=foreignkeyvalidation,
                    brand=values["Product Name"],
                    datetime=datetime.datetime.now(),
                    originalprice=values["Original Prices"],
                    price=values["Price"],
                    discount=values["Discount rates"],
                    rating=str(random.choice([1, 2, 3, 4, 5])),
                )
            )

        category_list.objects.bulk_create(new_list)

        return Response("CategoryListUpdated")



class MultiplefilterAPI(APIView, LimitOffsetPagination):

    def get(self, request):

        Makeconditions = {}
        
        for Keys, Values in self.request.GET.items():
            if "category_name" in Keys:

                new_cat = categories.objects.filter(
                    category_name__in=self.request.GET["category_name"].split(",")
                ).values_list("id", flat=True)

                Makeconditions["cat_id__in"] = new_cat

            if "minprice" in Keys:
                Makeconditions["price__gte"] = int(float(self.request.GET["minprice"]))

            if "maxprice" in Keys:
                Makeconditions["price__lte"] = int(float(self.request.GET["maxprice"]))

            if "rating" in Keys:
                Makeconditions["rating__in"] = self.request.GET["rating"].split(",")

        queryset = category_list.objects.filter(**Makeconditions)

        results = self.paginate_queryset(queryset, request, view=self)

        new_serializer = category_list_serializer(results, many=True)

        return self.get_paginated_response(new_serializer.data)


@api_view(["GET"])
def delete_table(request):
    category_list.objects.all().delete()
    return Response("deleted")
