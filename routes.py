from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_from_directory, current_app
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Content, Rating, Test, Question, Option, TestResult, Lecture, Presentation
from extensions import db
from forms import LoginForm, RegistrationForm, ContentForm, TestForm, LectureForm
import os

main = Blueprint('main', __name__)

# Здесь разместите ваши маршруты (routes)
@main.route('/')
def index():
    contents = Content.query.order_by(Content.id.desc()).limit(6).all()
    return render_template('index.html', contents=contents)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/add_content', methods=['GET', 'POST'])
@login_required
def add_content():
    form = ContentForm()
    if form.validate_on_submit():
        content = Content(
            title=form.title.data,
            content_type=form.content_type.data,
            category=form.category.data,
            url=form.url.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(content)
        db.session.commit()
        flash('Content added successfully!')
        return redirect(url_for('main.index'))
    return render_template('add_content.html', form=form)

@main.route('/content/<int:content_id>')
def content_detail(content_id):
    content = Content.query.get_or_404(content_id)
    return render_template('content_detail.html', content=content)

@main.route('/category/<category>')
def category_content(category):
    contents = Content.query.filter_by(category=category).all()
    return render_template('category_content.html', category=category, contents=contents)

@main.route('/lectures')
def lectures():
    lectures = Lecture.query.all()
    return render_template('lectures.html', lectures=lectures)

@main.route('/lecture/<int:lecture_id>')
def lecture_detail(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    return render_template('lecture_detail.html', lecture=lecture)

@main.route('/create_lecture', methods=['GET', 'POST'])
@login_required
def create_lecture():
    form = LectureForm()
    if form.validate_on_submit():
        lecture = Lecture(title=form.title.data, description=form.description.data, content=form.content.data)
        db.session.add(lecture)
        db.session.commit()
        flash('Лекция успешно создана!', 'success')
        return redirect(url_for('main.lecture_detail', lecture_id=lecture.id))
    return render_template('create_lecture.html', form=form)

@main.route('/presentations')
def presentations():
    presentations = Presentation.query.all()
    return render_template('presentations.html', presentations=presentations)

@main.route('/presentation/<int:presentation_id>')
def presentation_detail(presentation_id):
    presentation = Presentation.query.get_or_404(presentation_id)
    return render_template('presentation_detail.html', presentation=presentation)

@main.route('/pdf/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(current_app.config['PDF_FOLDER'], filename)

@main.route('/courses')
def courses():
    courses = [
        {
            'id': 1,
            'title': 'Python для начинающих',
            'description': 'Базовый курс программирования на Python',
            'video_url': 'https://www.youtube.com/embed/rfscVS0vtbw'
        },
        {
            'id': 2,
            'title': 'Продвинутый JavaScript',
            'description': 'Углубленное изучение JavaScript',
            'video_url': 'https://www.youtube.com/embed/W6NZfCO5SIk'
        },
        {
            'id': 3,
            'title': 'Алгоритмы и структуры данных',
            'description': 'Изучение основных алгоритмов и структур данных',
            'video_url': 'https://www.youtube.com/embed/8hly31xKli0'
        },
        {
            'id': 4,
            'title': 'Веб-разработка с Flask',
            'description': 'Создание веб-приложений с использованием Flask',
            'video_url': 'https://www.youtube.com/embed/Z1RJmh_OqeA'
        },
        {
            'id': 5,
            'title': 'Машинное обучение для начинащих',
            'description': 'Введение в машинное обучение с Python',
            'video_url': 'https://www.youtube.com/embed/7eh4d6sabA0'
        },
        {
            'id': 6,
            'title': 'Разработка мобильных приложений',
            'description': 'Создание мобильных приложений с React Native',
            'video_url': 'https://www.youtube.com/embed/0-S5a0eXPoc'
        }
    ]
    return render_template('courses.html', courses=courses)

@main.route('/enroll/<int:course_id>')
@login_required
def enroll_course(course_id):
    # Здесь должна быть логика записи на курс
    flash('Вы успешно записались на курс!', 'success')
    return redirect(url_for('main.courses'))

@main.route('/tests')
def tests():
    tests = Test.query.all()
    return render_template('tests.html', tests=tests)

@main.route('/test/<int:test_id>')
def test_detail(test_id):
    test = Test.query.get_or_404(test_id)
    return render_template('test_detail.html', test=test)

@main.route('/take_test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    if request.method == 'POST':
        score = 0
        for question in test.questions:
            selected_option_id = request.form.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.query.get(selected_option_id)
                if selected_option and selected_option.is_correct:
                    score += 1
        
        test_result = TestResult(test_id=test.id, user_id=current_user.id, score=score)
        db.session.add(test_result)
        db.session.commit()
        flash(f'Тест завершен! Ваш результат: {score} из {len(test.questions)}', 'success')
        return redirect(url_for('main.test_detail', test_id=test.id))
    
    return render_template('take_test.html', test=test)

@main.route('/submit_test', methods=['POST'])
def submit_test():
    data = request.json
    test_id = data['test_id']
    answers = data['answers']
    
    tests = [
        # Сопируйте список тестов из функции tests()
    ]
    test = next((t for t in tests if t['id'] == test_id), None)
    
    if test:
        correct_answers = sum(1 for i, answer in enumerate(answers) if answer == test['questions'][i]['correct_answer'])
        return jsonify({'correct_answers': correct_answers, 'total_questions': len(test['questions'])})
    else:
        return jsonify({'error': 'Test not found'}), 404

@main.route('/dashboard')
@login_required
def dashboard():
    user_contents = Content.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user_contents=user_contents)

@main.route('/create_test', methods=['GET', 'POST'])
@login_required
def create_test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test(title=form.title.data, description=form.description.data)
        for question_form in form.questions:
            question = Question(text=question_form.text.data)
            for option_form in question_form.options:
                option = Option(text=option_form.text.data, is_correct=option_form.is_correct.data)
                question.options.append(option)
            test.questions.append(question)
        db.session.add(test)
        db.session.commit()
        flash('Тест успешно сздан!', 'success')
        return redirect(url_for('main.test_detail', test_id=test.id))
    return render_template('create_test.html', form=form)

# Добавьте остальные маршруты здесь




































