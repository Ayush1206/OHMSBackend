"""
Module for defining the database models and managing database operations.
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from modules.utilities import logger

Base = declarative_base()


class Users(Base):
    """
    Model representing the Users table.
    """

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)

    # Establish a relationship to Employees table
    employee = relationship("Employees", back_populates="user", uselist=False)


class Employees(Base):
    """
    Model representing the Employees table.
    """

    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    employee_id = Column(String(20), nullable=False, unique=True)
    department_id = Column(Integer, nullable=True)
    blood_group = Column(String(3), nullable=True)
    gov_id = Column(String(50), nullable=True)
    verification_documents = Column(String(255), nullable=True)

    # Establish a relationship to Users table
    user = relationship("Users", back_populates="employee")

    # Unique constraint for employee_id
    __table_args__ = (UniqueConstraint("employee_id", name="uq_employee_id"),)


def add_user(username, email, hashed_password, role_id, first_name, last_name, middle_name=None):
    """
    Add a new user to the database.

    :param username: The username of the user.
    :param email: The email of the user.
    :param hashed_password: The hashed password of the user.
    :param role_id: The role ID associated with the user.
    :param first_name: The first name of the user.
    :param last_name: The last name of the user.
    :param middle_name: The middle name of the user (optional).
    :return: The newly created user object.
    :raises Exception: If there is an error during database operations.
    """
    try:
        new_user = Users(
            username=username,
            email=email,
            password=hashed_password,
            role_id=role_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )
        session = create_db_session()
        session.add(new_user)
        session.commit()
        return new_user
    except SQLAlchemyError as exc:
        session.rollback()
        logger.error(f"Failed to add user: {str(exc)}")
        raise Exception(f"Failed to add user: {str(exc)}") from exc
    finally:
        session.close()


def add_employee(user_id, blood_group=None, gov_id=None, verification_documents=None):
    """
    Add a new employee to the database.

    :param user_id: The user ID associated with the employee.
    :param blood_group: The blood group of the employee (optional).
    :param gov_id: The government ID of the employee (optional).
    :param verification_documents: The verification documents for the employee (optional).
    :raises Exception: If there is an error during database operations.
    """
    try:
        new_employee = Employees(
            user_id=user_id,
            employee_id=generate_employee_id(),  # Assumes a function to generate a unique employee ID
            blood_group=blood_group,
            gov_id=gov_id,
            verification_documents=verification_documents,
        )
        session = create_db_session()
        session.add(new_employee)
        session.commit()
    except SQLAlchemyError as exc:
        session.rollback()
        logger.error(f"Failed to add employee: {str(exc)}")
        raise Exception(f"Failed to add employee: {str(exc)}") from exc
    finally:
        session.close()


def create_db_session():
    """
    Create a new SQLAlchemy session for interacting with the database.

    :return: A new SQLAlchemy session.
    """
    try:
        # Replace with your Google Cloud SQL connection string
        engine = create_engine(
            "postgresql+psycopg2://user:password@cloudsql/project-id:region:instance-id/dbname"
        )
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        logger.info("Database session created successfully.")
        return session
    except SQLAlchemyError as exc:
        logger.error(f"Failed to create database session: {str(exc)}")
        raise Exception(f"Failed to create database session: {str(exc)}") from exc


# If using SQLAlchemy for database connections
def init_db(engine):
    """
    Initialize the database by creating all tables.

    :param engine: The SQLAlchemy engine connected to the database.
    """
    Base.metadata.create_all(engine)
