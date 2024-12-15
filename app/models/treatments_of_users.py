import sqlalchemy

from app.models.db_session import SqlAlchemyBase


class TreatmentsOfUsers(SqlAlchemyBase):
    """Модель вопросов юзеров"""

    __tablename__ = "treatments_of_users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    key_words = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    data_of_treatment = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
