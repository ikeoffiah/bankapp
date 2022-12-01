from django.shortcuts import render, HttpResponse
from rest_framework import generics
from .models import AccountModel, AccountDetail
from .serializers import AccountSerializers
from rest_framework import status
from util.error import Error
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json
from authentications.models import User
import requests





class AccountView(generics.GenericAPIView):
    serializer_class = AccountSerializers
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            account_number =serializer.validated_data['account_number']
            AccountModel.objects.create(user=request.user, account_number=account_number)
            return Response({"success":"account number saved"}, status=status.HTTP_201_CREATED)

        error = Error().error(serializer.errors)

        return Response(error, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
def webhook(request):
    if request.method == "POST":
        body = request.body
        jsoning = body.decode('utf8').replace("'", '"')
        dat = json.loads(jsoning)
        acc_id = dat['data']['account']['_id']

        a = dat['data']['account']['accountNumber']
        account =AccountModel.objects.get(account_number=a)
        print(account.user)
        AccountDetail.objects.create(user=account.user, acc_id=acc_id)


        return HttpResponse("Done")


class AccountDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user

        account_owner = AccountDetail.objects.get(user=user)
        id = account_owner.acc_id

        url = f"https://api.withmono.com/accounts/{id}/transactions"


        payload = {}
        headers = {
            'mono-sec-key': 'test_sk_YoXTIz28MxRgYW6sLf1X'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res =response.json()

        num_page = res['paging']['total']
        range_page = (num_page // 20) + 2
        a =[]
        for i in res['data']:
            a.append(
                {"Id": i['_id'], "amount": i['amount'], "type": i["type"], "balance": i["balance"], "date": i['date']})

        for n in range(2, range_page):
            url = f'https://api.withmono.com/accounts/{id}/transactions?page={n}'

            response = requests.request("GET", url, headers=headers, data=payload)
            ni = response.json()

            for i in ni['data']:
                a.append({"Id": i['_id'], "amount": i['amount'], "type": i["type"], "balance": i["balance"],
                          "date": i['date']})

            credit_sum = []
            for i in a:
                credit_sum.append(i['balance'])

            total = sum(credit_sum)

            credit = []
            credit_detail = []
            debit = []
            debit_detail = []

            for i in a:
                if i['type'] == 'credit':
                    credit.append(i['balance'])
                    credit_detail.append(i)
                else:
                    debit.append(i['balance'])
                    debit_detail.append(i)

        return Response({"total_debit":sum(debit),"total_credit":sum(credit),"credit_detail":credit_detail,"debit_detail":debit_detail, }, status=status.HTTP_200_OK)


