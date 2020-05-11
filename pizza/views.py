from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from .models import Pizza
from .forms import PizzaForm
import datetime

class PizzaIndex(generic.ListView):
	template_name = "pizza/index.html"
	context_object_name = "pizzas"

	def get_context_data(self, **kwargs):
		context = super(PizzaIndex, self).get_context_data(**kwargs)
		context['error_msg'] = "No pizzas avaliable at the moment."
		return context

	def get_queryset(self):
		return Pizza.objects.order_by('-pub_date')

class PizzaIndexFilter(PizzaIndex):
	def get_context_data(self, **kwargs):
		context = super(PizzaIndexFilter, self).get_context_data(**kwargs)
		context['error_msg'] = "No pizzas match the selected filter."
		return context

	def get_queryset(self):
		d_filter = self.kwargs['filter']
		return Pizza.objects.filter(pub_date__lte=timezone.now()).filter(pub_date__gte=timezone.now()-datetime.timedelta(days=d_filter)).order_by('-pub_date')

class PizzaDetails(generic.DetailView):
	model = Pizza
	template_name = "pizza/details.html"

	def get_context_data(self, **kwargs):
	    context = super(PizzaDetails, self).get_context_data(**kwargs)
	    pizza = get_object_or_404(Pizza, pk=self.kwargs['pk'])
	    context['toppings'] = [pizza.get_topping_1_display(), pizza.get_topping_2_display(), pizza.get_topping_3_display()]
	    return context

def home(request):
	return render(request, 'pizza/home.html')


def create_pizza(request):
	context = {}
	if request.method == "POST":
		form = PizzaForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			name = data.get('name')
			c_name = data.get('creator_name')
			t1 = data.get('topping_1')
			t2 = data.get('topping_2')
			t3 = data.get('topping_3')
			size = data.get('size')
			cooking = data.get('cooking')
			pizza = Pizza.objects.create(name=name, creator_name=c_name, topping_1=t1, topping_2=t2, topping_3=t3, size=size, cooking=cooking)
			return redirect('pizza:pizza_index')
		else:
			context['error'] = "The form is not valid. Please, try again"
	else:
		form = PizzaForm()
		context['form'] = form

	return render(request, 'pizza/create.html', context)