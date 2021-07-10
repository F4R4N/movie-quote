# movie-quote
a api made with django rest framework serve movie and series quotes. you can find the api [Here](https://movie-quote-api.herokuapp.com).

## Run locally
### Linux
1. `git clone https://github.com/F4R4N/movie-quote.git`
2. `apt install python3`
3. `cd movie-quote`
4. `python3 -m venv venv`
5. `source venv/bin/activate`
6. `mv sample.config.py config.py` (change settings based on your usage)
7. `python3 manage.py migrate`
8. `python3 manage.py runserver`
9. open browser in 127.0.0.1:8000

### Windows
1. `git clone https://github.com/F4R4N/movie-quote.git` or download directly
2. install [python3](https://www.python.org/downloads/)
3. `cd movie-quote`
4. `python -m venv venv`
5. `venv\Scripts\activate`
6. `move sample.config.py config.py` (change settings based on your usage)
7. `python manage.py migrate`
8. `python manage.py runserver`
9. open browser in 127.0.0.1:8000

## Usage
use the following path's to get the quotes.

### `/v1/quote/`
get a random quote each time, from all quotes.

### `/v1/quote?censored`
don't show quotes which contain adult language.

### `/v1/shows/<show_slug>`
you can get a random quote from the desired show. you can find list of show's slug in https://movie-quote-api.herokuapp.com/v1/shows/.

### `/v1/shows/`
get list of available shows slugs.

## make this repo better
feel free to open `issue` or `pull request` I am trying to make repo better and this will help me.

## deployment
`main` branch of this repository will automatically deploy on [Heroku](https://www.heroku.com).
