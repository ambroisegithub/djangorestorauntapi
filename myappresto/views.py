from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,MenuItem1
from .serializers import  MenuItemSerializer,MenuItemSerializer1
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User , Group
# Create your views here.
# serializer 1
class MenuItemView(generics.ListCreateAPIView):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    
class SingletMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    

# @api_view()
# def menu_items(request):
#     items = MenuItem.objects.select_related('category').all()
#     serialized_items = MenuItemSerializer(items,many=True)
#     return Response(serialized_items.data)
#     # return Response(items.values())
    
    
# @api_view()
# def single_items(request,id):
#     items = get_object_or_404(MenuItem, pk=id)
#     serialized_items = MenuItemSerializer1(items)
#     return Response(serialized_items.data)  


# deserialization 
# filtering and searching  
  
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # filtering  
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        # searching
        search = request.query_params.get('search')
        # ordering
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default =2)
        page = request.query_params.get('page',default =1)
        if category_name:
            items = items.filter(category=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__istartswith=search)
        if ordering:
            # items = items.order_by(ordering)  
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
            paginator = Paginator(items, per_page= perpage)
            try:
                items = paginator.page(number=page)
            except EmptyPage:
                items = []   
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status=status.HTTP_201_CREATED)

    # return Response(items.values())
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
  
    return Response({"some authentication required"})    



@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
       return Response({"only shakur manager is allowed to see this"}) 
    else:
     return Response({"message":"you are not authorized"},403)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method =='DELETE':
              managers.user_set.remove(user)
        return Response({"message":"OK"}) 
    
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)        
    
@api_view()
def single_items(request,id):
    items = get_object_or_404(MenuItem, pk=id)
    serialized_items = MenuItemSerializer1(items)
    return Response(serialized_items.data)     
    
#To use serilizer  2 using @api_view
@api_view(['POST'])
def create_item(request):
    serialized_item = MenuItemSerializer1(data=request.data)
    if serialized_item.is_valid():
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer1(item, data=request.data)
    if serialized_item.is_valid():
        serialized_item.save()
        return Response(serialized_item.data)
    return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
 



