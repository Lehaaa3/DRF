from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination, LessonPagination
from materials.permissions import IsUserOwner, IsUserModerator
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_mail_for_subscribers


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset

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
        elif self.action == 'course_subscribe':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        course = serializer.instance

        subscriptions_list = course.subscriptions.all()
        user_list = [subscription.user.email for subscription in subscriptions_list]

        send_mail_for_subscribers.delay(course.title, user_list)

        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def course_subscribe(self, request, pk=None):
        user = self.request.user
        course = get_object_or_404(Course, pk=pk)
        try:
            subs_item = Subscription.objects.get(user=user, course=course)
            subs_item.delete()
            message = 'подписка удалена'
        except ObjectDoesNotExist:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        return Response({"message": message})


class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        if self.request.user.groups.filter(name='Moderators').exists():
            return queryset

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
    permission_classes = [IsAuthenticated & ~IsUserModerator | IsAuthenticated & IsUserOwner]
