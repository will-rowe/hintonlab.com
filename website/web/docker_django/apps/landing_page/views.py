from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import logout
from django.conf import settings
import datetime
from datetime import date, timedelta
from .models import UserProfile, UserForm, UserProfileForm, ResearchStrand, LabPublication, Carousel, Bioinformatics, Tools
from docker_django.apps.todo.models import Item
from docker_django.apps.databases.models import MEETINGS, NOTIFICATIONS, MUTANTS
from .forms import ContactForm, LabPublicationForm
from pubmed_lookup import PubMedLookup, Publication


###############################################################################
# Public pages
###############################################################################
def home(request):
    carousel = Carousel.objects.all().order_by('upload_date')
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            form = ContactForm()
            try:
                send_mail(subject, message, from_email, ['will.rowe@liverpool.ac.uk'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response = '<strong>Message success.</strong> Your message has been sent, we will respond as soon as possible.'
            return render(request, "landing_page/home.html", {'form': form, 'response': response, 'carousel': carousel})
        else:
            response = '<strong>Message failed.</strong> Please check the form and try sending your message again.'
            return render(request, "landing_page/home.html", {'form': form, 'response': response, 'carousel': carousel})
    return render(request, "landing_page/home.html", {'form': form, 'carousel': carousel})

def research(request):
    research = ResearchStrand.objects.all().order_by('upload_date')
    return render(request, 'public_pages/research.html', {'research': research})

def the_team(request):
    team = User.objects.filter(groups__name='lab').filter(is_active='True').order_by('date_joined')
    collaborators = User.objects.filter(groups__name='collaborators').order_by('date_joined')
    return render(request, 'public_pages/the-team.html', {'team': team, 'collaborators': collaborators})

def publications(request):
    publications = LabPublication.objects.all().order_by('-year')
    return render(request, 'public_pages/publications.html', {'publications': publications})

def tools(request):
    tools = Tools.objects.all().order_by('upload_date')
    return render(request, 'public_pages/tools.html', {'tools': tools})

@login_required
def pubmed_search(request):
    publications = LabPublication.objects.all().order_by('-year')
    if 'pubmed_id' in request.GET:
        paper_id = request.GET['pubmed_id']
        if not paper_id:
            message = '<strong>No PubMed ID or PubMed URL provided!</strong>'
        else:
            email = request.user.email
            url = paper_id
            try:
                lookup = PubMedLookup(url, email)
            except Exception:
                message = '<strong>Error using your PubMed ID/URL</strong>'
                return render(request, 'public_pages/publications.html', {'publications': publications, 'message': message})
            publication = Publication(lookup)
            if publication == '':
                message = '<strong>No match found for your pubmed ID</strong>'
                return render(request, 'public_pages/publications.html', {'publications': publications, 'message': message})
            user = request.user
            title = publication.title
            authors = publication.authors
            journal = publication.journal
            year = publication.year
            journal_url = publication.url
            pubmed = publication.pubmed_url
            citation = publication.cite()
            mini_citation = publication.cite_mini()
            abstract = repr(publication.abstract)
            try:
                new_publication, created = LabPublication.objects.get_or_create(user = user, title = title, authors = authors, journal = journal, year = year, journal_url = journal_url, pubmed = pubmed, citation = citation, mini_citation = mini_citation, abstract = abstract)
            except:
                message = '<strong>Could not add your publication. Are you trying to add a duplicate entry?</strong>'
                return render(request, 'public_pages/publications.html', {'publications': publications, 'message': message})
            if created == '':
                message = '<strong>Could not add your publication. Are you trying to add a duplicate entry?</strong>'
                return render(request, 'public_pages/publications.html', {'publications': publications, 'message': message})
            else:
                return HttpResponseRedirect('publications')
    return render(request, 'public_pages/publications.html', {'publications': publications, 'message': message})

def publication_detail(request, pk):
    publication = get_object_or_404(LabPublication, pk=pk)
    return render(request, 'public_pages/publication_detail.html', {'publication': publication})

@login_required
def edit_publication(request, pk):
    publication = get_object_or_404(LabPublication, pk=pk)
    if request.method == "POST":
        form = LabPublicationForm(request.POST or None, request.FILES or None, instance=publication)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.user = request.user
            if request.FILES:
                publication.pdf = request.FILES['pdf']
            try:
                publication.save()
            except:
                message = '<strong>Could not update publication entry</strong>'
                return render(request, 'public_pages/publications.html', {'message': message})
            return redirect('publication_detail', pk=publication.pk)
    else:
        form = LabPublicationForm(instance=publication)
    return render(request, 'public_pages/publication_edit.html', {'form': form, 'publication': publication})

@login_required
def remove_publication(request, pk):
    publication = get_object_or_404(LabPublication, pk=pk)
    publication.delete()
    return redirect('publications')


###############################################################################
# Member only pages
###############################################################################
@login_required
def member(request):
    admin, register, profile = 0, 0, 0
    user = request.user

    # if user is logged on with the admin account, get them to sign up for a new username
    if user.username == 'hinton.admin':
        admin = 1
        args = {}
        args.update(csrf(request))
        if request.method == 'POST':
            form = UserForm(request.POST)
            args['form'] = form
            if form.is_valid():
                user = form.save(commit=False)
                pw = user.password
                user.set_password(pw)
                email = user.email
                try:
                    user.save()
                except:
                    error = 'Could not save new user, contact Will.'
                    return render(request, 'landing_page/error.html', {'error': error})
                # Send email with activation info
                email_subject = 'Hinton Lab: website account confirmation'
                email_message = 'You\'ve just signed up to the Hinton Lab website.\n\n Username: {}\n\n Please now sign in to the website using your new user and then follow the instructions to create a profile.\n\nContact Will if you need any help.' .format(user)
                html_content = render_to_string("member/email.html", {'user': user, 'email_message': email_message})
                email_body = 'Hey {}, \n\n You\'ve just signed up to the Hinton Lab website.\n\n Username: {}\nContact Will if you need any help.' .format(user.first_name, user)
                try:
                    send_mail(email_subject, email_body, 'will.rowe@liverpool.ac.uk', [user.email, 'will.rowe@liveprool.ac.uk'], fail_silently=False, html_message=html_content)
                except:
                    error = 'Email confirmation error, contact Will.'
                    return render(request, 'landing_page/error.html', {'error': error})
                logout(request)
                return HttpResponseRedirect('/member')
        else:
            form = UserForm
        return render(request, 'member/member.html', {'form': form, 'admin': admin})

    # if the user doesn't have a profile, they need one!
    try:
        user.userprofile
    except:
        register = 1
        args = {}
        args.update(csrf(request))
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            args['form'] = form
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                try:
                    profile.save()
                except:
                    error = 'Could not save new user profile, contact Will.'
                    return render(request, 'landing_page/error.html', {'error': error})
                # Send email with activation info
                email_subject = 'Hinton Lab: your website profile'
                email_message = 'You\'ve just created your profile for the Hinton Lab website. This is now visible on the public pages.\n\nUsername: {}\n\nPosition: {}\n\nBio: {}\n\n\nContact Will if you need any help.' .format(user, profile.position, profile.bio)
                html_content = render_to_string("member/email.html", {'user': user, 'email_message': email_message})
                email_body = 'Hey {}, \n\n You\'ve just created your profile. This is now visible no the public pages.\n\n Username: {}\nContact Will if you need any help.' .format(user.first_name, user)
                try:
                    send_mail(email_subject, email_body, 'will.rowe@liverpool.ac.uk', [user.email, ], fail_silently=False, html_message=html_content)
                except:
                    error = 'Email confirmation error, contact Will.'
                    return render(request, 'landing_page/error.html', {'error': error})
                return HttpResponseRedirect('/member')
        else:
            form = UserProfileForm
        return render(request, 'member/member.html', {'up_form': form, 'register': register, 'admin': admin})

    # as long as they have their own account and a profile, they can view the member page
    else:
        profile = 1
        picture = settings.MEDIA_URL + str(request.user.userprofile.picture)
        position = request.user.userprofile.position
        bio = request.user.userprofile.bio
        #all_completed_tasks, submitted_tasks, task_lists = 0,0,0
    # return task data from todo app - starting with all completed tasks
        all_completed_tasks = Item.objects.filter(completed=True).order_by('-completed_date')
    # tasks recently submitted by user
        submitted_tasks = Item.objects.filter(created_by=user).order_by('-created_date')
    # get all tasks, find out list name and then count items in each list
        tasks = Item.objects.all()
        task_lists = {}
        for task in tasks:
            if task.list in task_lists:
                next;
            else:
                task_lists.update({task.list:0})
            if task.list in task_lists:
                task_lists[task.list] += 1
    # get all notifications
        notifications = NOTIFICATIONS.objects.all()
    # get all meetings, return this weeks meeting
        current_date = date.today()
        future_date = current_date + timedelta(days=7)
        next_meeting = MEETINGS.objects.filter(DATE__range=[current_date, future_date]).order_by('DATE')
        return render(request, 'member/member.html', {'user': user, 'profile': profile, 'admin': admin, 'picture': picture, 'position': position, 'bio': bio, 'completed_tasks': all_completed_tasks, 'submitted_tasks': submitted_tasks, 'task_lists': task_lists, 'notifications': notifications, 'next_meeting': next_meeting})


@login_required
def edit_profile(request):
    if request.method == "POST":
        edit_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if edit_profile_form.is_valid():
            user = request.user
            profile = edit_profile_form.save(commit=False)
            profile.user = user
            try:
                profile.save()
            except:
                error = 'Could not edit user profile, contact Will.'
                return render(request, 'landing_page/error.html', {'error': error})
            return HttpResponseRedirect('/member')
    else:
        edit_profile_form = UserProfileForm(instance=request.user)
    return render(request, 'member/edit-profile.html', {'form': edit_profile_form})


@login_required
def analysis(request):
    jobs = Bioinformatics.objects.all().order_by('-created_date')
    return render(request, 'member/analysis.html', {'jobs': jobs})
