import discord
import requests
import keep_alive
import time
def get_blacklist(guildid, guildlist, blacklists):
      return blacklists[guildlist.index(guildid)]
def get_guild(guildid, guildlist):
      return guildlist.index(guildid)

client = discord.Client()
blacklists = [[],[],[]]
onlist = [True, True, True]
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '#KickBotOff' in message.content:
        await message.channel.send("Kick Bot Turned Off")
        onlist[get_guild(message.guild.id, [x.id for x in client.guilds])] = False
    if '#KickBotOn' in message.content:
        await message.channel.send("Kick Bot Turned On!")
        await message.channel.send("Current blacklist:")
        for user in get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists):
            await message.channel.send(user)
            await message.guild.get_member(user[1]).move_to(None,reason="Because ur gay")
        onlist[get_guild(message.guild.id, [x.id for x in client.guilds])] = True
    if '#Show Blacklist' in message.content:
        await message.channel.send("Current blacklist:")
        for user in get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists):
            await message.channel.send(user[0])
    if '#Add Blacklist' in message.content[:14]:
        #print(message.content[15:])
        #print([x.id for x in client.guilds])
        #print(blacklists)
        for sublist in get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists):
            if message.content[15:] == sublist[0]:
                await message.channel.send("This member is already in the blacklist!")
                return
        for member in message.guild.members:
            if message.content[15:] == member.nick:
                get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists).append([member.nick, member.id])
                await message.channel.send("User added!")
                return
        await message.channel.send("User doesn't exist!")
    if '#Remove Blacklist' in message.content[:17]:
        for sublist in range(len(get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists))):
            if message.content[18:] == get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists)[sublist][0]:
                get_blacklist(message.guild.id, [x.id for x in client.guilds], blacklists).pop(sublist)
                await message.channel.send(message.content[18:] + " removed!")
            return
    if '#RPT' in message.content:
        await message.channel.send("RPT " + message.content[5:])
        MEME_POST = {
            'template_id': 61516,
            'username': 'sunnyk',
            'password': 'Kissme77',
            'text0': 'RAPTOR PRO TIPS',
            'text1': message.content[5:]
        }
        response = requests.post(f"https://api.imgflip.com/caption_image",data=MEME_POST)
        raptor_link = response.json()["data"]["url"]
        await message.channel.send(raptor_link)
        #raptor_img = requests.get(raptor_link)
        #poster = Image.open(BytesIO(raptor_img.content))
        #poster.save('Raptor.png','PNG')
        #file = discord.File('Raptor.png', filename='Raptor.png')
        #await message.channel.send(file=file)
        #os.remove("C:\\Users\\Sungh\\PycharmProjects\\Jewdah\\Raptor.png")
@client.event
async def on_voice_state_update(voicemember, before, after):
   # print(voicemember.name)
    #rint(before)
   # print(af)
    memberblacklist = [voicemember.guild.get_member(x[1]).name for x in get_blacklist(voicemember.guild.id, [x.id for x in client.guilds], blacklists)]
    print(memberblacklist)
    #print([client.get_guild(429667475609878555).get_member(x[1]).name for x in blacklist])
    if onlist[get_guild(voicemember.guild.id, [x.id for x in client.guilds])] == True and voicemember.name in memberblacklist and after.channel != None and after.self_mute == False:
        time.sleep(1)
        await voicemember.move_to(None,reason="Because ur gay")
    if onlist[get_guild(voicemember.guild.id, [x.id for x in client.guilds])] == True and voicemember.name in memberblacklist and before.self_mute == True and after.self_mute == False:
        await voicemember.move_to(None,reason="Because ur gay")
      

keep_alive.keep_alive()
client.run("TOKEN")