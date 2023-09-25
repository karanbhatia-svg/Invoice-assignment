from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, InvoiceDetail
from rest_framework.decorators import api_view
from django.utils import timezone
from .serilizers import InvoiceDetailSerializer,InvoiceSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET'])
def getInvoiceList(request):
    Invd = InvoiceDetail.objects.all()
    serializer = InvoiceDetailSerializer(Invd, many=True)
 
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def createInvoice(request):
    Invserializer = InvoiceSerializer(data={'CustomerName':request.data['CustomerName'],'Date':timezone.now().date()})
    if Invserializer.is_valid():
        code =Invserializer.save()
    else:
        Response(Invserializer.errors)
        print(Invserializer.errors)
    Invd = InvoiceDetailSerializer(data={'invoice':code.Invoice,'description':request.data['description'],'quantity':request.data['quantity'],'unit_price':request.data['unit_price'],'price':request.data['price']})
    if Invd.is_valid():
        Invd.save()
    else:
        Response(Invd.errors)
    return Response("Invoice created",status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def updateInvoice(request):
    Inv = Invoice.objects.get(Invoice=request.data['id'])
    Invd = InvoiceDetail.objects.get(invoice=request.data['id'])
    Invserializer = InvoiceSerializer(Inv,data={'CustomerName':request.data['CustomerName'],"Date":Inv.Date})
    if Invserializer.is_valid():
        code =Invserializer.save()
    else:
        Response(Invserializer.errors)
    Invd = InvoiceDetailSerializer(Invd,data={'description':request.data['description'],'quantity':request.data['quantity'],'unit_price':request.data['unit_price'],'price':request.data['price']},partial=True)
    if Invd.is_valid():
        Invd.save()
    else:
        Response(Invd.errors)
    return Response("Invoice created",status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def deleteInvoice(request):
    Inv = Invoice.objects.get(Invoice=request.data['id'])
    Invd = InvoiceDetail.objects.get(invoice=request.data['id'])
    Inv.delete()
    Invd.delete()

    return Response('Items delete successfully!',status=status.HTTP_200_OK)