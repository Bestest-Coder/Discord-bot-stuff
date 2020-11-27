import discord
import role_checks
from discord.ext import commands
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageColor
import asyncio

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

    @commands.command(name='color')
    async def showColor(self,ctx, input1, input2=None, input3=None):
        try:
            if input2 == None:
                daColor = ImageColor.getrgb(input1)
            else:
                daColor = ImageColor.getrgb(f"rgb({input1},{input2},{input3})")
        except ValueError:
            await ctx.send("""Error: invalid color format, valid formats include:
=color #[hex color code] ex: ~color #ff0000
=color [red] [green] [blue] ex: ~color 255 0 0
=color [color name] ex: ~color red OR Red
Note: color names are based on HTML standards""")
            return
        daImage = Image.new('RGB', (100, 100), daColor)
        outputBytes = BytesIO()
        daImage.save(outputBytes, 'png')
        outputBytes.seek(0)
        daFile = discord.File(filename="color.png", fp=outputBytes)
        daColorHex = f'#{daColor[0]:02x}{daColor[1]:02x}{daColor[2]:02x}'
        daMessage = f"""RGB:{daColor}
Hex: {daColorHex}"""
        await ctx.send(daMessage, file=daFile)

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
                im = im.convert("LA")
            final_buffer = BytesIO()

            im.save(final_buffer, "png")
            final_buffer.seek(0)

            file = discord.File(filename="greayscale.png", fp=final_buffer)

            await ctx.send(file=file)

    @commands.group(invoke_without_command=True)
    async def filter(self,ctx):
        await ctx.send('''Guide to filter commands:
filter level - determines how much of each image to show on a scale of 0 to 1.0, higher filter level means more filter than base image
=filter me {filter level} - the image attached to the command message is placed over your avatar
=filter these {filter level} - the image attached to the command message is filtered by the image attached to a second message, limited 10 seconds later''')

    @filter.command(brief="adds attached image as a filter over your avatar")
    async def me(self,ctx, filterLevel : float=0.25):
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
                    resultImage = Image.blend(userImage, filterImage, filterLevel)

                    output_buffer = BytesIO()
                    resultImage.save(output_buffer, "png")
                    output_buffer.seek(0)

                    outputFile = discord.File(filename="filtered_Avatar.png",fp=output_buffer)
                    await ctx.send(file=outputFile)

    @filter.command(brief="adds second image as filter over first image")
    async def these(self,ctx, alphaAmount : float=0.25):
        try:
            first_bytes = await self.get_image(ctx.message.attachments[0])
        except IndexError:
            await ctx.send("Error: Message has no attached image")
            return
        def check(msg):
            return msg.author == ctx.message.author

        try:
            msg2 = await self.client.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Error: second image was not received fast enough")
            return
        try:
            second_bytes = await self.get_image(msg2.attachments[0])
        except IndexError:
            await ctx.send("Error: Second message has no attached image")
            return

        async with ctx.typing():
            with Image.open(BytesIO(first_bytes)) as firstImage:
                with Image.open(BytesIO(second_bytes)) as secondImage:
                    secondImage = secondImage.resize(firstImage.size)
                    secondImage = secondImage.convert("RGBA")
                    firstImage = firstImage.convert("RGBA")
                    resultImage = Image.blend(firstImage, secondImage, alphaAmount)

                    output_buffer = BytesIO()
                    resultImage.save(output_buffer, "png")
                    output_buffer.seek(0)

                    outputFile = discord.File(filename="filtered_Avatar.png",fp=output_buffer)
                    await ctx.send(file=outputFile)

    @commands.command(brief="replaces transparent parts of images and gifs with specified color (gifs WIP)")
    async def background(self,ctx, input1, input2=None, input3=None):
        try:
            if input2 == None:
                daColor = ImageColor.getrgb(input1)
            else:
                daColor = ImageColor.getrgb(f"rgb({input1},{input2},{input3})")
        except ValueError:
            await ctx.send("""Error: invalid color format, valid formats include:
=color #[hex color code] ex: ~color #ff0000
=color [red] [green] [blue] ex: ~color 255 0 0
=color [color name] ex: ~color red/Red
Note: color names are based on HTML standards""")
            return
        try:
            imageBytes = await self.get_image(ctx.message.attachments[0])
        except IndexError:
            await ctx.send("Error: no attached image or gif")
            return
        inputImage = Image.open(BytesIO(imageBytes))
        if getattr(inputImage, "is_animated", False):
            async with ctx.typing():
                bgImage = Image.new("RGBA", (inputImage.width, inputImage.height), daColor)
                images = []
                print("is animated ya fuck")
                for i in range(inputImage.n_frames):
                    bgFrame = bgImage.copy()
                    inputImage.seek(i)
                    currentFrame = (inputImage.copy()).convert('RGBA')
                    bgFrame.alpha_composite(currentFrame)
                    images.append(bgFrame)
                inputImage.seek(0)
                outputBytes = BytesIO()
                images[0].save(outputBytes, "gif", save_all=True, append_images=images[1:], loop=inputImage.info['loop'],
                               duration=(inputImage.info['duration']), disposal=2)
                outputBytes.seek(0)
                outputFile = discord.File(filename="backgrounded.gif", fp=outputBytes)
                await ctx.send("Note: gif backgrounds are WIP and inconsistent", file=outputFile)
        else:
            async with ctx.typing():
                bgImage = Image.new("RGBA", (inputImage.width, inputImage.height), daColor)
                newInput = inputImage.convert("RGBA")
                bgImage.alpha_composite(newInput)
                outputBytes = BytesIO()
                bgImage.save(outputBytes, "png")
                outputBytes.seek(0)
                outputFile = discord.File(filename="backgrounded.png", fp=outputBytes)
                await ctx.send(file=outputFile)

def setup(client):
    client.add_cog(Images(client))
