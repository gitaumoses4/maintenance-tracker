"""Runs the database set up options such as refresh, reset and create"""

from v2.app.models import User, Request, Feedback, Notification, Blacklist, Admin


class Migration:

    @staticmethod
    def refresh():
        """The refresh function does not recreate the database, but deletes data from the tables"""
        Migration.tear_down()
        Migration.set_up()

    @staticmethod
    def set_up():
        """
        Create the tables
        :return:
        """
        User.migrate()
        Request.migrate()
        Feedback.migrate()
        Notification.migrate()
        Blacklist.migrate()

        # create default admin
        admin = Admin.default()
        if not Admin.query_one_by_field("username", admin.username)
            admin.save()

    @staticmethod
    def tear_down():
        """
        Delete data from the tables
        :return:
        """
        Feedback.rollback()
        Request.rollback()
        Notification.rollback()
        User.rollback()
        Blacklist.rollback()


migration = Migration()
# Running this file drops the database and creates the tables
if __name__ == '__main__':
    migration.set_up()
