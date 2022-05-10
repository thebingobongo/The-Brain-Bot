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
        study_realm = self.client.get_channel(895898369019478046)

        await ctx.send("Activated.")
        await study_realm.send(f"Hello {ctx.author.mention}. You have activated Study Mode, Good Luck!\n To exit use .unstudymode")

        member = ctx.author
        reason = 'study mode activated'

        await self.add_study_roles(ctx, member)
        # await member.remove_roles(member_role, reason=reason)
        # await member.add_roles(study_role, reason = "study mode activated.")
        # if aboveage_role in member.roles:
        #     await member.remove_roles(aboveage_role)
        await ctx.author.move_to(None)

    @commands.command()
    async def unstudymode(self,ctx):
        member = ctx.author

        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        pomo_role =discord.utils.get(ctx.guild.roles, id=897958571306811442)

        if study_role not in member.roles:
            await ctx.send("You are not currently in study mode.")
            return

        await ctx.send("Study Mode has been deactivated.")

        if pomo_role in member.roles:
            await member.remove_roles(pomo_role)
            await ctx.send("You have been removed from your pomodoro session as well.")
        await self.remove_study_roles(ctx,member)
        await ctx.author.move_to(None)

    def findgroup(self, member:discord.Member):

        for key in self.groups:
            for curr in self.groups[key]:
                if member == curr:
                    return key
        return None

    @commands.command(aliases=['activegroups'])
    async def showgroups(self,ctx):
        i=0
        embed = discord.Embed(title="Active Groups", color=ctx.author.color)
        if len(self.groups) == 0:
            await ctx.send("There are no active pomodoro groups right now.\n You can start one with .startpomo")
            return

        # print(self.groups)
        for key in self.groups:
            memberString=''
            # print(key)
            for member in self.groups[key]:
                memberString = memberString + member.name + "\n"
                # print(memberString)
            embed.add_field(name=f"Group number {i}", value=memberString)
        await ctx.send(embed=embed)

    async def add_study_roles(self,ctx, member:discord.Member):

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        aboveage_role = discord.utils.get(ctx.guild.roles, id=897665019913842768)
        staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
        mod_3_role = discord.utils.get(ctx.guild.roles, id=835623182484373535)

        await member.add_roles(study_role)
        await member.remove_roles(member_role)
        if aboveage_role in member.roles:
            await member.remove_roles(aboveage_role)
        if staff_role in member.roles:
            await member.remove_roles(staff_role)
            if mod_3_role in member.roles:
                await member.remove_roles(mod_3_role)


    async def remove_study_roles(self,ctx, member:discord.Member):

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        aboveage_role = discord.utils.get(ctx.guild.roles, id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)
        staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
        mod_1_role = discord.utils.get(ctx.guild.roles, id=831213087758614609)
        mod_2_role = discord.utils.get(ctx.guild.roles, id=831213644058329151)
        mod_3_role = discord.utils.get(ctx.guild.roles, id=835623182484373535)
        mels_role = discord.utils.get(ctx.guild.roles, id=885650021251444737)
        nosh_role = discord.utils.get(ctx.guild.roles, id=890059984203812924)
        wenis_role = discord.utils.get(ctx.guild.roles, id=885648963473121280)

        if mod_2_role in member.roles or mod_1_role in member.roles:
            await member.add_roles(staff_role)
        elif mels_role in member.roles or nosh_role in member.roles or wenis_role in member.roles:
            await member.add_roles(staff_role)
            await member.add_roles(mod_3_role)
        else:
            await member.add_roles(member_role)
        await member.remove_roles(study_role)
        if not underage_role in member.roles:
            await member.add_roles(aboveage_role)



    @commands.command(aliases=['pomodoro','startpomodorosession','startpomodoro'])
    async def startpomo(self, ctx, members: commands.Greedy[discord.Member],studytime:int=None, breaktime:int=None ):

        pom_tracker = self.client.get_channel(898047525188173854)
        self.activegroups += 1
        currentgroup = self.activegroups


        if studytime == None or breaktime == None:
            await ctx.send("How long would you like to study for? Try the command again with .studypomo [members] [studytime] [breaktime]")
            return

        if not members:
            members = [ctx.author]
        else:
            if ctx.author not in members:
                members.append(ctx.author)

        self.groups[currentgroup] = members

        pomo_role =discord.utils.get(ctx.guild.roles, id=897958571306811442)


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


        completed_poms = 0
        while len(self.groups[currentgroup]) > 0:

            # starts pomodoro for all members in the current group
            for member in self.groups[currentgroup]:
                result = await check_pomo_role(member)
                if result:
                    await self.add_study_roles(ctx, member)
            await asyncio.sleep((studytime*60))

            # starts break time
            completed_poms += 1
            for member in self.groups[currentgroup]:
                r = await check_pomo_role(member)
            if len(self.groups[currentgroup]) != 0:
                member_ping = ''
                for member in self.groups[currentgroup]:
                    member_ping = member_ping + f"{member.mention}"
                await ctx.send(f"Your study session has been completed, time to take a break!\n Your group has completed {completed_poms} study session(s)!\n {member_ping}")
            else:
                del self.groups[currentgroup]
                self.activegroups -= 1
                return

            # announces completed pom
            for member in self.groups[currentgroup]:
                if pomo_role not in member.roles:
                    try:
                        await members.remove(member)
                    except:
                        pass
                else:
                    await pom_tracker.send(f"{member.name} has completed a pomodoro study session!")
                    await self.remove_study_roles(ctx, member)
            if completed_poms % 4 == 0:
                await ctx.send(f"Your group has completed {completed_poms} sessions. Every fourth session you get a break twice as long as your previous ones ({breaktime*2} minutes)! Good work!")
                longer_break_time = breaktime * 2
                await asyncio.sleep((longer_break_time*60))
            else:
                await asyncio.sleep((breaktime*60))

            # ends break time, sets up next pom
            for member in self.groups[currentgroup]:
                r = await check_pomo_role(member)
            if len(self.groups[currentgroup]) != 0:
                member_ping = ''
                for member in self.groups[currentgroup]:
                    member_ping = member_ping + f"{member.mention}"
                await ctx.send(f"Your break time is over. Time to start studying again!\n{member_ping}")
            else:
                del self.groups[currentgroup]
                self.activegroups -= 1
                return

    @commands.command()
    async def endpomo(self, ctx):

        pomo_role = discord.utils.get(ctx.guild.roles, id=897958571306811442)

        if pomo_role not in ctx.author.roles:
            await ctx.send("You are not currently in a pomodoro session.")
            return

        await ctx.author.remove_roles(pomo_role)
        self.groups[self.findgroup(ctx.author)].remove(ctx.author)

        await self.remove_study_roles(ctx,ctx.author)

        await ctx.send("You have been removed from the pomodoro session.")

    @commands.command()
    async def joinpomo(self, ctx, member:discord.Member=None):

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        study_role = discord.utils.get(ctx.guild.roles, id=867540943217491978)
        pomo_role =discord.utils.get(ctx.guild.roles, id=897958571306811442)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)

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



        if study_role in member.roles:
            await ctx.author.add_roles(study_role)
            await ctx.author.remove_roles(member_role)
            if aboveage_role in ctx.author.roles:
                await ctx.author.remove_roles(aboveage_role)
        else:
            await ctx.author.add_roles(member_role)
            await ctx.author.remove_roles(study_role)
            if not underage_role in ctx.author.roles:
                await ctx.author.add_roles(aboveage_role)

        self.groups[membergroup].append(ctx.author)
        await ctx.author.add_roles(pomo_role)
        await ctx.send("You have successfully joined that pomodoro session!")



def setup(client):
    client.add_cog(Study(client))