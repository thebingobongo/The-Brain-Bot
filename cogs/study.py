import asyncio

import discord
from discord.ext import commands

class Study(commands.Cog):
    activegroups = 0
    groups = {}
    def __init__(self, client):
        self.client = client
        activegroups = 0
        groups = {}


    @commands.command()
    async def studymode(self, ctx):

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)

        await ctx.send("You have activated Study Mode, Good Luck!")

        member = ctx.author
        reason = 'study mode activated'

        await member.remove_roles(member_role, reason=reason)
        await member.add_roles(study_role, reason = "study mode activated.")
        if aboveage_role in member.roles:
            await member.remove_roles(aboveage_role)
        await ctx.author.move_to(None)


    @commands.command()
    async def unstudymode(self,ctx):
        member = ctx.author

        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)

        await member.remove_roles(study_role, reason='study mode disactivated')
        await member.add_roles(member_role, reason='study mode disactivated')
        if not underage_role in member.roles:
            await member.add_roles(aboveage_role)
        await ctx.send("Study Mode has been deactivated.")
        await ctx.author.move_to(None)


    def findgroup(self, member:discord.Member):
        # global groups
        # global activegroups

        for key in self.groups:
            for curr in self.groups[key]:
                if member == curr:
                    return key
        return None


    @commands.command()
    async def startpomo(self, ctx, members: commands.Greedy[discord.Member],studytime:int=None, breaktime:int=None ):
        # global activegroups
        # global groups

        pom_tracker = self.client.get_channel(898047525188173854)
        self.activegroups += 1
        currentgroup = self.activegroups


        if studytime == None or breaktime == None:
            await ctx.send("How long would you like to study for? Try the command again with .studypomo [members] [studytime] [breaktime]")
            return

        if not members:
            members = [ctx.author]
        else:
            members.append(ctx.author)

        self.groups[currentgroup] = members

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        pomo_role =discord.utils.get(ctx.guild.roles, id=897958571306811442)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)


        await ctx.send(f"OK! Your pomodoro session has begun! You will be studying for {studytime} minutes and you'll take a  break for {breaktime} minutes.")
        for member in members:
            await member.add_roles(pomo_role)

        async def check_pomo_role(member):
            if pomo_role not in member.roles:
                try:
                    self.groups[currentgroup].remove(member)
                    return False
                except:
                    pass
            else:
                return True


        while len(self.groups[currentgroup]) > 0:
            for member in self.groups[currentgroup]:
                result = await check_pomo_role(member)
                if result:
                    await member.add_roles(study_role)
                    await member.remove_roles(member_role)
                    if aboveage_role in member.roles:
                        await member.remove_roles(aboveage_role)
            await asyncio.sleep((studytime*60))
            for member in self.groups[currentgroup]:
                r = await check_pomo_role(member)
            if len(self.groups[currentgroup]) != 0:
                print(self.groups[currentgroup])
                member_ping = ''
                for member in self.groups[currentgroup]:
                    member_ping = member_ping + f"{member.mention}"
                await ctx.send(f"Your study session has been completed, time to take a break!\n {member_ping}")
            else:
                await ctx.send("This group is empty")
                del self.groups[currentgroup]
                self.activegroups -= 1
                return
            for member in self.groups[currentgroup]:
                # print(f"{self.groups[currentgroup]} {len(self.groups[currentgroup])} and {member}")
                if pomo_role not in member.roles:
                    try:
                        await members.remove(member)
                    except:
                        pass
                else:
                    await pom_tracker.send(f"{member.name} has completed a pomodoro study session!")
                    await member.add_roles(member_role)
                    await member.remove_roles(study_role)
                    if not underage_role in member.roles:
                        await member.add_roles(aboveage_role)
            await asyncio.sleep((breaktime*60))
            for member in self.groups[currentgroup]:
                r = await check_pomo_role(member)
            if len(self.groups[currentgroup]) != 0:
                member_ping = ''
                for member in self.groups[currentgroup]:
                    member_ping = member_ping + f"{member.mention}"
                await ctx.send(f"Your break time is over. Time to start studying again!\n{member_ping}")
            else:
                await ctx.send("This group is empty")
                del self.groups[currentgroup]
                self.activegroups -= 1
                return




    @commands.command()
    async def endpomo(self, ctx):
        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        pomo_role = discord.utils.get(ctx.guild.roles, id=897958571306811442)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)


        if pomo_role not in ctx.author.roles:
            await ctx.send("You are not currently in a pomodoro session.")
            return

        await ctx.author.remove_roles(pomo_role)
        self.groups[self.findgroup(ctx.author)].remove(ctx.author)
        if member_role not in ctx.author.roles:
            await ctx.author.add_roles(member_role)
        if study_role in ctx.author.roles:
            await ctx.author.remove_roles(study_role)
        if underage_role not in ctx.author.roles:
            await ctx.author.add_roles(aboveage_role)

        await ctx.send("You have been removed from the pomodoro session.")






    @commands.command()
    async def joinpomo(self, ctx, member:discord.Member=None):
        # global activegroups
        # global groups

        pomo_role = discord.utils.get(ctx.guild.roles, id=897958571306811442)

        if member == None:
            await ctx.send("Please name someone whose pomodoro session you would like to join.")
            return
        if self.activegroups == 0:
            await ctx.send("There are no ongoing pomodoro sessions at the moment. Try starting one with .startpomo")
            return
        membergroup = self.findgroup(member)
        if membergroup == None:
            await ctx.send("That session could not be found.")
            return

        self.groups[membergroup].append(ctx.author)
        await ctx.author.add_roles(pomo_role)
        await ctx.send("You have successfully joined that pomodoro session! Your permissions will sync up in the next cycle.")
        # perms sync up on next run







def setup(client):
    client.add_cog(Study(client))