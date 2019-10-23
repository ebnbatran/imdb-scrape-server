import os
import logging
from datetime import date
import psycopg2 as pg
from django.http import HttpResponse


DATABASE_URL = os.environ['DATABASE_URL']
logger = logging.getLogger("django")

def get_movies():
	logger.info(f'Connecting to database: {DATABASE_URL} ...')
	connection = pg.connect(DATABASE_URL)
	
	if connection:
		logger.info('Success.')
	else:
		logger.error('Failed!')
	
	cursor = connection.cursor()
	
	sql = "SELECT * FROM server_movie;"
	
	cursor.execute(sql)
	movies = cursor.fetchall()
	
	if movies:
		logger.info('Got movies.')
	else:
		logger.error('Failed to retrieve movies!')

	cursor.close()
	connection.close()

	return movies


def correct(value):
	value = value.strip()
	
	if '"' in value:
		value = value.replace('"', '*')
	elif "'" in value:
		value = value.replace("'", '_')

	return value


def home(request):
	logger.info('Getting movies ...')
	movies = get_movies()

	count = len(movies)
	
	if count > 0:
		counter = 0
		
		data = "["

		for movie in movies:
			counter += 1
			ID, title, url, year, rating, synopsis, image = movie

			title = correct(title)
			url = correct(url)
			rating = correct(rating)
			synopsis = correct(synopsis)
			image = correct(image)

			data += '{'
			data += f'"id": "{ID}", '
			data += f'"title": "{title}", '
			data += f'"url": "{url}", '
			data += f'"year": "{year}", '
			data += f'"rating": "{rating}", '
			data += f'"synopsis": "{synopsis}", '
			data += f'"image": "{image}"'
			data += '}'
			
			if counter < count:
				data += ', '

		data += "]"

		return HttpResponse(data, content_type="application/json")

	return HttpResponse('<h1>No data yet</h1>', status=404)


def get_dates():
	logger.info(f'Connecting to database: {DATABASE_URL}')
	connection = pg.connect(DATABASE_URL)

	if connection:
		logger.info('Success')
	else:
		logger.error('Failed!')

	cursor = connection.cursor()
	
	sql = "SELECT * FROM server_scrapedate;"
	
	cursor.execute(sql)
	dates = cursor.fetchall()

	if dates:
		logger.info('Got dates.')
	else:
		logger.error('Failed to get dates!')

	cursor.close()
	connection.close()

	return dates

def check_date():
	logger.info('Getting dates ...')
	dates = get_dates()
	count = len(dates)

	if count > 0:
		last_one = dates[count - 1]
		last_date = last_one[1]
		stored_date = date.fromisoformat(last_date)
	else:
		return True

	today = date.today()
	delta = today - stored_date

	if int(delta.days) >= 7:
		return True
	
	return False


def scrape():
	os.chdir('scrape_imdb/')
	logger.info('Started scraping ...')
	os.spawnlp(os.P_NOWAIT, 'scrapy', 'scrapy', 'crawl', 'imdb')
	os.chdir('../')


def register_date():
	logger.info(f'Connecting to database: {DATABASE_URL}')
	connection = pg.connect(DATABASE_URL)
	
	if connection:
		logger.info('Success.')
	else:
		logger.error('Failed to connect to database!')

	cursor = connection.cursor()
	
	sql = "INSERT INTO server_scrapedate (date) VALUES ("
	sql += f"'{date.today().isoformat()}'"
	sql += ");"
	
	cursor.execute(sql)
	logger.info('Registering date ...')
	connection.commit()
	logger.info('Success.')
	
	cursor.close()
	connection.close()


def do_scrape(request):
	if check_date():
		scrape()
		register_date()
		return HttpResponse('Scraping ...')
	else:
		return HttpResponse('Not for another week', status=400)


def search(request):
	if request.method != 'GET':
		return HttpResponse(status=400)
	
	phrase = request.GET['title']
	movies = get_movies()
	count = 0

	for movie in movies:
		title = movie[1]
		if phrase.lower() in title.lower():
			count += 1

	if count == 0:
		return HttpResponse(status=404)

	counter = 0
	found_data = '['

	for movie in movies:
		ID, title, url, year, rating, synopsis, image = movie
		
		if phrase.lower() in title.lower():
			counter += 1

			title = correct(title)
			url = correct(url)
			rating = correct(rating)
			synopsis = correct(synopsis)
			image = correct(image)

			data = '{'
			data += f'"id": "{ID}", '
			data += f'"title": "{title}", '
			data += f'"url": "{url}", '
			data += f'"year": "{year}", '
			data += f'"rating": "{rating}", '
			data += f'"synopsis": "{synopsis}", '
			data += f'"image": "{image}"'
			data += '}'

			if counter < count:
				data += ', '

			found_data += data

	found_data += ']'

	return HttpResponse(found_data, content_type="application/json")
