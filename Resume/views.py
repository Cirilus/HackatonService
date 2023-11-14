from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from .serializers import ResumeSerializer, GraduationSerializer, EducationSerializer, WorkSerializer, ContactSerializer, HackatonsSerializer

from .models import Resume, Graduation, Education, Work, Contact, Hackatons


@extend_schema(description="Resume URLs:", tags=["Resume"])
class ResumeCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Resume.objects.all()

        # Добавляем фильтрацию по полю 'visible' из параметров запроса
        visible_param = self.request.query_params.get('visible')
        if visible_param is not None:
            visible_value = visible_param.lower() == 'true'
            queryset = queryset.filter(visible=visible_value)

        return queryset

    def byuserid(self, request, user_id=None):
        self.lookup_field = 'user_id'

        if user_id not in Resume.objects.values_list('user', flat=True):
            return Response({"error": f"Резюме с таким user_id {user_id} не существует."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Добавляем фильтрацию по полю 'visible'
        visible_param = request.query_params.get('visible')
        if visible_param is not None:
            visible_value = visible_param.lower() == 'true'
            queryset = Resume.objects.filter(user_id=user_id, visible=visible_value)
        else:
            queryset = Resume.objects.filter(user_id=user_id)

        if request.method == 'DELETE':
            queryset.delete()
            return Response({"message": f"Записи с user_id {user_id} удалены."}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            instance = queryset.first()
            serializer = ResumeSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResumeSerializer(queryset, many=True)
        return Response(serializer.data)


# получение списка всех объектов, получение создание удаление изменение объектов по resume_id
@extend_schema(description="Work URLs:", tags=["Work"])
class WorkCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    @action(detail=False, methods=['get'], )  # может добавить и другие методы?
    def byresumeid(self, request, resume_id=None):
        # http://127.0.0.1:8000/api/v1/worklist/byuserid/<int:user_id>/
        # получаем все записи которые есть для указанного resume_id
        if resume_id is None:
            return Response({"error": "введите resume_id."}, status=status.HTTP_400_BAD_REQUEST)

        if resume_id not in Work.objects.values_list('resume', flat=True):
            return Response({"error": "записи с таким resume_id не существует"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Work.objects.filter(resume_id=resume_id)
        serializer = WorkSerializer(queryset, many=True)

        return Response(serializer.data)


# получение списка всех объектов, получение создание удаление изменение объектов по resume_id
@extend_schema(description="Contact URLs:", tags=["Contact"])
class ContactCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @action(detail=False, methods=['get'], )  # может добавить и другие методы?
    def byresumeid(self, request, resume_id=None):
        # http://127.0.0.1:8000/api/v1/pointconditionlist/byuserid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if resume_id is None:
            return Response({"error": "введите resume_id."}, status=status.HTTP_400_BAD_REQUEST)

        if resume_id not in Contact.objects.values_list('resume', flat=True):
            return Response({"error": "записи с таким resume_id не существует"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Contact.objects.filter(resume_id=resume_id)
        serializer = ContactSerializer(queryset, many=True)

        return Response(serializer.data)


# получение списка всех объектов, получение создание удаление изменение объектов по resume_id
@extend_schema(description="Hackatons URLs:", tags=["Hackatons"])
class HackatonsCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Hackatons.objects.all()
    serializer_class = HackatonsSerializer

    @action(detail=False, methods=['get'], )
    def byresumeid(self, request, resume_id=None):
        # http://127.0.0.1:8000/api/v1/hackatonslist/byresumeid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if resume_id is None:
            return Response({"error": "введите resume_id."}, status=status.HTTP_400_BAD_REQUEST)

        if resume_id not in Hackatons.objects.values_list('resume', flat=True):
            return Response({"error": "записи с таким resume_id не существует."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Hackatons.objects.filter(resume_id=resume_id)
        serializer = HackatonsSerializer(queryset, many=True)

        return Response(serializer.data)


# получение списка всех объектов, получение создание удаление изменение объектов по resume_id
@extend_schema(description="Education URLs:", tags=["Education"])
class EducationCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    @action(detail=False, methods=['get'], )  # может добавить и другие методы?
    def byresumeid(self, request, resume_id=None):
        # http://127.0.0.1:8000/api/v1/educationlist/byresumeid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if resume_id is None:
            return Response({"error": "введите resume_id."}, status=status.HTTP_400_BAD_REQUEST)

        if resume_id not in Education.objects.values_list('resume', flat=True):
            return Response({"error": "записи с таким resume_id не существует."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Education.objects.filter(resume_id=resume_id)
        serializer = EducationSerializer(queryset, many=True)

        return Response(serializer.data)


# получение списка всех объектов, получение создание удаление изменение объектов по id
@extend_schema(description="Graduation URLs:", tags=["Graduation"])
class GraduationCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Graduation.objects.all()
    serializer_class = GraduationSerializer
