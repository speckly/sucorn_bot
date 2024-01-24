import discord
import datetime
from discord import app_commands
import sys
sys.path.append('./features')
from catrescue import catDownloader

MY_GUILD = discord.Object(id=494484012484788245)
buttons = []

async def buttonCB(interaction: discord.Interaction, button: discord.ui.Button, mode: str, view: discord.ui.View):
    if interaction.user.id != 494483880410349595:
        await interaction.response.send_message('Not authorised to use this button', ephemeral=True) 
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: BAKA DETECTED USING BUTTONS! {interaction.user.id}')
    else:
        button.disabled = True
        # Given list [n1 to 4, p1 to 4], find and remove opposite button of given button
        image_number: str = int(mode[-1])
        idx = image_number+3 if mode[:-1] == "Negative" else image_number-1
        view.remove_item(view.buttons[idx])
        channel_name = interaction.channel.name
        image_index = image_number - 1 # Labels are 1-4 attached to the end of the string
        try:
            emb = interaction.message.embeds[image_index]
            res = f"Image {image_index+1}: {catDownloader(emb.image.url, channel_name, mode)}\n"
        except IndexError:
            res = f"Image {image_index+1}: Index out of range"
        await interaction.response.edit_message(view=view)
        await interaction.followup.send(f"{mode}:\n{res}", ephemeral=True) 

class PosNegView(discord.ui.View):
    def __init__(self, image_count:int = 0):
        super().__init__(timeout=None)
        self.buttons = [self.negative1, self.negative2, self.negative3, self.negative4, 
                 self.positive1, self.positive2, self.positive3, self.positive4]
        self.update_buttons(image_count)

    @discord.ui.button(label='Negative1', row=0, style=discord.ButtonStyle.danger, custom_id='persistent_negative1')
    async def negative1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Negative1', self)

    @discord.ui.button(label='Negative2', row=0, style=discord.ButtonStyle.danger, custom_id='persistent_negative2')
    async def negative2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Negative2', self)

    @discord.ui.button(label='Negative3', row=0, style=discord.ButtonStyle.danger, custom_id='persistent_negative3')
    async def negative3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Negative3', self)

    @discord.ui.button(label='Negative4', row=0, style=discord.ButtonStyle.danger, custom_id='persistent_negative4')
    async def negative4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Negative4', self)

    @discord.ui.button(label='Positive1', row=1, style=discord.ButtonStyle.success, custom_id='persistent_positive1')
    async def positive1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Positive1', self)

    @discord.ui.button(label='Positive2', row=1, style=discord.ButtonStyle.success, custom_id='persistent_positive2')
    async def positive2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Positive2', self)

    @discord.ui.button(label='Positive3', row=1, style=discord.ButtonStyle.success, custom_id='persistent_positive3')
    async def positive3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Positive3', self)

    @discord.ui.button(label='Positive4', row=1, style=discord.ButtonStyle.success, custom_id='persistent_positive4')
    async def positive4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await buttonCB(interaction, button, 'Positive4', self)

    def update_buttons(self, image_count:int = 0):
        self.clear_items()
        for i in range(image_count):
            self.add_item(self.buttons[i]) # Negative
            self.add_item(self.buttons[i+4]) # Positive 

    

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

        # Persistent listening
        self.add_view(PosNegView())
