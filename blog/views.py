from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views import generic
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from blog import forms
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import FormView
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import FormView
from blog.forms import ContactForm

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "index.html"
    paginate_by = 2


class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"

# class blog(generic.ListView):
#     queryset = models.Entry.objects.published()
#     template_name = "blog.html"
#     paginate_by = 2
#
#     context_dict['object_list'] = queryset
#     return render_to_response(template_name, context_dict)

# def contact(request):
#     return render(request, 'contact.html')


def cv(request):
    return render(request, "cv.html")

def forms(request):
    return render(request, "contact.html")

def blog(request):
    context_dict = {}
    # queryset = models.Entry.objects.published()
    template_name = "blog.html"
    paginate_by = 2

    # context_dict['object_list'] = queryset


    blog_list = models.Entry.objects.published()
    paginator = Paginator(blog_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)
    # context_dict['paginator'] = paginator

    context_dict['object_list'] = blogs

    return render_to_response("blog.html", context_dict)

class ContactFormView(FormView):

    form_class = ContactForm
    template_name = "template/forms.html"
    success_url = '/email-sent/'

    def form_valid(self, form):
        message = "{name} / {email} said: ".format(
            name=form.cleaned_data.get('name'),
            email=form.cleaned_data.get('email'))
        message += "\n\n{0}".format(form.cleaned_data.get('message'))
        send_mail(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            from_email='mencher@gmail.com',
            recipient_list=[settings.LIST_OF_EMAIL_RECIPIENTS],
        )
        return super(ContactFormView, self).form_valid(form)
