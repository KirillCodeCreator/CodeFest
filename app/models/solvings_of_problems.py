import sqlalchemy

from app.models.db_session import SqlAlchemyBase


class SolvingsOfProblems(SqlAlchemyBase):
    __tablename__ = "solvings_of_problems"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    key_words = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    solving_of_problem = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
