from flask.cli import FlaskGroup
from flask_migrate import Migrate, upgrade
from app import create_app, db
from models import User, Content, Rating, Test, Question, Option, TestResult, Lecture, Presentation
from seed_database import seed_database

app = create_app()
cli = FlaskGroup(create_app=create_app)
migrate = Migrate(app, db)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database tables created!")

@cli.command("seed_db")
def seed_db():
    seed_database()
    print("Database seeded!")

@cli.command("db_migrate")
def db_migrate():
    """Создает миграцию"""
    import subprocess
    subprocess.run(["flask", "db", "migrate"])
    print("Migration created.")

@cli.command("db_upgrade")
def db_upgrade():
    """Применяет миграции к базе данных"""
    upgrade()
    print("Database upgraded.")

@cli.command("db_downgrade")
def db_downgrade():
    """Откатывает последнюю миграцию"""
    import subprocess
    subprocess.run(["flask", "db", "downgrade"])
    print("Database downgraded.")

if __name__ == '__main__':
    cli()
