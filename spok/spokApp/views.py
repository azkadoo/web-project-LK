from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SPOKChallenge, SPOKSession
from .forms import SPOKForm



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user_sessions = SPOKSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'sessions': user_sessions})


@login_required
def spok_game(request):
    challenge = SPOKChallenge.objects.order_by('?').first()  # Ambil tantangan acak
    form = SPOKForm()

    if request.method == "POST":
        form = SPOKForm(request.POST)
        if form.is_valid():
            answers = {
                'subject': form.cleaned_data['subject'],
                'predicate': form.cleaned_data['predicate'],
                'object': form.cleaned_data['object'],
                'description': form.cleaned_data.get('description', '')
            }
            correct_answers = {
                'subject': challenge.subject,
                'predicate': challenge.predicate,
                'object': challenge.object,
                'description': challenge.description
            }

            # Hitung skor
            score = 0
            for key in answers:
                if answers[key].lower() == correct_answers[key].lower():
                    score += 5

            # Simpan sesi permainan
            session = SPOKSession.objects.create(
                user=request.user,
                challenge=challenge,
                score=score
            )
            return redirect('spok_result', session_id=session.id)

    return render(request, 'spok_game.html', {'challenge': challenge, 'form': form})

@login_required
def spok_result(request, session_id):
    session = get_object_or_404(SPOKSession, id=session_id)
    return render(request, 'spok_result.html', {'session': session})




# @login_required
# def spok_game(request):
#     if request.method == 'POST':
#         subject = request.POST.get('subject', '').strip()
#         predicate = request.POST.get('predicate', '').strip()
#         obj = request.POST.get('object', '').strip()
#         complement = request.POST.get('complement', '').strip()

#         correct_answers = {
#             "subject": ["kancil"],
#             "predicate": ["memakan"],
#             "object": ["timun"],
#             "complement": ["di hutan"]
#         }

#         score = 0
#         if subject in correct_answers['subject']:
#             score += 5
#         if predicate in correct_answers['predicate']:
#             score += 5
#         if obj in correct_answers['object']:
#             score += 5
#         if complement in correct_answers['complement']:
#             score += 5

#         session = GameSPOKSession.objects.create(
#             user=request.user,
#             example_sentence="Kancil memakan timun di hutan",
#             subject=subject,
#             predicate=predicate,
#             object=obj,
#             complement=complement,
#             score=score
#         )
#         return redirect('spok_result', session_id=session.id)

#     return render(request, 'spok_game.html', {
#         'example_sentence': "Kancil memakan timun di hutan",
#         'tags': ["kancil", "memakan", "timun", "di hutan"]
#     })


# @login_required
# def spok_result(request, session_id):
#     session = GameSPOKSession.objects.get(id=session_id, user=request.user)
#     return render(request, 'spok_result.html', {'session': session})
