from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, Lecture, Course, Content

@bp.route('/')
def index():
    popular_courses = Course.query.filter_by(type='course').order_by(Course.views.desc()).limit(3).all()
    popular_video_courses = Course.query.filter_by(type='video').order_by(Course.views.desc()).limit(3).all()
    return render_template('index.html', 
                           popular_courses=popular_courses, 
                           popular_video_courses=popular_video_courses)

@bp.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    print(f"Rendering course_detail.html for course_id: {course_id}")  # Добавьте эту строку
    return render_template('course_detail.html', course=course)

@bp.route('/add_lecture', methods=['GET', 'POST'])
@login_required
def add_lecture():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_lecture = Lecture(title=title, content=content, author_id=current_user.id)
        db.session.add(new_lecture)
        db.session.commit()
        flash('Лекция успешно добавлена!')
        return redirect(url_for('main.index'))
    return render_template('add_lecture.html', title='Добавить лекцию')

# ... (другие маршруты)

@bp.route('/content/<int:id>')
def content_detail(id):
    content = Content.query.get_or_404(id)
    return render_template('content_detail.html', content=content)
