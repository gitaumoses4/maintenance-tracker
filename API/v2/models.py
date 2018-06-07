"""Creates the database models with ability to perform SQL functions"""

from run import database
import v1.models
from datetime import datetime


class DBBaseModel(v1.models.BaseModel):
    __table__ = ""

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, created_at, updated_at):
        super().__init__(created_at, updated_at)

    def migrate(self):
        pass

    @staticmethod
    def deserialize(dictionary):
        """ Create a model object from the dictionary,
            Override this method to do the conversion custom
        """
        return None

    @classmethod
    def query_all(cls):
        """
        Query all items from the database
        :return:
        """
        database.cursor.execute("SELECT * FROM {}".format(cls.__table__))
        items = database.cursor.fetchall()
        return {cls.deserialize(x) for x in items}

    @classmethod
    def query_by_id(cls, _id):
        """
        Query items from the database by id
        :param _id:
        :return:
        """
        database.cursor.execute("SELECT * FROM %s WHERE id = %s", (cls.__table__, _id))
        item = database.cursor.fetchone()
        if item is None:
            return None
        return cls.deserialize(item)

    def save(self):
        """ Save an item to the database"""
        pass

    def update(self):
        """
        Updates the details of an item
        :return:
        """
        self.updated_at = datetime.now()
        pass

    def delete(self):
        """
        Deletes an item from the database
        :return:
        """
        database.cursor.execute("DELETE FROM %s WHERE id = %s", (self.__table__, self.id))
        database.connection.commit()


class User(v1.models.User, DBBaseModel):
    __table__ = "users"

    def migrate(self):
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY ,
            firstname varchar,
            lastname varchar,
            username varchar,
            email varchar,
            password varchar,
            created_at timestamp,
            updated_at timestamp,
            role varchar)""")
        database.connection.commit()

    @staticmethod
    def deserialize(dictionary):
        user = User()
        if dictionary is None:
            return None
        user.firstname = dictionary['firstname']
        user.lastname = dictionary['lastname']
        user.username = dictionary['username']
        user.email = dictionary['email']
        user.password = dictionary['password']
        user.created_at = datetime.strptime(dictionary['created_at'], DBBaseModel.DATE_FORMAT)
        user.updated_at = datetime.strptime(dictionary['updated_at'], DBBaseModel.DATE_FORMAT)
        return user

    def save(self):
        """
        Save the user into the database
        :return:
        """
        database.cursor.execute(
            "INSERT INTO users(firstname,lastname,username,email,"
            "password,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s)", (
                self.firstname, self.lastname, self.username, self.email,
                self.password, self.created_at,
                self.updated_at
            ))
        database.connection.commit()

    def update(self):
        """
        Update the details of the user
        :return:
        """
        super().update()
        database.cursor.execute(
            "UPDATE users SET firstname = %s, lastname = %s, username = %s,"
            "email = %s, password = %s, updated_at = %s where id = %s", (
                self.firstname, self.lastname, self.username,
                self.email, self.password,
                self.updated_at,
                self.id))
        database.connection.commit()


class Request(v1.models.Request, DBBaseModel):
    __table__ = "requests"

    def migrate(self):
        database.cursor.execute("""CREATE TABLE requests(
          id serial PRIMARY KEY ,
          product_name varchar,
          description varchar,
          status varchar,
          photo varchar,
          created_by INTEGER,
          created_at TIMESTAMP,
          updated_at TIMESTAMP,
          FOREIGN KEY (created_by) REFERENCES users(id))""")
        database.connection.commit()

    def save(self):
        """
        Save the request into the database
        :return:
        """
        database.cursor.execute(
            "INSERT INTO requests(product_name,description,status,photo,created_by,created_at,updated_at)"
            " VALUES(%s,%s,%s,%s,%s,%s,%s)", (
                self.product_name,
                self.description,
                self.status,
                self.photo,
                self.created_by,
                self.created_at,
                self.updated_at
            ))
        database.connection.commit()

    def update(self):
        super().update()
        database.cursor.execute(
            "UPDATE requests SET product_name = %s, description = %s, "
            "status = %s, photo = %s, updated_at = %s WHERE id = %s", (
                self.product_name,
                self.description,
                self.status,
                self.photo,
                self.updated_at,
                self.id
            )
        )
        database.connection.commit()

    def approve(self):
        """
        Mark a request as approved
        :return:
        """
        self.status = Request.STATUS_APPROVED
        self.update()

    def disapprove(self):
        """
        Mark a request as disapproved
        :return:
        """
        self.status = Request.STATUS_DISAPPROVED
        self.update()

    def resolve(self):
        """
        Mark a request as resolved
        :return:
        """
        self.status = Request.STATUS_RESOLVED
        self.update()


class Feedback(v1.models.Feedback, DBBaseModel):
    __table__ = "feedback"

    def migrate(self):
        database.cursor.execute("""CREATE TABLE feedback(
          id serial PRIMARY KEY ,
          admin INTEGER,
          request INTEGER,
          message varchar,
          created_at timestamp,
          updated_at TIMESTAMP,
          foreign key (admin) references users(id),
          foreign key (request) references requests(id)
        )""")
        database.connection.commit()

    def save(self):
        database.cursor.execute("INSERT INTO feedback(admin, request, message, created_at, updated_at) "
                                "VALUES(%s,%s,%s,%s,%s)", (
                                    self.admin,
                                    self.request,
                                    self.message,
                                    self.created_at,
                                    self.updated_at
                                ))


if __name__ == '__main__':
    User.query_all()
