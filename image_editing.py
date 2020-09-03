import discord
import role_checks
from discord.ext import commands
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession(loop=client.loop) #make session that can fetch images from URLs

    async def get_image(self, imageSource) -> bytes:

        if type(imageSource) == discord.User or type(imageSource) == discord.Member: #get profile picture if user/member
            image_url = str(imageSource.avatar_url_as(format="png"))
        elif type(imageSource) == discord.Attachment: #get image if attachment
            image_url = str(imageSource.url)
        elif type(imageSource) == discord.Asset: #get image if asset, which idk if that can happen naturally
            image_url = str(imageSource)

        async with self.session.get(image_url) as response:
            # this gives us our response object, and now we can read the bytes from it.
            image_bytes = await response.read()

        return image_bytes

    @commands.command(brief="returns pfp in greyscale", aliases=['grayscale'])
    async def greyscale(self, ctx, *,member :discord.User=None):
        daImage = member or ctx.author
        try:
            daImage = ctx.message.attachments[0]
        except IndexError:
            #there's no attachments but I can't figure out a better way to deal with it
            pass
        async with ctx.typing():
            image_bytes = await self.get_image(daImage)
            with Image.open(BytesIO(image_bytes)) as im:
                im = im.convert("L")
            final_buffer = BytesIO()

            im.save(final_buffer, "png")
            final_buffer.seek(0)

            file = discord.File(filename="greayscale.png", fp=final_buffer)

            await ctx.send(file=file)

    @commands.command(brief="adds attached image as a filter over your avatar")
    async def filterme(self,ctx):
        avatar_bytes = await self.get_image(ctx.author)
        try:
            filter_bytes = await self.get_image(ctx.message.attachments[0])
        except IndexError:
            await ctx.send("Error: Message has no attached image")
            return
        async with ctx.typing():
            with Image.open(BytesIO(avatar_bytes)) as userImage:
                with Image.open(BytesIO(filter_bytes)) as filterImage:
                    filterImage = filterImage.resize(userImage.size)
                    filterImage = filterImage.convert("RGBA")
                    userImage = userImage.convert("RGBA")
                    resultImage = Image.blend(userImage, filterImage, 0.25)

                    output_buffer = BytesIO()
                    resultImage.save(output_buffer, "png")
                    output_buffer.seek(0)

                    outputFile = discord.File(filename="filtered_Avatar.png",fp=output_buffer)
                    await ctx.send(file=outputFile)

def setup(client):
    client.add_cog(Images(client))
