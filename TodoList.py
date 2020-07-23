from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

def display_task(dolist):
    if len(dolist) <= 1:
        print('\nToday', datetime.today().strftime("%d, %b"))
        print("Nothing to do!")
        print()
    else:
        doinx = 1
        print('\nToday', dolist[0].deadline.strftime("%d, %b"))
        for row in dolist:
            if row.task != "Nothing to do!":
                print(f"{doinx}. {row.task}")
                doinx += 1
        print()

def disp_weektask(dolist):
    if len(dolist) == 1:
        print(dolist[0].deadline.strftime("%A, %d, %b"))
        print(dolist[0].task)
        print()
    else:
        doinx = 1
        print(dolist[0].deadline.strftime("%A, %d, %b"))
        for row in dolist:
            if row.task != "Nothing to do!":
                print(f"{doinx}. {row.task}")
                doinx += 1
        print()

def disp_alltasks(dolist):
    indx = 1
    for row in dolist:
        print(f"{indx}. {row.task}. {row.deadline.strftime('%d, %b')}")
        indx += 1

def add_tasks():
    ondate = datetime.today()
    for days in range(7):
        add_row = Table(deadline=ondate)
        session.add(add_row)
        session.commit()
        ondate += timedelta(days=1)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

user_ch = 1
while user_ch != 0:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    user_ch = int(input('Enter Choice >').strip())

    if user_ch == 1:    # display today's task
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        display_task(rows)

    elif user_ch == 2:  # display week's task
        rows = session.query(Table).all()
        if len(rows) < 7:
            add_tasks()
        date_count = datetime.today().date()
        print()
        for day in range(7):
            rows = session.query(Table).filter(Table.deadline == date_count).all()
            disp_weektask(rows)
            date_count += timedelta(days=1)

    elif user_ch == 3:  # display all tasks
        print('\nAll tasks:')
        rows = session.query(Table).filter(Table.task != "Nothing to do!").order_by(Table.deadline).all()
        disp_alltasks(rows)
        print()

    elif user_ch == 4:  # display missed tasks
        print('\nMissed tasks:')
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if len(rows) != 0:
            disp_alltasks(rows)
            print()
        else:
            print('Nothing is missed!')
            print()

    elif user_ch == 5:  # add task & deadline
        print('\nEnter Task')
        new_task = input().strip()
        print('Enter deadline date')
        datestr = input().strip()
        ddate = datetime.strptime(datestr, '%Y-%m-%d').date()
        new_row = Table(task=new_task, deadline=ddate)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')

    elif user_ch == 6:  # delete task
        print('\nChoose the number of the task you want to delete:')
        rows = session.query(Table).filter(Table.task != "Nothing to do!").order_by(Table.deadline).all()
        disp_alltasks(rows)
        taskno = int(input().strip())
        delete_row = rows[taskno-1]
        session.delete(delete_row)
        session.commit()
        print('The task has been deleted!')
        print()

    elif user_ch == 0:  # Exit
        print("\nBye!")
