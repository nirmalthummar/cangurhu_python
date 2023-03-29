# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import render, redirect
# from apps.cook.models import Cook
# from .serializers import KitchenImageCaptureFrequencySerializer
# from ..models import KitchenImageCaptureFrequency

# class KitchenImageCaptureFrequencyAPI(APIView):

#     def get(self,request):
#         print("get")
#         data=KitchenImageCaptureFrequency.objects.all()
#         print(data.values())
#         serializer=KitchenImageCaptureFrequencySerializer(data,many=True)
#         return Response(serializer.data)
#         # return Response({"msg":"get"})
#
#     def post(self,request):
#         print("post")
#         # country=self.request.POST['Country']
#         # state=self.request.POST['State']
#         # frequency=self.request.POST['Frequency']
#         # print(country,state,frequency)
#         # KitchenImageCaptureFrequency.objects.filter(id=1).update(country=country,state=state,frequency=frequency)
#         # serializer=KitchenImageCaptureFrequencySerializer(KitchenImageCaptureFrequency.objects.filter(id=1))
#         print(request.data)
#         serializer=KitchenImageCaptureFrequencySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return Response(serializer.data,status=status.HTTP_200_OK)
#             return redirect('dashboard:app-configurations-parameters')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # return Response({"msg":[country,state,frequency]})
#         #return render(request,"dashboard/app-configurations-parameters.html",context=serializer.data)
#         # return redirect('dashboard:app-configurations-parameters')
#
# class KitchenImageCaptureFrequencyAPIUpdate(APIView):
#
#     def get_object(self,pk):
#         try:
#
#             print(pk)
#             print("data",KitchenImageCaptureFrequency.objects.get(pk=pk))
#             return KitchenImageCaptureFrequency.objects.get(pk=pk)
#             # return Response({"msg":"get_object"})
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         # id=pk
#         # data=Model.objects.get(pk=id)
#         # serializer=ModelSerializer(data,data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response({"msg":"data updated"})
#         # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         # return redirect('dashboard:app-configurations-parameters')
#     def get(self,request,pk):
#         print("put")
#         data=self.get_object(pk)
#         print(data)
#         # data=self.get_object(pk)
#         print(request.POST)
#         serializer=KitchenImageCaptureFrequencySerializer(data,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         # return Response({"msg": "get_updated","data":data})
#
#     # def put(self,request,pk):
#     #     print("put")
#     #     print(pk)
#     #     data=self.get_object(pk)
#     #     serializer=KitchenImageCaptureFrequencySerializer(data,data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data,status=status.HTTP_200_OK)
#     #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         # return Response({"msg": "put"})
#
#
#     def delete(self,request,pk):
#         print("delete")
#         id=pk
#         data=KitchenImageCaptureFrequency.objects.get(pk=id)
#         data.delete()
#         return Response({"msg":"record deleted"})
#         # return "deleted"
#
