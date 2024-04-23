from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils.email_utils import handle_email_subscription


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
    }
    return render(request, 'home.html', context)


def about(request):
    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    return render(request, 'about.html', {"form": form})


def blog(request):
    form = NewsletterSubscriptionForm()
    blogs = Blog.objects.all()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    return render(request, 'blog.html', {"form": form, "blogs": blogs})


def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)  # Get the specific blog
    similar_blogs = Blog.objects.filter(category=blog.category).exclude(slug=slug)[:3]  # Example to get similar blogs

    form = NewsletterSubscriptionForm()
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            # Assuming you have a function to handle email subscriptions
            handle_email_subscription(request, form, 'blog_details')
    
    context = {
        'blog': blog,
        'similar_blogs': similar_blogs,
        'form': form,
    }
    return render(request, 'blog_details.html', context)



def project(request):
    form = NewsletterSubscriptionForm()
    
    projects = Project.objects.all().order_by('-id')
    paginated_projects = paginate_items(request, projects, items_per_page=9)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    context = {
        'paginated_projects': paginated_projects,
        "form": form
    }
    return render(request, 'project.html', context)


def project_details(request, project_slug, category_name=None):
    form = NewsletterSubscriptionForm()
    inspection_form = InspectionBookingForm()
    
    available_projects = Project.objects.all().order_by('-id')
    project = get_object_or_404(Project, slug=project_slug)
    images = project.projectimage_set.all()

    if category_name:
        category = get_object_or_404(Project_Category, name=category_name)
        projects = Project.objects.filter(category=category)
    else:
        projects = [project]

    paginated_projects = paginate_items(request, projects, items_per_page=9)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form)
    context = {
        'available_projects': available_projects,
        'project': project,
        'projects': paginated_projects,
        'images': images,
        'selected_category': category_name,
        "form": form,
        "inspection_form": inspection_form

    }
    return render(request, 'project_details.html', context)


def properties(request):
    form = NewsletterSubscriptionForm()
    
    properties = Property.objects.all().order_by('-id')
    paginated_properties = paginate_items(
        request, properties, items_per_page=9)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        handle_email_subscription(request, form, 'home')
    context = {
        'paginated_properties': paginated_properties,
        "form": form

    }
    return render(request, 'properties.html', context)


def properties_details(request, property_slug):
    form = NewsletterSubscriptionForm()
    inspection_form = InspectionBookingForm() 
    available_properties = Property.objects.all().order_by('-id')
    properties = get_object_or_404(Property, slug=property_slug)
    images = properties.propertyimage_set.all()
    agents = properties.associated_agent.all()

    if request.method == 'POST':
        if 'newsletter_form' in request.POST:
            form = NewsletterSubscriptionForm(request.POST)
            if form.is_valid():
                handle_email_subscription(request, form, 'home')
        elif 'inspection_form' in request.POST:
            inspection_form = InspectionBookingForm(request.POST)
            if inspection_form.is_valid():
                inspection_booking = InspectionBooking.objects.create(
                    name=inspection_form.cleaned_data['name'],
                    phone=inspection_form.cleaned_data['phone_number'],
                    email=inspection_form.cleaned_data['email'],
                    message=inspection_form.cleaned_data['message'],
                )
                messages.success(request, 'Your inspection booking has been submitted successfully! We will get back to you soon.')
                return redirect('properties_details', property_slug=property_slug)

    context = {
        'available_properties': available_properties,
        'properties': properties,
        'images': images,
        'agents': agents,
        'form': form,
        'inspection_form': inspection_form,
        'property_slug': property_slug,
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

