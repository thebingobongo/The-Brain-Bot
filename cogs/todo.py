import discord
from discord.ext import commands
from databaselayer import getTodo, deleteTodo, addTodo

def displayToDo():
    todolist = getTodo()
    #returntext = '**To Do list:**\n'
    returnembed = discord.Embed(title="To Do List",color=0x12ffdb)
    for i in range(len(todolist)):
        returntext = (str(i + 1) + '. ' + todolist[i][0])
        returnembed.add_field(name=returntext, value="** **",inline=False)

    returnembed.set_footer(text="To remove a task: .delete [task number] \n To add a new task: .add [task]")
    return returnembed


def removeToDo(index):
    td = getTodo()
    if index > len(td):
        return 'Index does not exist, try again.'
    else:
        removed = td[index - 1][0]
        deleteTodo(removed)
        return ' Task at index ' + str(index) + ' has been successfully removed.'


def addToDo(task):
    addTodo(task)
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