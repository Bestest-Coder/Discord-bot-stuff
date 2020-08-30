import discord
import role_checks
from discord.ext import commands
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession(loop=client.loop)

    async def get_avatar(self, user:discord.Member) -> bytes:

        # generally an avatar will be 1024x1024, but we shouldn't rely on this
        avatar_url = str(user.avatar_url_as(format="png"))

        async with self.session.get(avatar_url) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        return avatar_bytes

    @commands.command(brief="returns pfp in greyscale")
    async def greyscale(self, ctx, *,member :discord.User=None):
        member = member or ctx.author
        async with ctx.typing():
            avatar_bytes = await self.get_avatar(member)
            with Image.open(BytesIO(avatar_bytes)) as im:
                im = im.convert("L")
            final_buffer = BytesIO()

            im.save(final_buffer, "png")
            final_buffer.seek(0)

            file = discord.File(filename="circle.png", fp=final_buffer)

            await ctx.send(file=file)


def setup(client):
    client.add_cog(Images(client))
