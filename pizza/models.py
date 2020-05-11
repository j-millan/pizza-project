from django.db import models

class Pizza(models.Model):
	toppings_list = (
		('PEP', 'Pepperoni'),
		('MUS', 'Mushrooms'),
		('ONI', 'Onions'),
		('SAU', 'Sausage'),
		('BAC', 'Bacon'),
		('ECH', 'Extra Cheese'),
		('BOL', 'Black Olives'),
		('GPP', 'Green Peppers'),
		('CHO', 'Chocolate')
	)
	
	cooking_times = (
		('RW', 'Raw'),
		('MD', 'Medium'),
		('SK', 'Smoked')
	)

	name = models.CharField(max_length=55, unique=True)
	creator_name = models.CharField(max_length=75)
	topping_1 = models.CharField(max_length=5, choices=toppings_list)
	topping_3 = models.CharField(max_length=5, choices=toppings_list)
	topping_2 = models.CharField(max_length=5, choices=toppings_list)
	size = models.IntegerField()
	cooking = models.CharField(max_length=50, choices=cooking_times)
	pub_date = models.DateTimeField('date_published', auto_now_add=True)

	def __str__(self):
		return self.name