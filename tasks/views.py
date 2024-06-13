from tasks.models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'customer':
            return self.queryset.filter(customer=user)
        elif user.user_type == 'employee':
            return self.queryset.filter(employee=user) | self.queryset.filter(employee__isnull=True)
        return self.queryset

    def perform_create(self, serializer):
        request = self.request
        if request.user.user_type == 'customer':
            serializer.save(customer=request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        if 'employee' in serializer.validated_data and instance.status == 'pending':
            serializer.validated_data['status'] = 'in_progress'
        serializer.save()

    def perform_destroy(self, instance):
        pass
