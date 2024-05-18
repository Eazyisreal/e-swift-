from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils.email_utils import handle_email_subscription
from django.db.models import Q
from django.db.models import Max


def global_search(request):
    query = request.GET.get('query')
    results = { 'blogs': [], 'properties': [], 'projects': [], 'agents': []}

    if query:
        agent_results = Agent.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))
        results['agents'].extend(agent_results)
        blog_results = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        results['blogs'].extend(blog_results)
        property_results = Property.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
        results['properties'].extend(property_results)
        project_results = Project.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
        results['projects'].extend(project_results)
    any_results_found = any(results.values())
    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'global_search')
    context = {
        'query': query,
        'results': results,
        'form': form,
        'any_results_found': any_results_found 
    }
    return render(request, 'global_search.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def paginate_items(request, items, items_per_page):
    """
    Paginates a list of items based on the request and number of items per page.

    Args:
    - request: Django HttpRequest object.
    - items: QuerySet or list of items to paginate.
    - items_per_page: Number of items to display per page.

    Returns:
    - Paginated items (Page object).
    """
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items


def handle_email_subscription(request, form, redirect_url):
    if form.is_valid():
        email = form.cleaned_data['email']
        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed.')
        else:
            subscription = NewsletterSubscription(email=email)
            subscription.save()
            messages.success(request, 'Your subscription has been successful!')
    return redirect(redirect_url)


def home(request):
    blogs = Blog.objects.all().order_by('-id')
    agents = Agent.objects.all().order_by('-id')[:3]
    recent_projects = Project.objects.all().order_by('-created')[:3]
    recent_properties = Property.objects.all().order_by('-created')[:3]
    first_property = recent_properties[0] if recent_properties else None
    second_property = recent_properties[1] if len(
        recent_properties) > 1 else None
    third_property = recent_properties[2] if len(
        recent_properties) > 2 else None
    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    context = {
        'recent_projects':  recent_projects,
        'recent_properties':  recent_properties,
        'first_property': first_property,
        'second_property': second_property,
        'third_property': third_property,
        'form': form,
        'agents': agents,
        "blogs": blogs,
    }
    return render(request, 'home.html', context)


def about(request):
    staffs = Staff.objects.all().order_by('-id')
    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'about')
    context = { 'form': form, 'staffs': staffs}
    return render(request, 'about.html', context)


def blog(request):
    form = NewsletterSubscriptionForm()
    blogs = Blog.objects.all().order_by('-id')
    search_query= request.GET.get('query')
    results = None
    if search_query:
        results = blogs.filter(title__icontains=search_query) | blogs.filter(description__icontains=search_query) | blogs.filter(category__icontains=search_query)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'blog')
    context = {
        "search_query": search_query,
        'results': results,
        "form": form,
        "blogs": blogs
    }
    return render(request, 'blog.html', context)


def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug) 
    similar_blogs = Blog.objects.filter(category=blog.category).exclude(slug=slug)[:3] 

    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            handle_email_subscription(request, form, 'blog_details')
    
    context = {
        'blog': blog,
        'similar_blogs': similar_blogs,
        'form': form,
    }
    return render(request, 'blog_details.html', context)



def project(request, category_name=None):
    form = NewsletterSubscriptionForm()
    projects = Project.objects.all().order_by('-id')
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    blocks = request.GET.get('blocks')
    floor = request.GET.get('floor')
    rooms = request.GET.get('rooms')
    results = None
    categories = Project_Category.objects.all()
    
    # Filter projects by category if category_name is provided
    if category_name:
        category_obj = get_object_or_404(Project_Category, name=category_name)
        projects = projects.filter(category=category_obj)

    max_blocks = str(projects.aggregate(Max('no_of_block'))['no_of_block__max'])
    max_floors = str(projects.aggregate(Max('no_of_floors'))['no_of_floors__max'])
    max_rooms = str(projects.aggregate(Max('no_of_flat'))['no_of_flat__max'])

    if keyword:
        projects = projects.filter(title__icontains=keyword)
    if location:
        projects = projects.filter(location__icontains=location)
    if blocks:
        projects = projects.filter(no_of_block=blocks)
    if floor:
        projects = projects.filter(no_of_floors=floor)
    if rooms:
        projects = projects.filter(no_of_flat=rooms)

    results = projects
    paginated_projects = paginate_items(request, projects, items_per_page=9)

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')

    context = {
        'paginated_projects': paginated_projects,
        "form": form,
        'results': results,
        'categories': categories,
        'selected_category': category_name,
        'max_blocks': max_blocks,
        'max_floors': max_floors,
        'max_rooms': max_rooms,
    }
    return render(request, 'project.html', context)
def project_details(request, project_slug, category_name=None):
    form = NewsletterSubscriptionForm()
    contact_form = ProjectContactForm()
    review_form = ReviewForm()
    project = get_object_or_404(Project, slug=project_slug)
    available_projects = Project.objects.all().order_by('-id')
    if category_name:
        category = get_object_or_404(Project_Category, name=category_name)
        projects = Project.objects.filter(category=category)
    else:
        projects = [project]
    paginated_projects = paginate_items(request, projects, items_per_page=9)
    if request.method == 'POST':
        contact_form = ProjectContactForm(request.POST)
        project_instance = get_object_or_404(Project, slug=project_slug)
        if contact_form.is_valid():
                contact_message = ProjectContactMessage.objects.create(
                    project= project_instance,
                    name=contact_form.cleaned_data['name'],
                    email=contact_form.cleaned_data['email'],
                    phone=contact_form.cleaned_data['phone_number'],
                    message=contact_form.cleaned_data['message']
                )
                contact_message.save()
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('project_details', project_slug=project_slug)
    else:
        contact_form = ProjectContactForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                review_message = Project_Review(
                    project=project,
                    user=request.user,
                    comment=review_form.cleaned_data['comment']
                )
                review_message.save()
                messages.success(request, 'Your review has been submitted successfully!')
                return redirect('project_details', project_slug=project_slug)
                
            else:
                messages.warning(request, 'Please login to submit a review.')
        else:
            review_form = ReviewForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    images = project.projectimage_set.all()
    context = {
        'available_projects': available_projects,
        'project': project,
        'projects': paginated_projects,
        'images': images,
        'selected_category': category_name,
        'form': form,
        'review_form': review_form,
        'contact_form': contact_form,
        'project_slug': project_slug,
    }
    return render(request, 'project_details.html', context)



def properties(request, category_name=None):
    form = NewsletterSubscriptionForm()
    properties = Property.objects.all().order_by('-id')
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    bedrooms = request.GET.get('bedrooms')
    floor = request.GET.get('floor')
    bathrooms = request.GET.get('bathrooms')
    results = None
    categories = Property_Category.objects.all()
    if category_name:
        category_obj = get_object_or_404(Property_Category, name=category_name)
        properties = properties.filter(category=category_obj)

    max_bedrooms = str(properties.aggregate(Max('no_of_bedrooms'))['no_of_bedrooms__max'])
    max_floors = str(properties.aggregate(Max('no_of_floors'))['no_of_floors__max'])
    max_bathrooms = str(properties.aggregate(Max('no_of_bathrooms'))['no_of_bathrooms__max'])

    if keyword:
        properties = properties.filter(title__icontains=keyword)
    if location:
        properties = properties.filter(location__icontains=location)
    if bedrooms:
        properties = properties.filter(no_of_bedrooms=bedrooms)
    if floor:
        properties = properties.filter(no_of_floors=floor)
    if bathrooms:
        properties = properties.filter(no_of_bathrooms=bathrooms)

    results = properties
    paginated_properties = paginate_items(
        request, properties, items_per_page=9)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'properties')
    context = {
        'paginated_properties': paginated_properties,
        "form": form,
        'results': results,
        'categories': categories,
        'selected_category': category_name,
        'max_bedrooms': max_bedrooms,
        'max_floors': max_floors,
        'max_bathrooms': max_bathrooms,

    }
    return render(request, 'properties.html', context)


def properties_details(request, property_slug=None):
    form = NewsletterSubscriptionForm()
    review_form = ReviewForm()
    inspection_form = InspectionBookingForm() 
    available_properties = Property.objects.all().order_by('-id')
    properties = get_object_or_404(Property, slug=property_slug)
    paginated_properties = paginate_items(request, available_properties, items_per_page=9)
    images = properties.propertyimage_set.all()
    agents = properties.associated_agent.all()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    if request.method == 'POST':
            inspection_form = InspectionBookingForm(request.POST)
            if inspection_form.is_valid():
                property_instance = get_object_or_404(Property, slug=property_slug)
                inspection_booking = InspectionBooking.objects.create(
                    property=property_instance,
                    name=inspection_form.cleaned_data['name'],
                    phone=inspection_form.cleaned_data['phone_number'],
                    email=inspection_form.cleaned_data['email'],
                    message=inspection_form.cleaned_data['message'],
                )
                inspection_booking.save()
                messages.success(request, 'Your inspection booking has been submitted successfully! We will get back to you soon.')
                return redirect('properties_details', property_slug=property_slug)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                review_message = Property_Review(
                    properties=properties,
                    user=request.user,
                    comment=form.cleaned_data['comment']
                )
                review_message.save()
                messages.success(request, 'Your review has been submitted successfully!')
                return redirect('properties_details', property_slug=property_slug)
                
            else:
                messages.warning(request, 'Please login to submit a review.')
        else:
            review_form = ReviewForm()
    context = {
        'available_properties': available_properties,
        'properties': properties,
        'images': images,
        'agents': agents,
        'form': form,
        'review_form': review_form,
        'inspection_form': inspection_form,
        'property_slug': property_slug,
        'paginated_properties': paginated_properties,
    }
    return render(request, 'properties_details.html', context)



def contact(request):
    form = NewsletterSubscriptionForm()
    contact_form = ContactForm()

    if request.method == 'POST':
        if 'form' in request.POST:
            form = NewsletterSubscriptionForm(request.POST)
            if form.is_valid():
                handle_email_subscription(request, form, 'contact')
        else:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_message = ContactMessage.objects.create(
                    name=contact_form.cleaned_data['name'],
                    email=contact_form.cleaned_data['email'],
                    phone=contact_form.cleaned_data['phone_number'],
                    subject=contact_form.cleaned_data['subject'],
                    message=contact_form.cleaned_data['message']
                )
                contact_message.save()
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('contact')

    return render(request, 'contact.html', { 'form': form, "contact_form": contact_form})

 