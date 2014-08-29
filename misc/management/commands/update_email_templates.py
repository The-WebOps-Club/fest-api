from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.conf import settings

#Email stuff
from django.template.loader import get_template
from django.utils.html import strip_tags

from post_office.models import EmailTemplate
import BeautifulSoup

import os

class Command(NoArgsCommand):
    help = 'Updates the emails for the post_office model from the templates.'

    def handle_noargs(self, **options):
        # Get the list of files in the email templates folder.
        email_root_path = settings.EMAIL_ROOT
        email_templates = [t for t in os.listdir(email_root_path) if t.endswith('.html')]

        # Get current templates from the database
        post_office_templates = EmailTemplate.objects.all()

        already_in_database = set()
        for template in post_office_templates:
            # Get the template name.
            this_email_template_name = template.name.replace('.email','.html')
            already_in_database.add(this_email_template_name)

            #Read the corresponding template from file. If it doesn't exist, move on.
            if not this_email_template_name in email_templates:
                self.stdout.write('Skipping %s - cannot find the template!' % template.name)
                continue
            self.stdout.write('Updating %s' % template.name)
            this_email_template = open(os.path.join(email_root_path, this_email_template_name), 'r').read()

            #Update content
            template.html_content = this_email_template
            soup = BeautifulSoup.BeautifulSoup(this_email_template)
            for l in soup.findAll('a'):
                if l.getString():
                    string = l.getString()
                else:
                    string = ""
                l.setString(string + u'( ' + l['href'] + ' )')
            template.content = strip_tags(str(soup)) #<---- Note: We can do soup.prettify() here instead of str(soup)
            #Update subject
            template.subject = open(os.path.join(email_root_path, this_email_template_name).replace('.html','.subject'), 'r').read()

            template.save()

        new_templates = set(email_templates) - already_in_database

        for template in new_templates:
            #Read the template:
            content = open(os.path.join(email_root_path, template),'r').read()

            new_template = EmailTemplate()

            new_template.name = template.replace('.html','.email')
            new_template.description = new_template.name.replace('.', ' ')
            new_template.subject = open(os.path.join(email_root_path, template).replace('.html','.subject'),'r').read()
            new_template.html_content = content
            soup = BeautifulSoup.BeautifulSoup(content)
            for l in soup.findAll('a'):
                if l.getString():
                    l.setString(l.getString() + u'( ' + l['href'] + ' )')
                else:
                    l.setString(u'( ' + l['href'] + ' )')
            for l in soup.findAll('li'):
                l.setString(u'- ' + l.getString())
            new_template.content = strip_tags(str(soup)) #<---- Note: We can do soup.prettify() here instead of str(soup)
            new_template.save()
            self.stdout.write('Adding %s' % template)

        self.stdout.write('All done. Check if everything is fine from the admin console. Wouldn\'t hurt!' )
