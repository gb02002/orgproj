from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, FormView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from orgs.db_utils import query_rectangular_orm
from orgs.models import Organisation, Locations, FilterforLocation, LocationMedia
from orgs.serializers import BoundsSerializer, LocInfoSerializer, FilterSerializer, LocationIdsSerializer
from .forms import OrgForm, LocationsForm, LocationMediaForm
from django.views.decorators.cache import cache_page
import logging
from django.utils.translation import gettext as _

# Create your views here.
logger = logging.getLogger(__name__)

# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)


@cache_page(60 * 15, key_prefix='about')
def about_view(request):
    logger.debug("about page")
    return render(request, 'about.html')


class OrganisationListView(ListView):
    """Выстилка всех органицаий"""
    model = Organisation
    template_name = 'organisation_list.html'
    context_object_name = 'organisations'

    @method_decorator(cache_page(15 * 60, key_prefix='org_list_all'))
    def get(self, request, *args, **kwargs):
        logging.debug('Entering OrganisationListView get method')
        result = super().get(request, *args, **kwargs)
        logging.debug('Exiting OrganisationListView get method')
        return result

    def get_params(self, request):
        extra_params = request.GET.get('filter_id')
        if extra_params:
            params = [int(id) for id in extra_params.split(',') if id.isdigit()]
            logging.debug(f'Extracted parameters: {params}')  # Пример отладочного сообщения
            return params
        else:
            logging.warning('No filter_id parameter found in request')  # Пример предупреждающего сообщения
            return None

    def get_queryset(self):
        logging.debug('Entering OrganisationListView get_queryset method')  # Пример отладочного сообщения
        queryset = super().get_queryset().all()
        # .values('organisation', 'title', 'phone', 'web')
        logging.debug('Exiting OrganisationListView get_queryset method')  # Пример отладочного сообщения
        return queryset

    def get_context_data(self, **kwargs):
        logging.debug('Entering OrganisationListView get_context_data method')  # Пример отладочного сообщения
        context = super().get_context_data(**kwargs)

        # Добавление данных из get_queryset в контекст представления
        queryset = self.get_queryset()
        p = Paginator(queryset, 3)

        page_number = self.request.GET.get('page')
        page_obj = p.get_page(page_number)

        context['title'] = "Orgs list"
        context['page_obj'] = page_obj

        extra_params = self.get_params(self.request)
        if extra_params:
            context['filters'] = extra_params
        else:
            context['filters'] = None  # или пустой словарь, в зависимости от вашей логики

        logging.debug('Exiting OrganisationListView get_context_data method')  # Пример отладочного сообщения
        return context


class Map2View(View):
    """Базовый view. Подключает все скрипты и они взаимодействуют с остальными представлениями"""

    template_name = "map.html"

    def post(self, request):
        """Unused, token is taken from session"""
        logger.debug("POST of MapView")
        return render(request, self.template_name)

    @method_decorator(cache_page(15 * 60, key_prefix='map_view'))
    def get(self, request):
        logger.debug("GET of MapView")
        return render(request, self.template_name)


class RetrieveLocationsFromCoordsApiView(APIView):
    """Gets ne:sw points from js and sends JSONResponse[locs]"""

    def post(self, request):
        try:
            bounds = request.data.get('bounds')

        except:
            pass


class LocationBoundsFiltersView(APIView):
    """Gets ne:sw points from js, perform instances check and transfer data to utils,
    performs serialization and sends back"""

    def post(self, request) -> Response | JsonResponse:
        bounds = request.data.get('bounds')
        logger.debug(f"raw {bounds}")
        if not bounds or not isinstance(bounds, dict):
            logger.info(f'No or invalid bounds provided in the request: {bounds}')
            return Response({'error': 'No or invalid bounds in request'}, status=status.HTTP_400_BAD_REQUEST)

        bounds_serializer = BoundsSerializer(data={'bounds_dict': bounds})

        if not bounds_serializer.is_valid():
            logger.info(f'Bounds serializer validation failed with {bounds_serializer.errors}')
            return Response(bounds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_bounds: dict = bounds_serializer.validated_data
        output_locations = query_rectangular_orm(current_bounds)

        if output_locations:
            serialized_locations = serialize("geojson", output_locations, geometry_field="point",
                                             fields=['location', 'location_name', 'filter', ])
            logger.debug('locations serialized successfully')
            return JsonResponse({'result': serialized_locations}, status=status.HTTP_200_OK, safe=False)

        logger.debug('No location in the area')
        return Response({'error': 'No location in the area'}, status=status.HTTP_204_NO_CONTENT)


class LocationListApiView(APIView):
    """List of current locations"""

    def get(self, request) -> JsonResponse|Response:

        location_ids = request.query_params.get('location_ids')
        if not location_ids:
            # Если параметр отсутствует, возвращаем сообщение об ошибке
            return Response({'message': 'Parameter location_ids is required'}, status=status.HTTP_400_BAD_REQUEST)

        location_ids_serializer = LocationIdsSerializer(data=request.query_params)
        if location_ids_serializer.is_valid():
            location_ids = location_ids_serializer.validated_data.get('location_ids')
            result_info_location = Locations.loc_man.full_data_map(location_ids)

            logger.debug(f"Res LocationListApiView: {result_info_location}")

            if result_info_location:
                serialized_data = LocInfoSerializer(result_info_location, many=True).data
                logger.debug(f"Serialized locs: {serialized_data}")
                return JsonResponse({'result': serialized_data}, status=status.HTTP_200_OK, safe=False)
            else:
                return Response({'message': 'No locations found'}, status=status.HTTP_204_NO_CONTENT)
        logging.info(f'LocationListApiView: locations_ids not valid: {location_ids_serializer.errors}')
        return Response({'message': 'Incorrect request'}, status=status.HTTP_400_BAD_REQUEST)


class GetFiltersApiView(APIView):
    @method_decorator(cache_page(60 * 15, key_prefix='filters'))
    def get(self, request):
        curr_filters = FilterforLocation.objects.all()
        response_filters = FilterSerializer(curr_filters, many=True).data
        if response_filters:
            logger.debug('Filters retrieved')
            return JsonResponse(data=response_filters, safe=False, status=status.HTTP_200_OK)
        logger.debug(f'Filters retrieving error {FilterSerializer.errors}', )
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganisationDetailView(DetailView):
    template_name = 'detail_org.html'
    model = Organisation
    context_object_name = 'org'
    allow_empty = False

    @method_decorator(cache_page(5 * 60, key_prefix='detail_org-'))
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(obj=self.object)
        return self.render_to_response(context)

    def get_context_data(self, obj, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = obj.locations.all()
        context['title'] = _("Page of ") + obj.title

        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)

        obj = self.get_queryset().filter(organisation=pk).first()

        # Проверяем, что переданный slug соответствует ожидаемому slug
        expected_slug = slugify(f"{obj.organisation}-{obj.title}")
        current_path = self.request.path  # Получаем текущий путь URL
        current_segment = current_path.split('/')[-2]
        if current_segment != expected_slug:
            raise Http404("Organisation does not exist")
        return obj


class ChoiceEditView(LoginRequiredMixin, TemplateView):
    """Шаблонный класс который выдает информацию о всех сущностях и предоставляет редакцию, добавление и удаление"""
    template_name = 'editing.html'
    context_object_name = 'orgs'

    # model = Organisation

    def get_context_data(self, **kwargs):
        """Collects all related instances and offers to add/change/delete"""
        context = super().get_context_data(**kwargs)
        orgs = self.request.user.orgs.all().prefetch_related('locations__media')
        logger.info(f'orgs context {orgs}')
        context['orgs'] = orgs
        context['title'] = _('Records Administration Pane')
        return context

    # @method_decorator(cache_page(15 * 60, key_prefix='agent_view'))
    def get(self, request, *args, **kwargs):
        """Обязательно надо добавить task который сносит этот кеш после updates"""
        request_cookies = request.COOKIES
        # Генерация токена
        response = super().get(request, *args, **kwargs)
        for key, value in request_cookies.items():
            response.set_cookie(key, value)
        if not response.cookies.get('edit_token', False):
            edit_token = get_random_string(length=32)
            response.set_cookie('edit_token', edit_token, max_age=600)
        return response


# class AddOrgView(LoginRequiredMixin, FormView):
#     template_name = 'add_org.html'
#     success_url = reverse_lazy('for_orgs/edit-choice/')  # Подставьте ваш URL
#     org_form_class = OrgForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['org_form'] = self.org_form_class(self.request.POST)
#             context['locations_formset'] = locations_formset_class(self.request.POST, prefix='locations')
#             context['location_media_formsets'] = [
#                 location_media_formset_class(self.request.POST, prefix=f'location_media_{i}')
#                 for i in range(len(context['locations_formset'].forms))
#             ]
#         else:
#             context['org_form'] = self.org_form_class()
#             context['locations_formset'] = locations_formset_class(prefix='locations')
#             context['location_media_formsets'] = [
#                 location_media_formset_class(prefix=f'location_media_{i}')
#                 for i in range(len(context['locations_formset'].forms))
#             ]
#         context['location_formset'] = locations_formset_class(
#             prefix='location')  # Добавляем пустую форму местоположения
#         context['title'] = 'Add organisation'
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         org_form = context['org_form']
#         locations_formset = context['locations_formset']
#         location_media_formsets = context['location_media_formsets']
#
#         if org_form.is_valid() and locations_formset.is_valid() and all(
#                 location_media_formset.is_valid() for location_media_formset in location_media_formsets):
#             org_instance = org_form.save(commit=False)
#
#             for form, location_media_formset in zip(locations_formset.forms, location_media_formsets):
#                 location_instance = form.save(commit=False)
#                 location_instance.related_org = org_instance
#                 location_instance.save()
#
#                 for media_form in location_media_formset.forms:
#                     media_instance = media_form.save(commit=False)
#                     media_instance.location = location_instance
#                     media_instance.save()
#
#             org_instance.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def get_form_class(self):
#         return self.org_form_class


class AddOrg(LoginRequiredMixin, CreateView):
    template_name = 'add_org_1.html'
    success_url = reverse_lazy("edit-choice")  # Подставьте ваш URL
    org_form_class = OrgForm
    model = Organisation
    fields = ['title', 'desc', 'mail', 'phone', 'web']

    def form_valid(self, form):
        form.instance.agent = self.request.user  # Set the agent field to the current user
        logger.info(f'Adding new org for {self.request.user}')
        return super().form_valid(form)


class AddLocforExistingOrgView(LoginRequiredMixin, CreateView):
    template_name = 'add_loc.html'
    org_form_class = LocationsForm
    model = Locations
    fields = ['location_name', 'address', 'open_hours', 'point', 'filter']

    def form_valid(self, form):
        org_id = self.kwargs['pk']
        org = Organisation.objects.get(pk=org_id)  # Получаем объект Org по org_id
        form.instance.related_org = org
        logger.info(f'Adding loc for {org_id}')
        return super().form_valid(form)

    def get_success_url(self):
        logger.info(f'Redirection of success')
        return reverse('edit-choice')  # Подставьте ваш URL


class DelOrgView(LoginRequiredMixin, DeleteView):
    model = Organisation
    template_name = 'confirm_delete_org.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Organisation.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted org {self.kwargs.get('pk')}')
        return super().delete(request, *args, **kwargs)


class DelLocOfOrgView(LoginRequiredMixin, DeleteView):
    model = Locations
    template_name = 'confirm_delete_loc.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Locations.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted loc {self.kwargs['pk']}')
        return super().delete(request, *args, **kwargs)


class EditOrgView(LoginRequiredMixin, UpdateView):
    model = Organisation
    template_name = 'edit_org.html'
    form_class = OrgForm  # Используем вашу собственную форму

    # Указываем URL для перенаправления после успешного обновления
    success_url = reverse_lazy('edit-choice')

    # Переопределяем метод get_object(), чтобы получить объект Organisation для редактирования
    def get_object(self, queryset=None):
        return Organisation.objects.get(pk=self.kwargs['pk'])

    # Переопределяем метод form_valid(), чтобы добавить дополнительную логику при успешном обновлении формы
    def form_valid(self, form):
        # Ваша дополнительная логика
        logger.debug(f'Edited org {self.kwargs['pk']}')
        return super().form_valid(form)


class EditLocView(LoginRequiredMixin, UpdateView):
    model = Locations
    template_name = 'edit_loc.html'
    form_class = LocationsForm  # Используем вашу собственную форму

    # Указываем URL для перенаправления после успешного обновления
    success_url = reverse_lazy('edit-choice')

    # Переопределяем метод get_object(), чтобы получить объект Organisation для редактирования
    def get_object(self, queryset=None):
        return Locations.objects.get(pk=self.kwargs['pk'])

    # Переопределяем метод form_valid(), чтобы добавить дополнительную логику при успешном обновлении формы
    def form_valid(self, form):
        # Ваша дополнительная логика
        logger.debug(f'Edited loc {self.kwargs['pk']}')
        return super().form_valid(form)


class AddLocMedia(LoginRequiredMixin, FormView):
    template_name = 'add_loc_media.html'
    success_url = reverse_lazy("edit-choice")  # Подставьте ваш URL
    org_form_class = LocationMediaForm
    model = LocationMedia
    fields = ['image', 'description', ]

    def get_form_class(self):
        return LocationMediaForm

    def form_valid(self, form):
        logger.debug("Valid form for add loc media")
        loc_id = self.kwargs['pk']
        loc = Locations.objects.get(pk=loc_id)  # Получаем объект Org по org_id
        form.instance.location = loc
        form.save()  # Сохраняем форму
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.info(f"Invalid form for add loc media. Error: {form.error}")
        return super().form_invalid(form)


class EditLocMediaView(LoginRequiredMixin, UpdateView):
    model = LocationMedia
    template_name = 'edit_loc_media.html'
    form_class = LocationMediaForm  # Используем вашу собственную форму
    success_url = reverse_lazy('edit-choice')

    def get_object(self, queryset=None):
        return LocationMedia.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        logger.debug(f'Edited media-form')
        return super().form_valid(form)


class DelLocMediaView(LoginRequiredMixin, DeleteView):
    model = LocationMedia
    template_name = 'confirm_delete_loc_media.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        return LocationMedia.objects.get(pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted media {self.kwargs.get('pk')}')
        return super().delete(request, *args, **kwargs)

    """Какие нужны страницы? 
    1. Добавление локации к орге
    Ответ gpt 3:23 заслуживает внимания. Вынести атрибуты в 2 классе и наследовать на выбор вместе с миксинами и view"""
