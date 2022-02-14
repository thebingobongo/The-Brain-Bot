import discord
from discord.ext import commands
import typing
import asyncio

from databaselayer import *

def predicate(ctx):
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    return staff_role in ctx.author.roles or ctx.author.id == 339070790987284491
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_roles
    async def approve(self, ctx, member: discord.Member):
        if not member:
            await ctx.send("You need to name someone to approve.")
            return

        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        aboveage_placeholder_role = discord.utils.get(ctx.guild.roles, id=939060590188589057)
        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)

        if underage_role not in member.roles and aboveage_placeholder_role not in member.roles:
            m = await ctx.send("Please ask {member.name} to react to the age message.")
            await asyncio.sleep(30)
            await m.delete()
            return
            # await member.add_roles(aboveage_role)

        if aboveage_placeholder_role in ctx.author.roles:
            await member.add_roles(aboveage_role)
            await member.remove_roles(aboveage_placeholder_role)

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        sendchannel = self.client.get_channel(831211215878488078)
        try:
            createUser(member.id)
        except:
            updateUserRole(member.id, 831213206155952179)
        await member.add_roles(member_role)
        await ctx.send("User has been approved.")
        await sendchannel.send(
            " Welcome to **The Vat!**  :confetti_ball: \n {0.mention} \n If you run into issues in the server, please message  :brain: **The Brain** bot listed at the top of the user panel on the right. Make sure to grab some roles from <#831215253076574219>! Here, we are all brains in a vat, sharing our knowledge together in the virtual world of Discord!".format(
                member))

    @commands.command()
    @has_roles
    async def underage(self, ctx, member: discord.Member):
        if not member:
            await ctx.send("You need to name someone to approve.")
            return

        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)

        if aboveage_role in member.roles:
            await member.remove_roles(aboveage_role)

        await member.add_roles(underage_role)
        await ctx.send("Underage Tag has been added!")

    @commands.command()
    @has_roles
    async def notunderage(self, ctx, member: discord.Member):
        if not member:
            await ctx.send("You need to name someone to approve.")
            return

        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        aboveage_role = discord.utils.get(ctx.guild.roles,  id=897665019913842768)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)


        await member.remove_roles(underage_role)
        await member.add_roles(aboveage_role)
        await ctx.send("Underage Tag has been removed!")


    @commands.command(aliases=['woman','makewoman','givewoman'])
    @has_roles
    async def iswoman(self,ctx,member:discord.Member=None):
        if member == None:
            await ctx.send("Whos a woman?")
            return
        textchannel = self.client.get_channel(919810228621561867)
        await textchannel.set_permissions(member,
                                        view_channel=True,
                                        send_messages=True,
                                        add_reactions = True,
                                        attach_files = True,
                                        embed_links = True,
                                        use_external_emojis = True,
                                        read_messages = True,
                                        read_message_history = True,

                                                    )
        await ctx.send(f"{member} has been granted access to the women only channel.")


    @commands.command(aliases=["sew"])
    @has_roles
    async def mute(self, ctx, members: commands.Greedy[discord.Member],
                   mute_minutes: typing.Optional[int] = 0,
                   *, reason: str = "None"):
        """Mass mute members with an optional mute_minutes parameter to time it"""

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)


        if not members:
            await ctx.send("You need to name someone to mute")
            return

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        for member in members:
            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                return

            await member.remove_roles(member_role, reason=reason)

            if mute_minutes <= 0:
                time = "indefinitely."
            else:
                time = f"for {mute_minutes} minutes"

            await member.add_roles(muted_role, reason=reason)
            voice_state = member.voice

            if voice_state is not None:
                await member.edit(mute=True)
            await ctx.send(
                "{0.mention} has been muted by {1} for *{2}* {3}".format(member, ctx.author, reason,
                                                                                 time))
        # logs = self.client.get_channel(831214657439924284)
        # await logs.send(
        #     "{0.mention} has been muted by {1} for *{2}* {3}".format(member, ctx.author, reason,
        #                                                                      time))
        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send(
            "{0.mention} has been muted by {1} for *{2}* {3}".format(member, ctx.author, reason,
                                                                     time))
        if mute_minutes > 0:
            await asyncio.sleep(mute_minutes * 60)
            for member in members:
                if not muted_role in member.roles:
                    continue
                else:
                    await member.remove_roles(muted_role, reason="time's up ")
                    voice_state = member.voice
                    if voice_state is not None:
                        await member.edit(mute=False)
                    await member.add_roles(member_role, reason=reason)
                    await userlogs.send(f"{member.mention} has been unmuted.")

    @commands.command()
    @has_roles
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)

        if not member:
            await ctx.send("You need to name someone to unmute.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        await member.add_roles(member_role, reason=reason)
        await member.remove_roles(muted_role, reason=reason)

        voice_state = member.voice
        if voice_state is not None:
            await member.edit(mute=False)
        await ctx.send(
            "{0.mention} has been unmuted by {1} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(934867511273476177)
        await logs.send("{0.mention} has been unmuted by {1} for *{2}* ".format(member, ctx.author, reason))

    @commands.command(aliases=['unpunish', 'unpanopticon', 'unprison'])
    @has_roles
    async def undungeon(self, ctx, member: discord.Member, *, reason=None):
        dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")
        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)

        if not member:
            await ctx.send("You need to name someone to unpunish.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        await member.add_roles(member_role, reason=reason)
        await member.remove_roles(dungeon_role, reason=reason)
        await member.move_to(None)
        await ctx.send(
            "{0.mention} has been unpunished by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(934867511273476177)
        await logs.send("{0.mention} has been unpunished by {1.mention} for *{2}* ".format(member, ctx.author, reason))

    @commands.command(aliases=['punish', 'prison', 'panopticon'])
    @has_roles
    async def dungeon(self, ctx, members: commands.Greedy[discord.Member],
                      dungeon_minutes: typing.Optional[int] = 0,
                      *, reason: str = "None"):
        """Mass mute members with an optional mute_minutes parameter to time it"""

        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)


        if not members:
            await ctx.send("You need to name someone to punish.")
            return

        dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")

        for member in members:
            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                return

            await member.add_roles(member_role, reason=reason)

            if dungeon_minutes <= 0:
                time = "indefinitely."
            else:
                time = f"for {dungeon_minutes} minutes."

            await member.add_roles(dungeon_role, reason=reason)
            await member.move_to(None)
            await ctx.send(
                "{0.mention} has been punished by {1} for *{2}* {3}".format(member, ctx.author,
                                                                                    reason, time))
        # logs = self.client.get_channel(831214657439924284)
        # await logs.send("{0.mention} has been punished by {1} for *{2}* {3}".format(member, ctx.author,
        #                                                                                      reason, time))

        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send("{0.mention} has been punished by {1} for *{2}* {3}".format(member, ctx.author,
                                                                                             reason, time))

        if dungeon_minutes > 0:
            await asyncio.sleep(dungeon_minutes * 60)
            for member in members:
                if not dungeon_role in member.roles:
                    continue
                else:
                    await member.remove_roles(dungeon_role, reason="time's up ")
                    await member.add_roles(member_role, reason="times up")

                    await userlogs.send(f"{member.mention} has been released from the Panopticon.")

    @commands.command()
    @has_roles
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not member:
            await ctx.send("You need to name someone to kick.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
        if staff_role in member.roles:
            await ctx.send("Cannot kick staff. Please contact a Mod III")
            return
        await ctx.send("{0.mention} has been kicked by {1} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been kicked by {1} for *{2}* ".format(member, ctx.author, reason))

        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send("{0.mention} has been kicked by {1} for *{2}* ".format(member, ctx.author, reason))
        await member.kick(reason=reason)


    @commands.command()
    @has_roles
    async def ban(self, ctx, member: discord.Member,time_to_ban=None, *, reason=None):
        if not member:
            await ctx.send("You need to name someone to ban.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
        if staff_role in member.roles:
            await ctx.send("Cannot ban staff. Please contact a Mod III")
            return
        if time_to_ban == None:
            time_to_ban = 5
        elif time_to_ban.isdigit():
            time_to_ban = int(time_to_ban)
        else:
            reason = str(time_to_ban) + reason
            time_to_ban = 5
        await ctx.send(
            f" <a:vibing:847619864738267217> <a:vibing:847619864738267217> {member.mention} is gonna get banned in {time_to_ban} seconds!!!! <a:vibing:847619864738267217> <a:vibing:847619864738267217>")
        for i in range(time_to_ban):
            await ctx.send(f"{member.mention} is gone in {time_to_ban - i} seconds <a:vibing:847619864738267217>")
            await asyncio.sleep(1)
        await member.ban(reason=reason)
        await ctx.send(
            f"<a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217> {member.display_name} IS GONE NOW! <a:vibing:847619864738267217><a:vibing:847619864738267217><a:vibing:847619864738267217>")

        # await member.ban(reason=reason)
        # await ctx.send("{0.mention} has been banned by {1} for *{2}* ".format(member, ctx.author, reason))

        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been banned by {1} for *{2}* ".format(member, ctx.author, reason))
        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send("{0.mention} has been banned by {1} for *{2}* ".format(member, ctx.author, reason))

    @commands.command()
    @has_roles
    async def promote(self, ctx, member: discord.Member, *, reason='Promotion'):
        if not member:
            await ctx.send("You need to name someone to promote.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
        bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
        knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
        pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
        member_role = discord.utils.get(ctx.guild.roles, id=835286042176127027)
        if rook_role in member.roles:
            await ctx.send("{0.mention} is already a Rook!".format(member))
        elif bishop_role in member.roles:
            await member.remove_roles(bishop_role, reason=reason)
            await member.add_roles(rook_role, reason=reason)
            updateUserRole(member.id, 831227767671619636)
            await ctx.send("{0.mention} has been promoted to Rook!".format(member))
        elif knight_role in member.roles:
            await member.remove_roles(knight_role, reason=reason)
            await member.add_roles(bishop_role, reason=reason)
            await ctx.send("{0.mention} has been promoted to Bishop!".format(member))
            updateUserRole(member.id, 831213133066534993)
        elif pawn_role in member.roles:
            await member.remove_roles(pawn_role, reason=reason)
            await member.add_roles(knight_role, reason=reason)
            await ctx.send("{0.mention} has been promoted to Knight!".format(member))
        elif member_role in member.roles:
            await member.add_roles(pawn_role, reason=reason)
            await ctx.send("{0.mention} has been promoted to Pawn!".format(member))
        else:
            await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")
            return

        # logs = self.client.get_channel(831214657439924284)
        # await logs.send("{0.mention} has been promoted by {1}.".format(member, ctx.author))

        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send("{0.mention} has been promoted by {1}.".format(member, ctx.author))


    @commands.command()
    @commands.has_role(831214459682029588)
    async def demote(self, ctx, member: discord.Member, *, reason='Demotion'):
        if not member:
            await ctx.send("You need to name someone to demote.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
        bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
        knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
        pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
        if rook_role in member.roles:
            await member.remove_roles(rook_role, reason=reason)
            await member.add_roles(bishop_role, reason=reason)
            await ctx.send("{0.mention} has been demoted to bishop.".format(member))
            updateUserRole(member.id, 831213133066534993)
        elif bishop_role in member.roles:
            await member.remove_roles(bishop_role, reason=reason)
            await member.add_roles(knight_role, reason=reason)
            await ctx.send("{0.mention} has been demoted to a Knight.".format(member))
            updateUserRole(member.id, 831213165105643520)
        elif knight_role in member.roles:
            await member.remove_roles(knight_role, reason=reason)
            await member.add_roles(pawn_role, reason=reason)
            await ctx.send("{0.mention} has been demoted to Pawn.".format(member))
            updateUserRole(member.id, 831213206155952179)
        elif pawn_role in member.roles:
            await member.remove_roles(pawn_role, reason=reason)
            await ctx.send("{0.mention} has been demoted to Member.".format(member))
        else:
            await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")
            return

        # logs = self.client.get_channel(831214657439924284)
        # await logs.send("{0.mention} has been demoted by {1}.".format(member, ctx.author))

        userlogs = self.client.get_channel(934867511273476177)
        await userlogs.send("{0.mention} has been demoted by {1}.".format(member, ctx.author))

    @commands.command(aliases=['gbr', 'brainrole'])
    @has_roles
    async def givebrainrole(self, ctx, member: discord.Member, *, role_id=None):
        if not member:
            await ctx.send("You need to name someone to demote.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        if role_id == None:
            await ctx.send("Please specify which brain role you want to give to this user.")
            await ctx.send('''.
                1. Biology 
                2. Business 
                3. Computer Science 
                4. Chemistry 
                5. Chef 
                6. Chess God 
                7. Debate Club 
                8. Economics 
                9. Engineering 
                10. Healthcare 
                11. History 
                12. History of Phil. 
                13. International Relations 
                14. Language 
                15. Metaethics 
                16. Maths 
                17. Metaphysics 
                18. Philosophy 
                19. Phil. of Mind 
                20. Physics 
                21. Political Science 
                22. Psychology 
                23. Religion 
                24. Literature
            ''')
            return
        else:
            role_id = int(role_id)
            if role_id == 1:
                role = 'Biology'
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=843667880519663686))
            elif role_id == 2:
                role = "Business"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835050210111651850))
            elif role_id == 3:
                role = "Computer Science"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835273070817181757))
            elif role_id == 4:
                role = "Chemistry"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=838589075128451102))
            elif role_id == 5:
                role = "Chef"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=843668667785936906))
            elif role_id == 6:
                role = "Chess God"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=836440277680914443))
            elif role_id == 7:
                role = "Debate Club"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835049191876198431))
            elif role_id == 8:
                role = "Economics"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=838589029694963723))
            elif role_id == 9:
                role = "Engineering"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=843314823810777108))
            elif role_id == 10:
                role = "Healthcare"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835412225669464074))
            elif role_id == 11:
                role = "History"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835272854601203712))
            elif role_id == 12:
                role = "History of Phil."
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835276025410879529))
            elif role_id == 13:
                role = "International Relations"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=839976074175709275))
            elif role_id == 14:
                role = "Language"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835274951505477684))
            elif role_id == 15:
                role = "Metaethics"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835049730001600542))
            elif role_id == 16:
                role = "Maths"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=836802292346781717))
            elif role_id == 17:
                role = "Metaphysics"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275452796239932))
            elif role_id == 18:
                role = "Philosophy"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=843668608898301973))
            elif role_id == 19:
                role = "Phil. of Mind"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275301025742909))
            elif role_id == 20:
                role = "Physics"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=836802289371971647))
            elif role_id == 21:
                role = "Political Science"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=838588978788958288))
            elif role_id == 22:
                role = "Psychology"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835050296837275658))
            elif role_id == 23:
                role = "Religion"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=835275048041447504))
            elif role_id == 24:
                role = "Literature"
                await member.add_roles(discord.utils.get(ctx.guild.roles, id=843673099807621155))

            await ctx.send(
                "{0.mention} has been awarded the brain role for {1} by {2}".format(member, role, ctx.author))
            logs = self.client.get_channel(831214657439924284)
            await logs.send(
                "{0.mention} has been awarded the brain role for {1} by {2}".format(member, role, ctx.author))

            userlogs = self.client.get_channel(934867511273476177)
            await userlogs.send(
                "{0.mention} has been awarded the brain role for {1} by {2}".format(member, role, ctx.author))

    @commands.command()
    @has_roles
    async def movetolounge(self, ctx):
        currentvc = ctx.author.voice.channel
        thelounge = discord.utils.get(ctx.guild.channels, id=831211215878488082)
        await ctx.send(f"moving members from {currentvc} to {thelounge}.")
        for member in currentvc.members:
            await member.move_to(thelounge)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def movetoquietroom(self, ctx):
        currentvc = ctx.author.voice.channel
        qroom = discord.utils.get(ctx.guild.channels, id=831216042725343282)
        await ctx.send(f"moving members from {currentvc} to {qroom}.")
        for member in currentvc.members:
            await member.move_to(qroom)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def movetodiscussion(self, ctx):
        currentvc = ctx.author.voice.channel
        discussion = discord.utils.get(ctx.guild.channels, id=831211215878488083)
        await ctx.send(f"moving members from {currentvc} to {discussion}.")
        for member in currentvc.members:
            await member.move_to(discussion)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def movetoadultclub(self, ctx):
        currentvc = ctx.author.voice.channel
        adultclub = discord.utils.get(ctx.guild.channels, id=839253190667141181)
        await ctx.send(f"moving members from {currentvc} to {adultclub}.")
        for member in currentvc.members:
            await member.move_to(adultclub)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def movetogaming(self, ctx):
        currentvc = ctx.author.voice.channel
        gaming = discord.utils.get(ctx.guild.channels, id=831211216277733436)
        await ctx.send(f"moving members from {currentvc} to {gaming}.")
        for member in currentvc.members:
            await member.move_to(gaming)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def movetomedia(self, ctx):
        currentvc = ctx.author.voice.channel
        media = discord.utils.get(ctx.guild.channels, id=838631088959651850)
        await ctx.send(f"moving members from {currentvc} to {media}.")
        for member in currentvc.members:
            await member.move_to(media)
        await ctx.send("Done.")

    @commands.command()
    @has_roles
    async def reply(self,ctx,member:discord.Member = None, *,message=None ):
        if member == None:
            await ctx.send("Name a member to reply to.")
            return
        if message == None:
            await ctx.send(f"What do you want to say to {member.display_name}?")
            return
        if not hasOpenTicket(member.id):
            await ctx.send(f"{member.name} has no open tickets.")
            return
        embed = discord.Embed(title=f"{ctx.author.display_name} says:", colour=0x00ff00)
        embed.add_field(name=message, value="** **")
        await member.send(embed=embed)
        await ctx.send("Message sent.")

    @commands.command()
    @has_roles
    async def closeticket(self,ctx, member:discord.Member):
        if hasOpenTicket(member.id):
            closeTicket(member.id)
            embed= discord.Embed(title="Your ticket has been closed.",colour=0xff0000)
            embed.add_field(name="If you are not satisfied with our response, reply below, or contact a MOD 3 within The Vat.",value="** **")
            await member.send(embed=embed)
            await ctx.send("Ticket has successfully been closed.")
        else:
            await ctx.send("No open tickets for that member.")


    @commands.command()
    @has_roles
    async def opentickets(self, ctx):
        opentickets = openTickets()
        embed = discord.Embed(title="Open Tickets", colour=0x00ff00)
        for ticket in opentickets:
            try:
                user = self.client.get_user(int(ticket[0]))

                embed.add_field(name=user.display_name,value="** **")
            except:
                print(f'failed for {ticket[0]}')
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

            # Checking if its a dm channel
        if isinstance(message.channel, discord.DMChannel):
            # Getting the channel

            # --------------------------------------------------------------------------------
            # CONFESSION STUFF
            # DELETE AFTER EVENT IS OVER
            if message.content.startswith(".confess "):
                return
            # ---------------------------------------------------------------------------------

            sendchannel = self.client.get_channel(831214657439924284)
            embedVar = discord.Embed(title="BOT RECIEVED DM", color=0x00ff00)
            embedVar.add_field(name=f"{message.author} sent the bot:",
                               value=f"{message.content}", inline=False)
            embedVar.set_footer(text=f"Member discord ID is {message.author.id}")
            await sendchannel.send(embed=embedVar)
            if not hasOpenTicket(message.author.id):
                embedVar1 = discord.Embed(title="Ticket created", color=0x00ff00)
                embedVar1.add_field(name="Mods will solve the issue as soon as possible. Thanks.",
                                    value="Please refrain from sending too many messages here.", inline=False)
                await message.channel.send(embed=embedVar1)
                createTicket(message.author.id)

        msg = message.content

        filteredwords = ['nigger', 'nigga', 'faggot', 'testbingobongo', 'niggers', 'fag', 'fagging', 'faggitt',
                         'faggot', 'retarded', 'r3tarded', 'r3tard3d',
                         'faggs', 'fagot', 'fagots', 'fags', 'dyke', 'n1gga', 'n1gger', 'nigg3r', 'nigg4h', 'nigga',
                         'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'retard', 'assnigger', 'douche-fag',
                         'negro', 'fagbag','goyim', 'goyum', 'gringo', 'mutt', 'Kike',
                         'fagfucker', 'faggit', 'faggotcock', 'fagtard', 'mc faggot', 'mcfaggot', 'mcfagget',
                         'nigaboo', 'niglet', 'sand nigger', 'sandnigger', 'darkie', 'sand nigga', 'niggerfucker',
                         'pissnigger', 'pissnigga', 'lolli', 'loli', 'porch monkey', 'porchmonkey',
                         'porch-monkey', 'bluegum', 'ching-chong', 'dog-eater',
                         'cat-eater', 'chink', 'cholo', 'chinky',
                         'Chink', 'Cholo', 'Chinky', 'jigaboo', 'jiggaboo', 'retards',
                         'injun', '1njun', 'jewboy', 'kyke', 'pickaninny',
                         'polack','polak', 'polack', 'tacohead', 'thicklips', 'thicklips',
                         'uncle-tom', 'Wigger','wigga', "moretesting",
                         'zipperhead', 'zippahead', 'zipper-head', 'zippa-head']

        msgwords = msg.split()
        for msgword in msgwords:
            msgword = msgword.replace("?", "")
            msgword = msgword.replace("!", "")
            msgword = msgword.replace(".", "")
            msgword = msgword.replace("*", "")
            msgword = msgword.replace("/", "")
            msgword = msgword.replace("|", "")
            msgword = msgword.replace("`", "")
            msgword = msgword.replace("~", "")

            for filter in filteredwords:
                # print(f'{msgword} {filter}')
                if msgword.lower() == filter.lower():
                    await message.delete()
                    sendchannel = self.client.get_channel(831214657439924284)
                    embedVar2 = discord.Embed(title="Filtered Message:", color=0xff0000)
                    embedVar2.add_field(name=f"{message.author} said in {message.channel}:",
                                        value=f"{message.content} \n \n Word = **{msgword}**", inline=False)
                    await sendchannel.send(embed=embedVar2)
                    break
            if msgword.lower() in ["bingo", "bingobongo", "<:bingo:838288733748461588>"]:
                await message.add_reaction("<:bingo:838288733748461588>")
            elif msgword.lower() in ["gag", "<:gag:837859560566816788>"]:
                await message.add_reaction("<:gag:837859560566816788>")
            elif msgword.lower() in ["brain", "<:happybrain:838485449512452157>", "vat"]:
                await message.add_reaction("<:happybrain:838485449512452157>")
            elif msgword.lower() in ["canada", 'toronto', 'eh', 'timmies', 'tims', "timbits", 'hortons', 'maple', 'poutine', 'beiber', 'drake']:
                await message.add_reaction("🍁")
            elif msgword.lower() == "<:feelsbadeh:854187237356863489>":
                await message.add_reaction("<:feelsbadeh:854187237356863489>")
            elif msgword.lower() in ["wenis", 'wemis', 'wamis', 'wanis','wnais', 'wensi','wemsi',"l" , 'millian', '<:wenis:838097027392864316>']:
                await message.add_reaction("<:wenis:838097027392864316>")
            elif msgword.lower() in ['mel', 'miffy', 'hgc', 'grapefruit','<:melmelmelmelmel:912462443354128384>']:
                await message.add_reaction('<:melmelmelmelmel:912462443354128384>')
            elif msgword.lower() in ['marz','barz', '<:marzbarz:867622876004745236>', 'marzbarz']:
                await message.add_reaction('<:marzbarz:867622876004745236>')
            elif msgword.lower() in ['nosh', 'lyra', 'delusional', 'despicable', "<:nosh:920397187081457727>"]:
                await message.add_reaction('<:nosh:920397187081457727>')
            elif msgword.lower() == '<:fuckthemods:912130927231111268>':
                await message.add_reaction('<:fucktheusers:912130974886801439>')
            elif msgword.lower() in ['joseph', 'josephs','wbfrcu','🍉']:
                await message.add_reaction('🍉')
            elif msgword.lower() in ['vinnie', 'vinchenzo', 'vin', 'osito']:
                await message.add_reaction("<:vinnie2:925188230150758432>")
            elif msgword.lower() in ['sterg', 'stergiara', 'mizkif']:
                await message.add_reaction('<:patrick:840390533892407296>')
            elif msgword.lower() in ['emi', 'artemida', 'emii', 'emiii', 'aviata']:
                await message.add_reaction('💖')
            elif msgword.lower() in ['sen', 'swole']:
                await message.add_reaction('<:sen:936785558703853578>')


        try:
            if msg[0] == ":" and msg[-1] == ":":
                emotename = msg[1:-1]
                thevat = self.client.get_guild(831211215375433728)
                for emote in thevat.emojis:
                    if emotename == emote.name:
                        await message.delete()
                        await message.channel.send(str(emote))
        except:
            pass

        if 'discord.gg' in message.content:
            if message.guild.id == 831211215375433728:
                # await message.channel.send(f"{message.channel.category_id} == 831211215375433731")
                staffrole = discord.utils.get(message.guild.roles, id=831214459682029588)
                if staffrole not in message.author.roles:

                    if message.channel.id != 838442788021993484 and message.channel.category_id != 831211215375433731 and message.author.id != 819778342818414632:
                        await message.delete()
                        embed = discord.Embed(
                            title="Sorry, that isn't allowed here. Contact a mod if you would like to partner.",
                            colour=0xff0000)
                        embed.add_field(name="If you need an invite to the Vat, try .invite.", value="** **")
                        embed.set_footer(text="DM me or any mods for problems/questions!")
                        await message.channel.send(embed=embed)
                        sendchannel = self.client.get_channel(831214657439924284)
                        embedVar2 = discord.Embed(title="Filtered Message:", color=0xff0000)
                        embedVar2.add_field(name=f"{message.author} sent an invite in {message.channel}:",
                                            value=f"{message.content}", inline=False)
                        await sendchannel.send(embed=embedVar2)


def setup(client):
    client.add_cog(Moderation(client))