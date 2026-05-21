import discord
from discord.ext import commands
import aiohttp
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

FORTNITE_API_KEY = '6228b402-0dd7-41f8-aec8-1bb19f94d13a'
ALLOWED_ROLE_ID = 1487483396958584923
OPENXBL_API_KEY = '03c68dd0-7045-4a6d-85ef-0c9da8d77230'
OUTPUT_CHANNEL_ID = 1490445025656701231
CREATE_ROLE_ID = 1459179799342743654

lookup_history = []

SCRIPT_TEXT = """
Hello,
I recently lost access to my epic games account as its attached to my deceased grandmothers email. 
My house recently burned down a month or so ago and I lost all my important things including my xbox. 
I no longer have access to my Microsoft account as it was also unfortunately on her email. 
I lost my Grandmother during the situation and no longer have any of her old electronics which consist of her emails and import documents. 
She was very old school with her technology and I don't even remember what the email is because I created the account in like 2017. 
I just recently finally got myself a new Xbox, and I just want too enjoy some games on my epic games account. 
it would be much appreciated if you could help me get back into my account.
I recently sold my xbox and forgot to remove my account from it. 
My Microsoft account was then stolen and I cannot recover it because the email was my mothers who passed in 2019. 
She typed her email into everything including my epic games which I don't have access to because of the hacker, nor do I know the email that she used. 
I would appreciate if you could help me regain access to my epic games account.
"""

RECEIPT_LINKS = [
    'https://x.frauded.cc/receipt/xboxstw.php',
    'https://x.frauded.cc/receipt/xboxvbucks.php',
    'https://x.frauded.cc/receipt/psnstw.php',
    'https://x.frauded.cc/receipt/psnvbucks.php'
]

def has_allowed_role():
    async def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.user.roles, id=ALLOWED_ROLE_ID)
        if role is None:
            await interaction.response.send_message(
                '❌ You dont have permission to use this command.', ephemeral=True
            )
            return False
        return True
    return discord.app_commands.check(predicate)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name='Pulling ur FN account ;)'
        )
    )
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name='account-id', description='Gets a Fortnite Account ID')
@has_allowed_role()
async def account_id(interaction: discord.Interaction, username: str):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://fortnite-api.com/v2/stats/br/v2',
            headers={'Authorization': FORTNITE_API_KEY},
            params={'name': username, 'accountType': 'epic'}
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                account = data['data']['account']
                embed = discord.Embed(title='Information', color=0x00BFFF)
                embed.add_field(name='Username', value=f'`{account["name"]}`', inline=False)
                embed.add_field(name='Account ID', value=f'`{account["id"]}`', inline=False)
                embed.set_footer(text='discord.gg/clod')
                lookup_history.append({'username': username, 'command': 'account-id', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                if len(lookup_history) > 50:
                    lookup_history.pop(0)
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif resp.status == 404:
                await interaction.followup.send(f'❌ No ID found by name **{username}**.', ephemeral=True)
            else:
                await interaction.followup.send('❌ Something went wrong, contact owner.', ephemeral=True)

@bot.tree.command(name='ban', description='Ban a Fortnite player')
@has_allowed_role()
async def ban(interaction: discord.Interaction, username: str):
    message = (
        f"Hello Epic Games, I'm reporting a player for violating Fortnite's rules. "
        f"Player Username: {username} "
        f"Date: This happened today, i don't remember what time it was. "
        f"Issue: Cheating, Hacking, Harassamment and teaming. "
        f"This behavior ruined fair gameplay and should be reviewed. "
        f"I've included evidence where possible. Thank you."
    )
    await interaction.response.send_message(message, ephemeral=True)

VOUCH_OUTPUT_CHANNEL_ID = 1490040160841105488  # Byt ut mot din vouch-kanals ID

@bot.tree.command(name='vouch', description='create a vouch')
@has_allowed_role()
async def vouch(interaction: discord.Interaction, username: str, text: str):
    await interaction.response.defer(ephemeral=True)

    channel = bot.get_channel(VOUCH_OUTPUT_CHANNEL_ID)
    if not channel:
        await interaction.followup.send('❌ Could not find the output channel.', ephemeral=True)
        return

    embed = discord.Embed(title='✅ Vouch', description=text, color=0x00FF00)
    embed.add_field(name='Vouch Created By:', value=f'**@{username}**', inline=False)
    embed.set_footer(text='Renegade Bot • discord.gg/clod')

    await channel.send(embed=embed)
    await interaction.followup.send('✅ Vouch sent!', ephemeral=True)

@bot.tree.command(name='epic-lookup', description='Look up information about an Epic Games account')
@has_allowed_role()
async def epic_lookup(interaction: discord.Interaction, username: str):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://fortnite-api.com/v2/stats/br/v2',
            headers={'Authorization': FORTNITE_API_KEY},
            params={'name': username, 'accountType': 'epic', 'image': 'all'}
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                account = data['data']['account']
                stats = data['data']['stats']['all']['overall']
                embed = discord.Embed(title=f'🔍 Epic Lookup – {account["name"]}', color=0x00BFFF)
                embed.add_field(name='👤 Username', value=f'`{account["name"]}`', inline=True)
                embed.add_field(name='🆔 Account ID', value=f'`{account["id"]}`', inline=True)
                embed.add_field(name='\u200b', value='\u200b', inline=False)
                embed.add_field(name='🏆 Wins', value=f'`{stats.get("wins", 0)}`', inline=True)
                embed.add_field(name='💀 Kills', value=f'`{stats.get("kills", 0)}`', inline=True)
                embed.add_field(name='🎮 Matches', value=f'`{stats.get("matches", 0)}`', inline=True)
                embed.add_field(name='☠️ Deaths', value=f'`{stats.get("deaths", 0)}`', inline=True)
                embed.add_field(name='📊 K/D', value=f'`{stats.get("kd", 0)}`', inline=True)
                embed.add_field(name='🎯 Win Rate', value=f'`{stats.get("winRate", 0)}%`', inline=True)
                embed.add_field(name='⏱️ Hours Played', value=f'`{round(stats.get("minutesPlayed", 0) / 60, 1)}`', inline=True)
                embed.add_field(name='🔫 Kills/Match', value=f'`{stats.get("killsPerMatch", 0)}`', inline=True)
                embed.set_footer(text='discord.gg/clod')
                lookup_history.append({'username': username, 'command': 'epic-lookup', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                if len(lookup_history) > 50:
                    lookup_history.pop(0)
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif resp.status == 403:
                await interaction.followup.send(f'🔒 **{username}** Is private.', ephemeral=True)
            elif resp.status == 404:
                await interaction.followup.send(f'❌ No account found by: **{username}**.', ephemeral=True)
            else:
                await interaction.followup.send('❌ Something went wrong.', ephemeral=True)

@bot.tree.command(name='receipt', description='Send receipt links')
@has_allowed_role()
async def receipt(interaction: discord.Interaction):
    embed = discord.Embed(title='🧾 Receipt', color=0x00BFFF)
    embed.add_field(name='Xbox STW', value=RECEIPT_LINKS[0], inline=False)
    embed.add_field(name='Xbox V-Bucks', value=RECEIPT_LINKS[1], inline=False)
    embed.add_field(name='PSN STW', value=RECEIPT_LINKS[2], inline=False)
    embed.add_field(name='PSN V-Bucks', value=RECEIPT_LINKS[3], inline=False)
    embed.set_footer(text='discord.gg/clod')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='creator-code-lookup', description='Look up a Fortnite creator code')
@has_allowed_role()
async def creator_code_lookup(interaction: discord.Interaction, code: str):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://fortnite-api.com/v2/creatorcode',
            headers={'Authorization': FORTNITE_API_KEY},
            params={'name': code}
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                creator = data['data']
                account = creator['account']
                embed = discord.Embed(title='🎨 Creator Code Lookup', color=0x00BFFF)
                embed.add_field(name='👤 Display Name', value=f'`{account["name"]}`', inline=True)
                embed.add_field(name='🆔 Account ID', value=f'`{account["id"]}`', inline=True)
                embed.add_field(name='🔖 Creator Code', value=f'`{code}`', inline=False)
                embed.add_field(name='✅ Status', value='`Active`' if creator.get('status') != 'DISABLED' else '`Inactive`', inline=True)
                embed.set_footer(text='discord.gg/clod')
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif resp.status == 404:
                await interaction.followup.send(f'❌ No creator code found for **{code}**.', ephemeral=True)
            else:
                await interaction.followup.send('❌ Something went wrong, contact owner.', ephemeral=True)

@bot.tree.command(name='epic-response', description='Check Epic Games server status')
@has_allowed_role()
async def epic_response(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://status.epicgames.com/api/v2/status.json') as resp:
            if resp.status == 200:
                data = await resp.json()
                status = data['status']
                indicator = status['indicator']
                description = status['description']
                if indicator == 'none':
                    color, emoji, status_text = 0x00FF00, '🟢', 'All Systems Operational'
                elif indicator == 'minor':
                    color, emoji, status_text = 0xFFA500, '🟡', 'Minor Issues'
                elif indicator == 'major':
                    color, emoji, status_text = 0xFF0000, '🔴', 'Major Outage'
                else:
                    color, emoji, status_text = 0xFF0000, '🔴', description
                embed = discord.Embed(title='Epic Games Public', description=f"Epic's response type is: **{status_text}**", color=color)
                embed.add_field(name='-24 Hours', value=emoji, inline=False)
                embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/1200px-Epic_Games_logo.svg.png')
                embed.set_footer(text='discord.gg/clod')
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send('❌ Could not fetch Epic Games server status.', ephemeral=True)

@bot.tree.command(name='ip', description='Look up information about an IP address')
@has_allowed_role()
async def ip_lookup(interaction: discord.Interaction, ip: str):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting,query') as resp:
            if resp.status == 200:
                data = await resp.json()
                if data['status'] == 'fail':
                    await interaction.followup.send(f'❌ Invalid IP address: **{ip}**', ephemeral=True)
                    return
                proxy = '✅ Yes' if data.get('proxy') else '❌ No'
                hosting = '✅ Yes' if data.get('hosting') else '❌ No'
                embed = discord.Embed(title=f'🔍 IP Lookup — {data["query"]}', color=0x00BFFF)
                embed.add_field(name='🌍 Country', value=f'`{data.get("country", "N/A")} ({data.get("countryCode", "N/A")})`', inline=True)
                embed.add_field(name='🏙️ City', value=f'`{data.get("city", "N/A")}`', inline=True)
                embed.add_field(name='📍 Region', value=f'`{data.get("regionName", "N/A")}`', inline=True)
                embed.add_field(name='📮 ZIP', value=f'`{data.get("zip", "N/A")}`', inline=True)
                embed.add_field(name='🕐 Timezone', value=f'`{data.get("timezone", "N/A")}`', inline=True)
                embed.add_field(name='📡 ISP', value=f'`{data.get("isp", "N/A")}`', inline=True)
                embed.add_field(name='🏢 Organization', value=f'`{data.get("org", "N/A")}`', inline=True)
                embed.add_field(name='🔢 AS', value=f'`{data.get("as", "N/A")}`', inline=True)
                embed.add_field(name='🗺️ Coordinates', value=f'`{data.get("lat", "N/A")}, {data.get("lon", "N/A")}`', inline=True)
                embed.add_field(name='🛡️ Proxy/VPN', value=proxy, inline=True)
                embed.add_field(name='🖥️ Hosting', value=hosting, inline=True)
                embed.set_footer(text='discord.gg/clod')
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send('❌ Something went wrong, contact owner.', ephemeral=True)

@bot.tree.command(name='script', description='Generates a script')
@has_allowed_role()
async def script(interaction: discord.Interaction):
    embed = discord.Embed(title='📝 Script', description=SCRIPT_TEXT, color=0x00BFFF)
    embed.set_footer(text='discord.gg/clod')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='help', description='Shows all available commands')
@has_allowed_role()
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title='📋 Command List', color=0x00BFFF)
    embed.add_field(
        name='🔍 Lookup Commands',
        value=(
            '`/account-id` – Get a Fortnite Account ID by username\n'
            '`/epic-lookup` – Get detailed Fortnite stats for an Epic account\n'
            '`/creator-code-lookup` – Look up a Fortnite creator code\n'
            '`/epic-response` – Check Epic Games server status\n'
            '`/ip` – Look up information about an IP address\n'
            '`/xbox-lookup` – Look up an Xbox account\n'
            '`/xbox-friends` – Get Xbox friends list link'
        ),
        inline=False
    )
    embed.add_field(
        name='💬 Other Commands',
        value=(
            '`/ban` – Report a Fortnite player to Epic Games\n'
            '`/vouch` – Send a vouch message for everyone to see\n'
            '`/receipt` – Get receipt links\n'
            '`/script` – Send the script message\n'
            '`/pulls` – Post your pull\n'
            '`/lookup-history` – Show recent lookups'
        ),
        inline=False
    )
    embed.set_footer(text='discord.gg/clod')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='xbox-lookup', description='Get information about an Xbox account')
@has_allowed_role()
async def xbox_lookup(interaction: discord.Interaction, username: str):
    await interaction.response.defer(ephemeral=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://xbl.io/api/v2/search/{username}',
            headers={'X-Authorization': OPENXBL_API_KEY, 'Accept': 'application/json', 'Accept-Language': 'en-US'}
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                people = data.get('content', {}).get('people', [])
                if not people:
                    await interaction.followup.send(f'❌ No Xbox account found with the name **{username}**.', ephemeral=True)
                    return
                user = people[0]
                xuid = user.get('xuid', 'N/A')
                gamertag = user.get('modernGamertag', user.get('gamertag', username))
                avatar = user.get('displayPicRaw', None)
                presence = user.get('presenceState', None)
                status_text = '🟢 Online' if presence == 'Online' else '🔴 Offline'
                detail = user.get('detail') or {}
                followers = detail.get('followerCount', 'N/A')
                following = detail.get('followingCount', 'N/A')
                profile_link = f'https://www.xbox.com/en-US/play/user/{gamertag}'
                async with session.get(
                    'https://fortnite-api.com/v2/stats/br/v2',
                    headers={'Authorization': FORTNITE_API_KEY},
                    params={'name': gamertag, 'accountType': 'xbl'}
                ) as fn_resp:
                    epic_id = 'N/A'
                    epic_name = 'N/A'
                    if fn_resp.status == 200:
                        fn_data = await fn_resp.json()
                        epic_id = fn_data['data']['account']['id']
                        epic_name = fn_data['data']['account']['name']
                embed = discord.Embed(title=f'🟢 Xbox Lookup — {gamertag}', color=0x107C10)
                embed.add_field(name='👤 Gamertag', value=f'`{gamertag}`', inline=True)
                embed.add_field(name='🆔 XUID', value=f'`{xuid}`', inline=True)
                embed.add_field(name='🌐 Status', value=status_text, inline=True)
                embed.add_field(name='👥 Followers', value=f'`{followers}`', inline=True)
                embed.add_field(name='➡️ Following', value=f'`{following}`', inline=True)
                embed.add_field(name='🔗 Profile', value=profile_link, inline=True)
                embed.add_field(name='⚡ Epic Name', value=f'`{epic_name}`', inline=True)
                embed.add_field(name='⚡ Epic ID', value=f'`{epic_id}`', inline=True)
                if avatar:
                    embed.set_thumbnail(url=avatar)
                embed.set_footer(text='discord.gg/clod')
                lookup_history.append({'username': username, 'command': 'xbox-lookup', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                if len(lookup_history) > 50:
                    lookup_history.pop(0)
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif resp.status == 404:
                await interaction.followup.send(f'❌ No Xbox account found with the name **{username}**.', ephemeral=True)
            else:
                await interaction.followup.send(f'❌ Something went wrong. Status: `{resp.status}`', ephemeral=True)

@bot.tree.command(name='xbox-friends', description='Get Xbox friends list link for a gamertag')
@has_allowed_role()
async def xbox_friends(interaction: discord.Interaction, username: str):
    link = f'https://eely-shelves.42web.io/friends/friends/?gamertag={username}'
    embed = discord.Embed(title=f'🟢 Xbox Friends — {username}', color=0x107C10)
    embed.add_field(name='🔗 Friends List', value=f'[View All Friends]({link})', inline=False)
    embed.set_footer(text='discord.gg/clod')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='pulls', description='Post your pull')
async def pulls(interaction: discord.Interaction, text: str, image: discord.Attachment):
    role = discord.utils.get(interaction.user.roles, id=CREATE_ROLE_ID)
    if role is None:
        await interaction.response.send_message('❌ You do not have permission to use this command.', ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    channel = bot.get_channel(OUTPUT_CHANNEL_ID)
    if not channel:
        await interaction.followup.send('❌ Could not find the output channel.', ephemeral=True)
        return
    embed = discord.Embed(description=text, color=0x00BFFF)
    embed.set_image(url=image.url)
    await channel.send(embed=embed)
    await interaction.followup.send('✅ Message sent!', ephemeral=True)

@bot.tree.command(name='lookup-history', description='Show the last accounts you have looked up')
@has_allowed_role()
async def lookup_history_cmd(interaction: discord.Interaction):
    if not lookup_history:
        await interaction.response.send_message('❌ No lookup history yet.', ephemeral=True)
        return
    embed = discord.Embed(title='🔍 Lookup History', color=0x00BFFF)
    for i, entry in enumerate(lookup_history[-10:], 1):
        embed.add_field(
            name=f'{i}. {entry["username"]}',
            value=f'Command: `{entry["command"]}` | Time: `{entry["time"]}`',
            inline=False
        )
    embed.set_footer(text='discord.gg/clod')
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run('TOKEN')
