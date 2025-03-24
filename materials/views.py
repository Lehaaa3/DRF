from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.permissions import IsUserOwner, IsUserModerator
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return queryset
            if self.request.user.is_authenticated:
                return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsUserModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsUserOwner | IsUserModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsUserOwner, ~IsUserModerator]
        return [permission() for permission in self.permission_classes]


class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Moderators').exists():
                return queryset
            if self.request.user.is_authenticated:
                return queryset.filter(owner=self.request.user)


class LessonRetrieveApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsUserOwner | IsUserModerator]


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsUserModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsUserOwner | IsUserModerator]


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner, ~IsUserModerator]
