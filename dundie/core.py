import os
from datetime import datetime
from csv import reader
from dundie.models import Person, Balance, Movement
from dundie.utils.db import add_movement, add_person
from dundie.utils.log import get_logger
from typing import Any, Dict, List
from dundie.database import get_session
from sqlmodel import select
from dundie.settings import DATEFMT
from dundie.utils.exchange import get_rates

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


def load(filepath: str) -> ResultDict:
    """Loads data from filepath to the database.
    >>> len(load('assets/people.csv'))
    2
    >>> load('assets/people.csv')[0][0]
    'J'
    """

    people = []
    headers = ["name", "dept", "role", "email", "currency"]

    try:
        with open(filepath, newline="") as csvfile:
            csv_data = reader(csvfile)
            header_row = next(csv_data)  # Read the header row
            header_map = dict(zip(header_row, headers))  # Map the header names

            with get_session() as session:
                for line in csv_data:
                    person_data = dict(
                        zip(header_row, [item.strip() for item in line])
                    )

                    # Ensure the email column is properly named and present
                    if not person_data.get(header_map.get("email")):
                        log.warning(
                            f"Skipping line with missing or invalid email: {person_data}"
                        )
                        continue

                    # Validate and process the data
                    try:
                        # Convert CSV data to Person instance
                        mapped_person_data = {
                            "email": person_data.get(header_map["email"]),
                            "name": person_data.get(header_map["name"]),
                            "dept": person_data.get(header_map["dept"]),
                            "role": person_data.get(header_map["role"]),
                            "currency": person_data.get(
                                header_map["currency"], "USD"
                            ),
                        }
                        instance = Person(**mapped_person_data)
                        person, created = add_person(session, instance)
                        return_data = person.model_dump(exclude={"id"})
                        return_data["created"] = created
                        people.append(return_data)
                    except Exception as e:
                        log.error(
                            f"Error processing record {person_data}: {e}"
                        )
                        continue

                session.commit()

    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        raise e

    return people


def read(**query: Query) -> ResultDict:
    """Read data from db and filters using query
    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    return_data = []

    query_statements = []
    if "dept" in query:
        query_statements.append(Person.dept == query["dept"])
    if "email" in query:
        query_statements.append(Person.email == query["email"])
    sql = select(Person)  # SELECT FROM PERSON
    if query_statements:
        sql = sql.where(*query_statements)

    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        rates = get_rates(currencies)
        results = session.exec(sql)
        for person in results:

            balance_value = (
                person.balance.value if person.balance else 0
            )  # Acessar diretamente o atributo
            movements = session.exec(
                select(Movement)
                .where(Movement.person_id == person.id)
                .order_by(Movement.date.desc())
            ).all()
            last_movement_date = (
                movements[0].date.strftime(DATEFMT) if movements else None
            )
            total = rates[person.currency].value * balance_value
            return_data.append(
                {
                    "email": person.email,
                    "balance": balance_value,
                    "last_movement": last_movement_date,
                    **person.model_dump(exclude={"id"}),
                    **{"value": total},
                }
            )

    return return_data


def add_movement(session, person, value, actor):
    """Add a movement entry for the specified person."""
    movement = Movement(
        person_id=person.id, value=value, actor=actor, date=datetime.now()
    )
    session.add(movement)


def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:  # pragma: no cover
        raise RuntimeError("Not Found")

    with get_session() as session:
        for person in people:
            # Encontre a pessoa no banco de dados
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()

            if instance:  # Verificar se a instância foi encontrada
                # Encontre o saldo atual
                balance = session.exec(
                    select(Balance).where(Balance.person_id == instance.id)
                ).first()

                if balance:
                    # Atualize o saldo
                    balance.value += value
                else:
                    # Se não houver saldo, crie um novo
                    balance = Balance(person_id=instance.id, value=value)
                    session.add(balance)

                # Crie um novo movimento
                movement = Movement(
                    person_id=instance.id,
                    actor="system",  # Defina um valor padrão para o ator, se necessário
                    value=value,
                    date=datetime.now(),
                )
                session.add(movement)

        session.commit()
