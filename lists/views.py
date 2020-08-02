from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})
    

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def my_lists(request, email):
    user = User.objects.get(email=email)
    shared_lists = List.objects.all().filter(shared_with=user)
    return render(request, 'my_lists.html', {'owner': user, "shared_lists": shared_lists})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    sharee_email = request.POST['sharee']
    ##from https://simpleisbetterthancomplex.com/tips/2016/07/14/django-tip-6-get-or-create.html
    sharee, created = User.objects.get_or_create(email=sharee_email)
    list_.shared_with.add(sharee)
    return redirect(list_) ## from https://realpython.com/django-redirects/
    ##return redirect('view_list', list_.id) ##if get_absolute_url() wasn't defined in lists.models.List

