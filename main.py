from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database import app, User, db
from stats import professions_data


@app.route('/')
@app.route('/index')
def index():
    title = request.args.get('title', 'Миссия')
    return render_template('index.html',
                           title=title,
                           mission_name='Поход к роковой горе',
                           mission_slogan='Сложности встречаются, но мы непременно дойдем до конца!')


@app.route('/training/<prof>')
def training(prof):
    title = 'Тренировка'
    prof = prof.lower()

    if prof in professions_data:
        profession = professions_data[prof]
        header = profession['header']
        image_url = profession['image_url']
        stats = profession['stats']

    return render_template('training.html',
                           title=title,
                           mission_name='Поход к роковой горе',
                           mission_slogan='Сложности встречаются, но мы непременно дойдем до конца!',
                           header=header,
                           image_url=image_url,
                           hp=stats['hp'],
                           mana=stats['mana'],
                           level=stats['level'],
                           experience=stats['experience'],
                           strength=stats['strength'],
                           stamina=stats['stamina'],
                           agility=stats['agility'])



@app.route('/form', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        login_email = request.form['login_email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        speciality = request.form['speciality']
        address = request.form['address']

        if password != repeat_password:
            flash('Пароли не совпадают!')
            return redirect(url_for('home'))

        hashed_password = generate_password_hash(password=password, method='pbkdf2:sha1', salt_length=8)

        new_user = User(login_email=login_email, password=hashed_password, surname=surname, name=name, age=age, speciality=speciality, address=address)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!')
        return redirect(url_for('home'))

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=False)
