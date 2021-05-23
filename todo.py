import pickle

with open('todo.pkl', 'rb') as f:
    todolist = pickle.load(f)

def displayToDo():
    global todolist
    with open('todo.pkl', 'rb') as f:
        todolist = pickle.load(f)
    returntext = '**To Do list:**\n'
    for i in range(len(todolist)):
        returntext = returntext + (str(i + 1) + '. ' + todolist[i] + '\n')

    returntext = returntext + '\n To remove a task: .delete [task number] \n To add a new task: .add [task]'
    return returntext


def removeToDo(index):
    global todolist
    if index > len(todolist):
        return 'Index does not exist, try again.'
    else:
        todolist.pop(index - 1)
        with open('todo.pkl', 'wb') as f:
            pickle.dump(todolist, f)
        return ' Task at index ' + str(index) + ' has been successfully removed.'


def addToDo(task):
    global todolist
    todolist.append(task)
    with open('todo.pkl', 'wb') as f:
        pickle.dump(todolist, f)
    return "Task has been successfully added!"