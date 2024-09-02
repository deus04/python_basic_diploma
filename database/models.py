from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config_data.config import DATE_FORMAT, DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


#Карточка в историю
class Task(BaseModel):
    task_id = AutoField()
    user = ForeignKeyField(User, backref="tasks")
    title = CharField()
    due_date = DateTimeField()

    def __str__(self):
        return "{task_id}. {title} - {due_date}".format(
            task_id=self.task_id,
            title=self.title,
            due_date=self.due_date.strftime(DATE_FORMAT),
        )


def create_models():
    db.create_tables(BaseModel.__subclasses__())