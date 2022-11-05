from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#     })


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {
#         "question": question
#     })


# # Vamos a llegar a esta vista después de que el usuario ejecute en la vista vote
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



# La vista vote recibe 2 parámetros (request y question_id que nos vienen de detail.html)
def vote(request, question_id):
    # Vamos a obtener la pregunta respectiva con el get_object_or_404 envíandole como parámetros Question y la PrimaryKey que contiene el question.id
    question = get_object_or_404(Question, pk=question_id)
    # Para obtener la respuesta del usuario hacermos un try/except (manejo de errores)
    try:
        # Si la respuesta existe va a pasar las cosas que están después del else y sino pasarán las cosas del except
        # Si el usuario ya voto, nosotros obtendremos esa elección mediante question.choice_set.get y si esto pasa se le agrega la aelección a la variable selected_choice y corre el else
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # Si la respuesta no existe o ocurre un error
    except (KeyError, Choice.DoesNotExist):
        # Retornaremos el resultado de la función render que lleva como parámetros un request, un template y como tercer parámetro un contexto en una llave con la pregunta "question" y también un error_mesage.  
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        # Si se eligió un choice correcto entonces se sumará un voto +1 a la respuesta elegida
        selected_choice.votes += 1
        # Y se guardará este voto en la base de datos
        selected_choice.save()
        # Por último y si todo salió bien retornamos redirigiendo al usuario a una URL con los resultados en este caso.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
