import discord
from discord.ext import commands
import typing
import asyncio

from databaselayer import *

def predicate(ctx):
    staff_role = discord.utils.get(ctx.guild.roles, id=831214459682029588)
    return staff_role in ctx.author.roles
    # test = discord.utils.get(ctx.guild.roles, id=858614845363322881)
    # return test in ctx.author.roles


has_roles = commands.check(predicate)


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['verify'])
    @has_roles
    async def approve(self, ctx, member: discord.Member):
        if not member:
            await ctx.send("You need to name someone to approve.")
            return

        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)
        sendchannel = self.client.get_channel(831211215878488078)
        try:
            createUser(member.id)
        except:
            updateUserRole(member.id, 831213206155952179)
        await member.add_roles(pawn_role)
        await ctx.send("User has been approved.")
        await sendchannel.send(
            " Welcome to **The Vat!**  :confetti_ball: \n {0.mention} \n If you run into issues in the server, please message  :brain: **The Brain** bot listed at the top of the user panel on the right.  Here, we are all brains in a vat, sharing our knowledge together in the virtual world of Discord!".format(
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

        textchannel = self.client.get_channel(839252122550009876)
        voicechannel = self.client.get_channel(839253190667141181)
        underage_role = discord.utils.get(ctx.guild.roles, id=839245778136072293)
        await member.add_roles(underage_role)
        await textchannel.set_permissions(member, view_channel=False)
        await voicechannel.set_permissions(member, view_channel=False)
        await ctx.send("Underage Tag has been added!")

    @commands.command()
    @has_roles
    async def mute(self, ctx, members: commands.Greedy[discord.Member],
                   mute_minutes: typing.Optional[int] = 5,
                   *, reason: str = "None"):
        """Mass mute members with an optional mute_minutes parameter to time it"""

        rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
        bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
        knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
        pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)


        if not members:
            await ctx.send("You need to name someone to mute")
            return

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        for member in members:
            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                return
            if rook_role in member.roles:
                await member.remove_roles(rook_role, reason=reason)
            elif bishop_role in member.roles:
                await member.remove_roles(bishop_role, reason=reason)
            elif knight_role in member.roles:
                await member.remove_roles(knight_role, reason=reason)
            elif pawn_role in member.roles:
                await member.remove_roles(pawn_role, reason=reason)

            if mute_minutes == 0:
                time = "indefinitely."
            else:
                time = f"for {mute_minutes} minutes"

            await member.add_roles(muted_role, reason=reason)
            voice_state = member.voice

            if voice_state is not None:
                await member.edit(mute=True)
            await ctx.send(
                "{0.mention} has been muted by {1.mention} for *{2}* {3}".format(member, ctx.author, reason,
                                                                                 time))
        logs = self.client.get_channel(831214657439924284)
        await logs.send(
            "{0.mention} has been muted by {1.mention} for *{2}* {3}".format(member, ctx.author, reason,
                                                                             time))
        if mute_minutes > 0:
            await asyncio.sleep(mute_minutes * 60)
            for member in members:
                if muted_role in member.roles:
                    continue
                else:
                    await member.remove_roles(muted_role, reason="time's up ")
                    voice_state = member.voice
                    if voice_state is not None:
                        await member.edit(mute=False)
                    roleid = int(getUserRole(member.id))
                    try:
                        memberrole = discord.utils.get(ctx.guild.roles, id=roleid)
                        await member.add_roles(memberrole, reason=reason)
                    except:
                        pass
                    await ctx.send(f"{member.mention} has been unmuted.")
                    await logs.send(f"{member.mention} has been unmuted.")

    @commands.command()
    @has_roles
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not member:
            await ctx.send("You need to name someone to unmute.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return

        roleid = int(getUserRole(member.id))
        try:
            member_role = discord.utils.get(ctx.guild.roles, id=roleid)
            await member.add_roles(member_role, reason='unmuted')
        except Exception as e:
            pass
        await member.remove_roles(muted_role, reason=reason)

        voice_state = member.voice
        if voice_state is not None:
            await member.edit(mute=False)
        await ctx.send(
            "{0.mention} has been unmuted by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been unmuted by {1.mention} for *{2}* ".format(member, ctx.author, reason))


    @commands.command(aliases=['unpunish', 'unpanopticon', 'unprison'])
    @has_roles
    async def undungeon(self, ctx, member: discord.Member, *, reason=None):
        dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")
        if not member:
            await ctx.send("You need to name someone to unpunish.")
            return
        if member == self.client.user:
            await ctx.send("You cannot do that to me, young one.")
            return
        roleid = int(getUserRole(member.id))
        try:
            member_role = discord.utils.get(ctx.guild.roles, id=roleid)
            await member.add_roles(member_role, reason='unmuted')
        except Exception as e:
            pass
        await member.remove_roles(dungeon_role, reason=reason)
        await ctx.author.move_to(None)
        await ctx.send(
            "{0.mention} has been unpunished by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been unpunished by {1.mention} for *{2}* ".format(member, ctx.author, reason))


    @commands.command(aliases=['punish', 'prison', 'panopticon'])
    @has_roles
    async def dungeon(self, ctx, members: commands.Greedy[discord.Member],
                      dungeon_minutes: typing.Optional[int] = 0,
                      *, reason: str = "None"):
        """Mass mute members with an optional mute_minutes parameter to time it"""

        rook_role = discord.utils.get(ctx.guild.roles, id=831227767671619636)
        bishop_role = discord.utils.get(ctx.guild.roles, id=831213133066534993)
        knight_role = discord.utils.get(ctx.guild.roles, id=831213165105643520)
        pawn_role = discord.utils.get(ctx.guild.roles, id=831213206155952179)


        if not members:
            await ctx.send("You need to name someone to punish.")
            return

        dungeon_role = discord.utils.get(ctx.guild.roles, name="Punished")

        for member in members:
            if member == self.client.user:
                await ctx.send("You cannot do that to me, young one.")
                return
            if rook_role in member.roles:
                await member.remove_roles(rook_role, reason=reason)
            elif bishop_role in member.roles:
                await member.remove_roles(bishop_role, reason=reason)
            elif knight_role in member.roles:
                await member.remove_roles(knight_role, reason=reason)
            elif pawn_role in member.roles:
                await member.remove_roles(pawn_role, reason=reason)

            if dungeon_minutes == 0:
                time = "indefinitely."
            else:
                time = f"for {dungeon_minutes} minutes."

            await member.add_roles(dungeon_role, reason=reason)
            await ctx.author.move_to(None)
            await ctx.send(
                "{0.mention} has been punished by {1.mention} for *{2}* {3}".format(member, ctx.author,
                                                                                    reason, time))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been punished by {1.mention} for *{2}* {3}".format(member, ctx.author,
                                                                                             reason, time))
        if dungeon_minutes > 0:
            await asyncio.sleep(dungeon_minutes * 60)
            for member in members:
                if dungeon_role in member.roles:
                    continue
                else:
                    await member.remove_roles(dungeon_role, reason="time's up ")
                    roleid = int(getUserRole(member.id))
                    try:
                        member_role = discord.utils.get(ctx.guild.roles, id=roleid)
                        await member.add_roles(member_role, reason=reason)
                    except:
                        pass
                    await ctx.send(f"{member.mention} has been released from the Panopticon.")
                    await logs.send(f"{member.mention} has been released from the Panopticon.")

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
        await ctx.send("{0.mention} has been kicked by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been kicked by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        await member.kick(reason=reason)


    @commands.command()
    @has_roles
    async def ban(self, ctx, member: discord.Member, *, reason=None):
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
        await member.ban(reason=reason)
        await ctx.send("{0.mention} has been banned by {1.mention} for *{2}* ".format(member, ctx.author, reason))
        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been banned by {1.mention} for *{2}* ".format(member, ctx.author, reason))


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
        elif member_role in member.roles:
            await member.remove_roles(pawn_role, reason=reason)
            await member.add_roles(knight_role, reason=reason)
            await ctx.send("{0.mention} has been promoted to Knight!".format(member))
            updateUserRole(member.id, 831213165105643520)
        elif pawn_role in member.roles:
            await member.add_roles(member_role, reason=reason)
            await ctx.send("{0.mention} has been promoted to Member!".format(member))
        else:
            await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")

        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been promoted by {1.mention}.".format(member, ctx.author))

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
            await ctx.send("{0.mention} is a Pawn. Cannot be further demoted.".format(member))
        else:
            await ctx.send("There was an error. Either that member is a Mod, or is not a pawn yet.")

        logs = self.client.get_channel(831214657439924284)
        await logs.send("{0.mention} has been demoted by {1.mention}.".format(member, ctx.author))

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
                "{0.mention} has been awarded the brain role for {1} by {2.mention}".format(member, role, ctx.author))
            logs = self.client.get_channel(831214657439924284)
            await logs.send(
                "{0.mention} has been awarded the brain role for {1} by {2.mention}".format(member, role, ctx.author))


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
        embed = discord.Embed(title=f"{ctx.author.display_name} says:",colour=0x00ff00)
        embed.add_field(name=message,value="** **")
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

            # Checking if its a dm channel
        if isinstance(message.channel, discord.DMChannel):
            # Getting the channel
            sendchannel = self.client.get_channel(831214657439924284)
            embedVar = discord.Embed(title="BOT RECIEVED DM", color=0x00ff00)
            embedVar.add_field(name=f"{message.author} sent the bot:",
                               value=f"{message.content}", inline=False)
            await sendchannel.send(embed=embedVar)
            if not hasOpenTicket(message.author.id):
                embedVar1 = discord.Embed(title="Ticket created", color=0x00ff00)
                embedVar1.add_field(name="Mods will solve the issue as soon as possible. Thanks.",
                                    value="Please refrain from sending too many messages here.", inline=False)
                await message.channel.send(embed=embedVar1)
                createTicket(message.author.id)

        msg = message.content

        filteredwords = ['nigger', 'nigga', 'faggot', 'testbingobongo', 'niggers', 'fag', 'fagging', 'faggitt',
                         'faggot',
                         'faggs', 'fagot', 'fagots', 'fags', 'dyke', 'n1gga', 'n1gger', 'nigg3r', 'nigg4h', 'nigga',
                         'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'retard', 'assnigger', 'douche-fag',
                         'fagbag',
                         'fagfucker', 'faggit', 'faggotcock', 'fagtard', 'mc faggot', 'mcfaggot', 'mcfagget',
                         'negro',
                         'nigaboo', 'niglet', 'sand nigger', 'sandnigger', 'darkie', 'sand nigga', 'niggerfucker',
                         'pissnigger', 'pissnigga', 'lolli', 'loli', 'porch monkey', 'porchmonkey',
                         'porch-monkey', 'bluegum', 'boonga', 'cabbage eater', 'ching-chong', 'dog-eater',
                         'dog eater',
                         'cat-eater', 'cat eater', 'Ching Chong', 'ching chong', 'chink', 'cholo', 'chinky',
                         'Chink', 'Cholo', 'Chinky', 'jigaboo', 'jiggaboo', 'retards',
                         'gin jockey', 'goyim', 'goyum', 'gringo', 'mutt', 'honky', 'honkey', 'honkie', 'Kike',
                         'injun', '1njun', 'jewboy', 'kyke', 'mayo monkey', 'mayonnaise monkey', 'pickaninny',
                         'polack',
                         'polak', 'polack', 'prarie nigger', 'prarie nigga', 'tacohead', 'thicklips', 'thicklips',
                         'thick lips', 'ting tong', 'towel head', 'twink', 'uncle tom', 'uncle-tom', 'Wigger',
                         'wigga', "moretesting",
                         'zipperhead', 'zippahead', 'zipper-head', 'zippa-head', 'twinks']

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
            if msgword.lower() in ["gag", "<:gag:837859560566816788>"]:
                await message.add_reaction("<:gag:837859560566816788>")
            if msgword.lower() in ["brain", "<:happybrain:838485449512452157>", "vat"]:
                await message.add_reaction("<:happybrain:838485449512452157>")
            if msgword.lower() in ["canada", 'toronto', 'eh', 'timmies', 'tims', "timbits"]:
                await message.add_reaction("🍁")
            if msgword.lower() == "<:feelsbadeh:854187237356863489>":
                await message.add_reaction("<:feelsbadeh:854187237356863489>")

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


    # @commands.command()
    # @has_roles
    # async def testingmod(selfself,ctx):
    #     await ctx.send("it works")


def setup(client):
    client.add_cog(Moderation(client))