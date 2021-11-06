import asyncio

async def get_confirmation(bot, msg, member):
    id = member.id
    valid_reactions = ["✅","❌"]
    for i in valid_reactions:
        await msg.add_reaction(i)
    try:
        reaction, _user = await bot.wait_for(
            'reaction_add',
            timeout=60,
            check=lambda reaction, user: str(reaction.emoji) in valid_reactions and user.id == id and reaction.message.id == msg.id
        )
    except asyncio.TimeoutError:
        timeup_embed = msg.embeds[0]
        timeup_embed.set_footer(text="No longer accepting input")
        timeup_embed.color = 0xFF0000
        await msg.edit(embed=timeup_embed)
        return False
    else:
        if str(reaction.emoji) == "✅":
            return True
        elif str(reaction.emoji) == "❌":
            return False

async def get_response_message(bot, member, channel, valid_responses = None, cooldown = 60):
    try:
        message = await bot.wait_for(
            'message',
            timeout=cooldown,
            check=lambda message: message.author.id == member.id and (valid_responses is None or valid_responses(message.content.lower())) and message.channel.id == channel.id
        )
    except asyncio.TimeoutError:
        return None
    else:
        return message
