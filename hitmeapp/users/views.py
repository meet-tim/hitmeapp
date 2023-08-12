from django.shortcuts import render,redirect
from django.contrib.auth import logout
from allauth.account.decorators import login_required
from .forms import ProductForm
from .models import Product,Best_Deals,Tags,Sponsored,Suggestion
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models.query import Q  
from datetime import datetime,timedelta
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_protect


def home(request):
    latest  = Product.objects.order_by('-date_posted')[0:5]
    lessthan100 = Product.objects.filter(price__lte = 100)
    deals  = Best_Deals.objects.all()[0:3]
    tags = Tags.objects.all()

    context={
        'latest':latest,
        'lessthan100':lessthan100,
        'tags':tags,
        'deals':deals,
    }
    return render(request,'users/index.html',context)

def search(request):
    query = request.GET.get('q')
    queryset = ''
    if query:
        queryset = Product.objects.filter(
        Q(name__icontains = query)|
        Q(location__icontains = query)|
        Q(price__icontains = query)|
        Q(category__icontains = query)|
        Q(desc__icontains = query)).distinct()
    tags = Tags.objects.all()
    paginator = Paginator(queryset, 6)
    page_var = 'page'
    page = request.GET.get(page_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'page_var':page_var,
        'products':paginated_queryset,
        'count':len(queryset),
        'count_of':len(paginated_queryset),
        'cat_name':query,
        'tags':tags,
    }
    return render(request,'users/product.html',context)

@login_required
def dashboard(request):
    products  = Product.objects.filter(owner_id=request.user.email)
    tags = Tags.objects.all()
    context = {
        'name':request.user,
        'products':products,
        'tags':tags,
        }
    return render(request,'users/dashboard.html',context)
    
@login_required
def addProduct(request):
    form = ProductForm()
    tags = Tags.objects.all()
    if request.method == 'POST':     
        form = ProductForm(request.POST,request.FILES)    
        if form.is_valid():
            form.instance.owner_id = request.user.email
            product = form.save()
            return redirect('dashboard')

    context = {
        'form':form,
        'name':request.user,
        'tags':tags,
    }
    return render(request,'users/addProduct.html',context)

def updateProduct(request, product_id):
    tags = Tags.objects.all()
    product = Product.objects.filter(owner_id=request.user.email).get(id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form =  ProductForm(request.POST or None, request.FILES or None,instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    context = {
        'form':form,
        'name':request.user,
        'tags':tags,
    }
    return render(request,'users/addProduct.html',context)

@csrf_protect
def deleteProduct(request, product_id):
    product = Product.objects.filter(owner_id=request.user.email).get(id=product_id)
    tags = Tags.objects.all()
    if request.method == 'POST':
        product.delete()
        return HttpResponse("Working succcessfully")

    context = {
        'item':product,
        'tags':tags,
    }
    return render(request,'accounts/delete.html',context)

def about(request):
    tags = Tags.objects.all()
    context = {
        'tags':tags,
    }
    return render(request,'users/about.html',context)

def products(request, cat_filter):
    tags = Tags.objects.all()
    products = Product.objects.filter(category__icontains=cat_filter)
    paginator = Paginator(products, 12)
    page_var = 'page'
    page = request.GET.get(page_var)
    
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'page_var':page_var,
        'products':paginated_queryset,
        'count':len(products),
        'count_of':len(paginated_queryset),
        'cat_name':cat_filter,
        'tags':tags,
    }
    return render(request,'users/product.html',context)


@login_required
def logout_view(request):
    logout(request)
    return render(request,'users/index.html')

#ajax views
def filterByAmount(request,category,amount):
    if amount == "lt100":
        filtered = Product.objects.filter(category=category).filter(price__lt=100)
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(price__lt=100)
        print(filtered)
    elif amount == "gt100":
        filtered = Product.objects.filter(category=category).filter(Q(price__gte= 100)&Q(price__lte= 199))
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(Q(price__gte= 100)&Q(price__lte= 199))
        print(filtered)
    elif amount == "gt200":
        filtered = Product.objects.filter(category=category).filter(Q(price__gte= 200)&Q(price__lte= 299))
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(Q(price__gte= 200)&Q(price__lte= 299))
        print(filtered)

    return JsonResponse({"filtered":list(filtered.values())})

def filterByTime(request,category,time):
    if time == "today":
        filtered = Product.objects.filter(category=category).filter(date_posted=datetime.today())
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(date_posted=datetime.today())
    elif time == "week":
        filtered = Product.objects.filter(category=category).filter(date_posted__gte=datetime.now()- timedelta(days=7))
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(date_posted__gte=datetime.now()- timedelta(days=7))
    elif time == "month":
        filtered = Product.objects.filter(category=category).filter(date_posted__gte=datetime.now()- timedelta(days=30))
        if not filtered:
            filtered = Product.objects.filter(name__icontains=category).filter(date_posted__gte=datetime.now()- timedelta(days=30))
        
    return JsonResponse({"filtered":list(filtered.values())})


def details(request,product_id):
    product = Product.objects.filter(pk=product_id)
    return JsonResponse({"product":list(product.values())})

def suggestion(request,msg):
    if not msg:
        raise ValueError
    else:
        m = Suggestion(message=msg)
        m.save()
    return HttpResponse("form submitted")
