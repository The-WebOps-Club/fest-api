from django.core.management.base import BaseCommand, CommandError, NoArgsCommand


class Command(BaseCommand):
    help = 'Automatically adds an event participation object for every event.'

    def handle(self, arg=None, **options):
		from apps.events.models import Event, EventParticipation
		for e in Event.objects.all():
			if e.event_participated!=None:
				continue
			b=EventParticipation()
			b.event_for_participation=e
			b.save()
			print "added object for " + e.name

		self.stdout.write("Added a participation object for every event")

