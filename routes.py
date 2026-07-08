import os
import secrets
from flask import render_template, redirect, url_for, flash, request
from ext import app, db, login_manager
from models import User, MovieCard, UserMovie, UserRecommendation
from forms import RegisterForm, LoginForm, MovieForm, UpdateProfileForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    
    if user.username == "mariam_admin":
        user.role = "Admin"
        db.session.commit()
        
    form = UpdateProfileForm()

    if current_user.username == user.username:
        if form.validate_on_submit():
            if form.username.data != current_user.username:
                existing_user = User.query.filter_by(username=form.username.data).first()
                if existing_user:
                    flash("ეს სახელი უკვე დაკავებულია! აირჩიე სხვა.", "danger")
                    return redirect(url_for('profile', username=current_user.username))
                current_user.username = form.username.data

            if form.avatar.data:
                picture_file = save_picture(form.avatar.data)
                current_user.avatar_url = picture_file

            db.session.commit()
            flash("შენი პროფილი წარმატებით განახლდა!", "success")
            return redirect(url_for('profile', username=current_user.username))

        elif request.method == 'GET':
            form.username.data = current_user.username

    my_recommendations = UserRecommendation.query.filter_by(user_id=user.id).all()
    share_link = request.url_root + "profile/" + user.username

    return render_template('profile.html', targeted_user=user, recommendations=my_recommendations,
                           share_link=share_link, form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    user = User.query.filter_by(username="mariam_admin").first() 
    if user:
        user.role = "Admin"
        db.session.commit()
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()


        if user and check_password_hash(user.password, form.password.data):

            if user.username == "mariami":
                user.role = "Admin"
                db.session.commit()

            login_user(user, remember=True)
            flash("წარმატებით შეხვედით სისტემაში!", "success")
            return redirect(url_for('main'))
        else:
            flash("სახელი ან პაროლი არასწორია", "danger")
    return render_template("login.html", form=form)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            gender=form.gender.data,
            country=form.country.data,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("წარმატებული რეგისტრაცია!", "success")
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route("/main")
def main():
    movies = MovieCard.query.all()
    return render_template("main.html", movies=movies)


@app.route("/details/<int:detail_id>")
def details(detail_id):
    movie = MovieCard.query.get_or_404(detail_id)
    return render_template('Details.html', movie=movie)


@app.route('/create_movie', methods=['GET', 'POST'])
@login_required
def create_movie():
    if current_user.role != "Admin":
        flash("ამ გვერდზე წვდომა აქვს მხოლოდ ადმინისტრატორს!", "danger")
        return redirect(url_for('main'))

    form = MovieForm()
    if form.validate_on_submit():
        img = form.image_url.data if form.image_url.data else None
        new_movie = MovieCard(
            title=form.title.data,
            genre=form.genre.data,
            director=form.director.data,
            image_url=img,
            year=form.year.data,
            user_id=current_user.id
        )
        db.session.add(new_movie)
        db.session.commit()
        flash("ფილმი წარმატებით დაემატა!", "success")
        return redirect(url_for('main'))

    return render_template('create_movie.html', form=form)


@app.route('/add_to_profile/<int:movie_id>', methods=['POST'])
@login_required
def add_to_profile(movie_id):
    movie = MovieCard.query.get_or_404(movie_id)
    user_comment = request.form.get('comment')

    already_added = UserRecommendation.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()

    if already_added:
        flash("ეს ფილმი უკვე დამატებული გაქვს პროფილზე!", "info")
    else:
        new_favorite = UserRecommendation(
            user_id=current_user.id,
            movie_id=movie_id,
            comment=user_comment
        )
        db.session.add(new_favorite)
        db.session.commit()
        flash(f"'{movie.title}' წარმატებით დაემატა შენს პროფილზე კომენტარით!", "success")

    return redirect("/main")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("შენ წარმატებით გამოხვედი სისტემიდან!", "success")
    return redirect(url_for('main'))


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if current_user.role != "Admin":
        flash("ამ მოქმედების უფლება მხოლოდ ადმინისტრატორს აქვს!", "danger")
        return redirect(url_for('main'))

    movie = MovieCard.query.get_or_404(movie_id)


    recommendations = UserRecommendation.query.filter_by(movie_id=movie_id).all()
    for rec in recommendations:
        db.session.delete(rec)

    db.session.delete(movie)
    db.session.commit()

    flash(f"ფილმი '{movie.title}' წარმატებით წაიშალა!", "success")
    return redirect(url_for('main'))
