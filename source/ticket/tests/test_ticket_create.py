from django.test import TestCase, Client
from django.urls import reverse

from ticket.models import ServiceLevel, Department
from ticket.models.ticket import User, TicketStatus, TicketPriority, TicketType, Work, ProblemArea, Ticket


class TicketTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # создаем пользователя
        operator = User.objects.create_user(username='operator', password='operator123')
        operator.save()

        # создаем статус заявки
        status = TicketStatus.objects.create(name='Неопределенный')
        status.save()

        # создаем приоритет заявки
        priority = TicketPriority.objects.create(name='Средний')
        priority.save()

        # создаем тип заявки
        type_ = TicketType.objects.create(name='Профилактика')
        type_.save()

        # создаем уровень обслуживания
        service_level = ServiceLevel.objects.create(name='First level maintenance')
        service_level.save()

        # создаем департамент
        department = Department.objects.create(name='Service Department')
        department.save()

        # создаем работу
        works = Work.objects.create(name='Демонтаж')
        works.save()

        # создаем проблемные области
        problem_areas = ProblemArea.objects.create(name='Printers')
        problem_areas.save()

        # создаем саму заявку
        test_ticket = Ticket.objects.create(operator=operator,
                                            description='some description...',
                                            status=status,
                                            priority=priority,
                                            type=type_,
                                            service_level=service_level,
                                            department=department, )
        test_ticket.works.add(works)
        test_ticket.problem_areas.add(problem_areas)
        test_ticket.save()

    def test_ticket_content(self):
        ticket = Ticket.objects.get(id=1)
        operator = f'{ticket.operator}'
        description = f'{ticket.description}'
        status = f'{ticket.status}'
        priority = f'{ticket.priority}'
        type_ = f'{ticket.type}'
        service_level = f'{ticket.service_level}'
        department = f'{ticket.department}'
        works = f'{ticket.works.all()}'
        problem_areas = f'{ticket.problem_areas.all()}'
        self.assertEqual(operator, 'operator')
        self.assertEqual(description, 'some description...')
        self.assertEqual(status, 'Неопределенный')
        self.assertEqual(priority, 'Средний')
        self.assertEqual(type_, 'Профилактика')
        self.assertEqual(service_level, 'First level maintenance')
        self.assertEqual(department, 'Service Department')
        self.assertIn('Демонтаж', works)
        self.assertIn('Printers', problem_areas)

    def test_ticket_list_view_not_authenticated_user(self):
        response = self.client.get(reverse('ticket:ticket_list'))
        self.assertEqual(response.status_code, 302)  # 302 потому что нас должно перенаправить на страницу входа

    def test_ticket_list_view_authenticated_user(self):
        client = Client()
        client.login(username='operator', password='operator123')
        response = client.get(reverse('ticket:ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неопределенный')  # так как мы выводим статус заявки в списке заявок
        self.assertTemplateUsed(response, 'ticket/list.html')
