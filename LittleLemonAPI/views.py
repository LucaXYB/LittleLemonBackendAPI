from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import MenuItem, Order, Category, Cart
from .serializers import MenuItemSerializer, OrderSerializer, CategorySerializer, CartSerializer
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Only managers can assign delivery crew to orders
        if request.user.groups.filter(name='Manager').exists():
            order = self.get_object()
            try:
                # Get the delivery crew by id from the request data
                delivery_crew = User.objects.get(id=request.data['delivery_crew_id'])
                order.delivery_crew = delivery_crew
                order.save()
                return Response({"message": "Delivery crew assigned successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Delivery crew not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def get_queryset(self):
        # If the user is in the Delivery crew group, return only orders assigned to them
        if self.request.user.groups.filter(name='Delivery crew').exists():
            return self.queryset.filter(delivery_crew=self.request.user)
        # Otherwise, return all orders
        return self.queryset
    
    def partial_update(self, request, *args, **kwargs):
        # Only the delivery crew assigned to the order can update the order status
        order = self.get_object()
        if self.request.user.groups.filter(name='Delivery crew').exists() and order.delivery_crew == self.request.user:
            order.status = request.data.get('status', order.status)
            order.save()
            return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "You are not authorized to update this order"}, status=status.HTTP_403_FORBIDDEN)
            


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Only admin can create and manage categories


class ManagerGroupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])  # 获取 user_id
            group, created = Group.objects.get_or_create(name='Manager')
            group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryCrewGroupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            group, created = Group.objects.get_or_create(name='Delivery crew')
            group.user_set.add(user)
            return Response({"message": "User added to Delivery crew group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the cart items for the logged-in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Retrieve the menu item based on the provided menuitem_id
        try:
            menuitem = MenuItem.objects.get(id=self.request.data['menuitem_id'])
            # Save the cart item with the menu item and the current user
            serializer.save(user=self.request.user, menuitem=menuitem, quantity=self.request.data['quantity'])
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)