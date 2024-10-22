from app import create_app, db
from app.models import Course

def seed_database():
    app = create_app()
    with app.app_context():
        # Добавляем курсы
        courses = [
            Course(title='Python для начинающих', 
                   description='Базовый курс программирования на Python', 
                   video_url='https://www.youtube.com/embed/rfscVS0vtbw'),
            Course(title='JavaScript с нуля', 
                   description='Полный курс по JavaScript для начинающих веб-разработчиков', 
                   video_url='https://www.youtube.com/embed/PkZNo7MFNFg'),
            Course(title='HTML и CSS основы', 
                   description='Введение в веб-разработку с HTML и CSS', 
                   video_url='https://www.youtube.com/embed/mU6anWqZJcc')
        ]
        
        for course in courses:
            db.session.add(course)
        
        db.session.commit()
        print("База данных успешно заполнена тестовыми данными.")

if __name__ == "__main__":
    seed_database()
