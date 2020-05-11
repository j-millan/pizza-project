from django.test import TestCase
from django.urls import reverse, resolve
from .models import Pizza
from .views import home, create_pizza
from .forms import PizzaForm

def create_p(name, creator, size, top):
	t1 = top[0]
	t2 = top[1]
	t3 = top[2]
	return Pizza.objects.create(name=name, creator_name=creator, topping_1=t1, topping_2=t2, topping_3=t3, size=size, cooking='SK')

class HomeViewTests(TestCase):
	def setUp(self):
		url = reverse('pizza:home')
		self.response = self.client.get(url)

	def test_success_status_code(self):		
		self.assertEquals(self.response.status_code, 200)

	def test_url_returns_correct_view(self):
		view = resolve('/pizza/home/')
		self.assertEquals(view.func, home)

	def test_contains_navigation_links(self):
		index_url = reverse('pizza:pizza_index')
		create_url = reverse('pizza:create_pizza')
		self.assertContains(self.response, 'href="{0}"'.format(index_url))
		self.assertContains(self.response, 'href="{0}"'.format(create_url))

class IndexViewTests(TestCase):
	def test_view_shows_right_pizzas(self):
		create_p('Pizza Party', 'pizza', 120, ['CHO', 'ONI', 'SAU'])
		url = reverse('pizza:pizza_index')
		response = self.client.get(url)
		self.assertQuerysetEqual(response.context.get('pizzas'), ['<Pizza: Pizza Party>'])

	def test_view_no_pizzas_yet(self):
		url = reverse('pizza:pizza_index')
		response = self.client.get(url)
		self.assertContains(response, 'No pizzas have been created yet.')
		self.assertQuerysetEqual(response.context.get('pizzas'), [])

	def test_view_contains_navigation_links(self):
		create_p('Pizza Party', 'pizza', 40, ['CHO', 'ONI', 'SAU'])
		pizza_url = reverse('pizza:pizza_details', kwargs={'pk': 1})
		home_url = reverse('pizza:home')
		create_url = reverse('pizza:create_pizza')
		response = self.client.get(reverse('pizza:pizza_index'))
		self.assertContains(response, 'href="{0}"'.format(pizza_url))
		self.assertContains(response, 'href="{0}"'.format(home_url))
		self.assertContains(response, 'href="{0}"'.format(create_url))

	def test_view_contains_creator_name_and_publication_date(self):
		piz = create_p('Pizza Party', 'Millan', 3, ['CHO', 'MUS', 'BOL'])
		url = reverse('pizza:pizza_index')
		response = self.client.get(url)
		self.assertContains(response, piz.pub_date.strftime('%B %d, %Y'))

class TestPizzaDetailsView(TestCase):
	def test_success_status_code(self):
		create_p("Pizza", "Hola", 50, ['CHO', 'CHO', 'CHO'])
		url = reverse('pizza:pizza_details', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
	
	def test__status_code_not_found(self):
		create_p("Pizza", "Hola", 50, ['CHO', 'CHO', 'CHO'])
		url = reverse('pizza:pizza_details', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_view_contains_creator_name_and_publication_date(self):
		piz = create_p('Pizza Party', 'Millan', 3, ['CHO', 'MUS', 'BOL'])
		url = reverse('pizza:pizza_details', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertContains(response, 'Created by: {0}'.format(piz.creator_name))
		self.assertContains(response, 'Published at: {0}'.format(piz.pub_date.strftime('%B %d, %Y, %I:%M %p')))

class TestPizzaCreationForm(TestCase):
	def setUp(self):
		url = reverse('pizza:create_pizza')
		self.response = self.client.get(url)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')
	
	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, PizzaForm)
	
	def test_new_pizza_valid_form_data(self):
		url = reverse('pizza:create_pizza')
		data = {
			'name': 'Pizza',
			'creator_name': 'BakerBoss',
			'size': '70',
			'topping_1': 'CHO',
			'topping_2': 'ECH',
			'topping_3': 'PEP',
			'cooking': 'RW'
		}

		response = self.client.post(url, data)
		self.assertTrue(Pizza.objects.exists())
	
	def test_new_pizza_invalid_form_data_empty_fields(self):
		url = reverse('pizza:create_pizza')
		data = {
			'name': '',
			'creator_name': '',
			'size': '',
			'topping_1': '',
			'topping_2': '',
			'topping_3': '',
			'cooking': ''
		}

		response = self.client.post(url, data)
		self.assertFalse(Pizza.objects.exists())