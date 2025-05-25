from django.core.management.base import BaseCommand
from api.scraper import scrape_computrabajo

class Command(BaseCommand):
    help = 'Scrape job offers from various job boards'

    def add_arguments(self, parser):
        parser.add_argument('--keyword', type=str, default='desarrollador', help='Keyword to search for')
        parser.add_argument('--location', type=str, default='bogota', help='Location to search in')

    def handle(self, *args, **options):
        keyword = options['keyword']
        location = options['location']
        
        self.stdout.write(f'Starting job scraping for {keyword} in {location}...')
        
        try:
            jobs_count = scrape_computrabajo(keyword, location)
            self.stdout.write(self.style.SUCCESS(f'Successfully scraped {jobs_count} jobs'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scraping jobs: {str(e)}'))
