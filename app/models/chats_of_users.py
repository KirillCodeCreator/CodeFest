import sqlalchemy

from app.models.db_session import SqlAlchemyBase


class ChatsOfUsers(SqlAlchemyBase):
    __tablename__ = "chats_of_users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.UUID, unique=True)
    data = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    name_of_chat = sqlalchemy.Column(sqlalchemy.String, nullable=False)
