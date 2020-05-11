from django import forms
from.models import Pizza

class PizzaForm(forms.ModelForm):
	topping_1 = forms.ChoiceField(choices=Pizza.toppings_list)
	topping_2 = forms.ChoiceField(choices=Pizza.toppings_list)
	topping_3 = forms.ChoiceField(choices=Pizza.toppings_list)
	cooking = forms.CharField(max_length=50, label='Cooking time', widget=forms.Select(choices=Pizza.cooking_times))

	class Meta:
		model = Pizza
		fields = ['name', 'creator_name', 'size', 'topping_1', 'topping_2', 'topping_3', 'cooking']