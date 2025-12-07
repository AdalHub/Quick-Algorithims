import datetime
class Commit:
    def __init__(self,commit_name, parent):
        self.commit_name= commit_name
        self.date_created = datetime.now()
        self.parent = parent

    def __str__(self):
        return f"{self.commit_name}"

    def __repr__(self):
        return f"Commit( commit_name= {self.commit_name}, date_created ={self.date_created} )"

    def __getitem__():
        with open():
            print()

class Branch():

    def __init__(self):
        self.head = Commit()

    def __del__():
        print()