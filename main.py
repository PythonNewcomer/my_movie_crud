from config_reader import ConfigReader
from flask import Flask, request, render_template, flash, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movie_tables import Movie, Country, Genre, movies_genres_association


app = Flask('MoviesREST')
cr = ConfigReader()
host, port, dbname, user, password = cr.get_database_config()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, dbname))
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def show_all():
    return render_template('home.html')


@app.route('/add_movie')
def send_to_add_page():
    return render_template('add_movie.html')


@app.route('/delete_movie')
def send_to_delete_page():
    return render_template('delete_movie.html')


@app.route('/find_movie')
def send_to_find_page():
    return render_template('find_movie.html')


@app.route('/movies', methods=['GET'])
def get_movies():
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name.label('country'), Genre.name.label('genre')) \
        .join(Country, isouter=True) \
        .join(movies_genres_association, isouter=True) \
        .join(Genre, isouter=True)\
        .all()
    return render_template('show_all.html', movies=result)


@app.route('/movie', methods=['POST'])
def get_movie():
    title = request.form.get("title")
    result = session.query(Movie.id, Movie.title, Movie.year, Country.name.label('country'), Genre.name.label('genre'))\
        .join(Country, isouter=True) \
        .join(movies_genres_association, isouter=True) \
        .join(Genre, isouter=True)  \
        .filter(Movie.title == title) \
        .first()
    return render_template('show_movie.html', movie=result)


@app.route('/movies', methods=['POST'])
def add_movie():
    if not request.form['title'] or not request.form['year'] or not request.form['country'] or not request.form['genre']:
        flash('Please enter all the fields', 'error')
    else:
        country = session.query(Country).filter(Country.name == request.form['country']).first()
        g = session.query(Genre).filter(Genre.name == request.form['genre']).first()
        print(type(country))
        print(g)

        movie_row = Movie(title=request.form['title'], year=request.form['year'],
                          country=session.query(Country).filter(Country.name == request.form['country']).first())
        movie_row.genre.append(session.query(Genre).filter(Genre.name == request.form['genre']).first())
        session.add(movie_row)
        session.commit()
        flash('Record was successfully added!')
    return redirect(url_for('get_movies'))


@app.route("/delete", methods=["POST"])
def delete_movie():
    title = request.form.get("title")
    movie_row = session.query(Movie).filter(Movie.title == title).first()
    session.delete(movie_row)
    session.commit()
    flash('Record was successfully deleted!')
    return redirect(url_for('get_movies'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)

