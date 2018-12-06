from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Note
from .forms import NoteForm
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Profile
# Create your views here.

def all_notes(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    all_notes = Note.objects.filter(user=user)
    context = {
        'all_notes' : all_notes,
        'profile':profile
    }
    return render(request, 'notes.html', context)

def detail(request, slug):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    note = Note.objects.get(slug = slug)
    context = {
        'note' : note,
        'profile':profile

    }
    return render(request, 'one-note.html', context)

def note_add(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, 'Note Added successfully.')
            return redirect('/Notes')

    else:
        form = NoteForm()

    context = {
        'form' : form,
        'profile':profile
    }
    return render(request, 'add.html', context)


def edit(request, slug):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    note = get_object_or_404(Note, slug = slug)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance = note)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('/Notes')

    else:
        form = NoteForm(instance = note)

    context = {
        'form' : form,
        'profile':profile
    }
    return render(request, 'edit.html', context)
