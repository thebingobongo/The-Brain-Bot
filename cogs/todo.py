import pickle
import discord
from discord.ext import commands

with open('todo.pkl', 'rb') as f:
    todolist = pickle.load(f)

def displayToDo():
    global todolist
    with open('todo.pkl', 'rb') as f:
        todolist = pickle.load(f)
    #returntext = '**To Do list:**\n'
    returnembed = discord.Embed(title="To Do List",color=0x12ffdb)
    for i in range(len(todolist)):
        returntext = (str(i + 1) + '. ' + todolist[i])
        returnembed.add_field(name=returntext, value="** **",inline=False)

    #returntext = returntext + '\n To remove a task: .delete [task number] \n To add a new task: .add [task]'
    returnembed.set_footer(text="To remove a task: .delete [task number] \n To add a new task: .add [task]")
    return returnembed


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


def predicate(ctx):
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    return staff_role in ctx.author.roles
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Todo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_roles
    async def todo(self, ctx):
        await ctx.send(embed=displayToDo())


    @commands.command()
    @has_roles
    async def add(self, ctx, *, task):
        if len(task) > 250:
            await ctx.send('The length of the task is too long. Please limit yourself to 250 characters')
        else:

            await ctx.send(addToDo(task))
            await ctx.send(embed=displayToDo())


    @commands.command(aliases=['del'])
    @has_roles
    async def delete(self, ctx, index):
        if index.isdigit():
            await ctx.send(removeToDo(int(index)))
            await ctx.send(embed=displayToDo())
        else:
            await ctx.send('Invalid index. Use a number next time.')


def setup(client):
    client.add_cog(Todo(client))