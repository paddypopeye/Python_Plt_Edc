# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from account.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from django.db.models import Count
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet
from .models import Course, Module, Subject, Content
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class ManageCourseListView(ListView):
	model = Course
	template_name = 'courses/manage/course/list.html'

	def get_queryset(self):
		qs = super(ManageCourseListView, self).get_queryset()
		return qs.filter(owner=self.request.user)

class OwnerMixin(object):
	def get_queryset(self):
		qs = super(OwnerMixin, self).get_queryset()
		return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
	model = Course
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('courses:manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('courses:manage_course_list')
	template_name = 'courses/manage/course/form.html'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
	permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
	template_name = 'courses/manage/course/form.html'
	permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
	template_name = 'courses/manage/course/delete.html'
	success_url = reverse_lazy('courses:manage_course_list')

class CourseModuleUpdateView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/formset.html'
	course = None

	def get_formset(self, data=None):
		return ModuleFormSet(instance=self.course, data=data)

	def dispatch(self, request, pk):
		self.course = get_object_or_404(Course, id=pk, owner=request.user)
		return super(CourseModuleUpdateView, self).dispatch(request, pk)

	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		return self.render_to_response({'course': self.course, 'formset': formset})

	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('courses:manage_course_list')
		return self.render_to_response({'course': self.course, 'formset': formset})

class ModuleContentListView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/content_list.html'

	def get(self, request, module_id):
		module = get_object_or_404(Module, id=module_id, course__owner=request.user)
		
		return self.render_to_response({'module': module})

class ContentCreateUpdateView(TemplateResponseMixin, View):
	template_name = 'courses/manage/content/form.html'
	module = None
	model = None
	obj = None
	

	def get_model(self, model_name):
		if model_name in ['text', 'video', 'image', 'file']:
			return apps.get_model(app_label='courses', model_name=model_name)
		return None

	def get_form(self, model, *args, **kwargs):
		Form = modelform_factory(model, exclude=['owner','order','created','updated'])

		return Form(*args, **kwargs)

	def dispatch(self, request, module_id, model_name, id=None):
		self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
		self.model = self.get_model(model_name)
		if id:
			self.obj = get_object_or_404(self.model, id=id, owner=request.user)
		return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

	def get(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj)
		return self.render_to_response({'form': form, 'object': self.obj})

	def post(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.owner = request.user
			obj.save()

			if not id:
				Content.objects.create(module=self.module, item=obj)
			return redirect('courses:module_content_list', self.module.id)
		return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View):
	def post(self, request, id):
		content = get_object_or_404(Content, id=id, module__course__owner=request.user)
		module = content.module
		content.item.delete()
		content.delete()
		
		return redirect('courses:module_content_list', module.id)#

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Module.objects.filter(id=id, course__owner=request.user).update(order=order)
		return self.render_json_response({'saved':'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id,module__course__owner=request.user).update(order=order)
		return self.render_json_response({'saved':'OK'})

class CourseListView(TemplateResponseMixin, View):
	model = Course 
	template_name = 'courses/course/list.html'

	def get(self, request, subject=None):
		subjects = cache.get('all_subjects')
		if not subjects:
			subjects = Subject.objects.annotate(total_courses=Count('courses'))
			cache.set('all_subjects', subjects)
		courses = Course.objects.annotate(total_modules=Count('modules'))

		if subject:
			subject = get_object_or_404(Subject, slug=subject)
			courses = Course.objects.filter(subject=subject)
		return self.render_to_response({'subjects': subjects,'subject': subject, 'courses': courses})

class CourseDetailView(DetailView):
	model = Course
	template_name = 'courses/course/detail.html'

	def get_context_data(self, **kwargs):
		context = super(CourseDetailView, self).get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})

		return context

def teacher_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)	
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username = cd['username'], password = cd['password'])
			if user is not None:
				if user.is_active and user.profile.teacher == True:
					login(request, user)
					return redirect(reverse('courses:manage_course_list'))
				else:
					return redirect(reverse('account:login'))
			
	else:
		form = LoginForm()

	return render(request, 'registration/courseslogin.html', {'form': form })