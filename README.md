# movie-quote
a api made by django rest framework serve movie and series quotes.

## Installation
### Linux
1. git clone https://github.com/F4R4N/movie-quote.git
2. apt install python3
3. cd movie-quote
4. ` python3 -m venv venv`
5. source venv/bin/activate
6. python3 manage.py migrate
7. python3 manage.py runserver
8. open browser in 127.0.0.1:8000

### Windows
1. git clone https://github.com/F4R4N/movie-quote.git or download directly
2. install [python3](https://www.python.org/downloads/)
3. cd movie-quote
4. `python -m venv venv`
5. venv\Scripts\activate
6. python manage.py migrate
7. python manage.py runserver
8. open browser in 127.0.0.1:8000

## Usage
use the following path's to get the quotes.

### /v1/quote/
get a random quote each time, from all quotes.

### /v1/shows/<show_slug>
you can get a random quote from the desired show. you can find list of show's slug in https://movie-quote-api.herokuapp.com/.
