import sqlalchemy

from app.models.db_session import SqlAlchemyBase


class ChatsOfUsers(SqlAlchemyBase):
    """Модель чатов юзеров"""

    __tablename__ = "chats_of_users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.UUID, unique=True)
    data = sqlalchemy.Column(
        sqlalchemy.JSON, nullable=True, default={"messages": []}
    )
    name_of_chat = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def add_new_message(
        self, sender: str, content: str, datetime_of_users_message: str
    ):
        """
        Добавляет сообщение в чат.

        :param sender: Отправитель сообщения ('user' или 'bot')
        :type sender: str
        :param content: Содержание сообщения
        :type content: str
        """
        self.data["messages"].append(
            {
                "timestamp": datetime_of_users_message,
                "sender": sender,
                "content": content,
            }
        )
