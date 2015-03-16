from django.shortcuts import render
from models import Entry
from forms import EntryForm
from django.template.defaultfilters import slugify

# Create your views here.



def test(request):
	msg='Hello there, this is a test of hitting the view'
	return render(request, 'api/test.html', {'message':msg})

def entry_view(request):
	entries = Entry.objects.order_by('title')
	return render(request, 'api/entry_list.html', {'entry':entries})

def create(request):
	if request.method == 'POST':
		form_data = EntryForm(request.POST)
		if form_data.is_valid():
			print >>sys.stderr, 'Valid form data'
		else:
			print >>sys.stderr, 'Invalid form data'
		blog=Entry()
		blog.title=form_data.cleaned_data['title']
		blog.body=form_data.cleaned_data['body']
		blog.user=form_data.cleaned_data['user']
		blog.pub_date=form_data.cleaned_data['pub_date']
		blog.slug = slugify(blog.title)
		blog.save()
		message='saved successfully'
		return render(request, 'api/test.html', {'message':message})
	else:
		form = EntryForm()
	return render(request, 'api/form.html', {'form':form})




def dummy(request):
	return render(request, 'api/dummy.html', {})
