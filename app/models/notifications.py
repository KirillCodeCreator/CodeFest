import sqlalchemy

from app.models.db_session import SqlAlchemyBase


class Notifications(SqlAlchemyBase):
    __tablename__ = "notifications"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    data = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
