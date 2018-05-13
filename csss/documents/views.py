from django.shortcuts import render
from django.http import HttpResponseRedirect
from documents.forms import ContactForm
from django.views.generic import TemplateView

def index(request):
	print("constitution index")
	return render(request, 'documents/constitution.html')

def policies(request):
	print("policies index")
	return render(request, 'documents/policies.html')

class FormView(TemplateView):
  template_name = 'documents/photo_gallery.html'

  def get(self, request):
    form = ContactForm()
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    form = ContactForm(request.POST)
    if form.is_valid():
      text = form.cleaned_data['post']
      print("text=["+str(text)+"]")
      form = ContactForm()
      print("form=["+str(form)+"]")
      return redirect('document:document')

    return render(request, self.template_name, {'form': form})

def photos(request):
	print("photo gallery index")
	return render(request, 'documents/photo_gallery.html')
# Create your views here.
