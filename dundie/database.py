from sqlmodel import Session, create_engine
from dundie import models
import warnings

from sqlalchemy.exc import SAWarning


from sqlmodel.sql.expression import Select, SelectOfScalar


from dundie.settings import SQL_CON_STRING

# ^ IMPORTANTE importar todos os models para este contexto


# We have to monkey patch this attributes
# https://github.com/tiangolo/sqlmodel/issues/189
warnings.filterwarnings("ignore", category=SAWarning)

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = create_engine(SQL_CON_STRING, echo=False)
models.SQLModel.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(engine)
