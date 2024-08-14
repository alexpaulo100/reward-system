from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship

class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int
    person_id: int = Field(foreign_key='person.id')

    person: "Person" = Relationship(back_populates="balances")

class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    balances: List[Balance] = Relationship(back_populates="person")

# Ajuste o caminho do banco de dados para um diretório no Windows
engine = create_engine("sqlite:///C:/Users/padrao/project/reward-system/sqlmodel.db", echo=False)

# Exclua a tabela existente
SQLModel.metadata.drop_all(bind=engine)

# Crie a tabela novamente com a nova estrutura
SQLModel.metadata.create_all(bind=engine)

with Session(engine) as session:
    # Adicionando pessoas e saldos
    person1 = Person(name="Alex")
    session.add(person1)
    session.commit()
    session.refresh(person1)  # Atualiza a instância para garantir que o ID seja preenchido

    balance1 = Balance(value=60, person_id=person1.id)
    session.add(balance1)
    session.commit()

    # Consultando pessoas
    sql = select(Person, Balance).where(Balance.person_id == Person.id)
    results = session.exec(sql)
    for person, balance in results:
        print(person.name, balance.value)
