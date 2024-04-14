import discord
from discord.ext import commands
from discord.app_commands import command
from discord import Button
from utils.openai import openai_client


class FactButton(Button):

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer()
    completion_message = f"{interaction.user.display_name}: Tell me a fact"

    try:
      chat_completion = await openai_client.chat.completions.create(
          model="convoai-pro",
          messages=[{
              "role":
              "system",
              "content":
              "I want you to act as a random fact generator, your facts should be always safe for work, so no bad stuff, only positive random facts, your message should start as Hello! Did you knew that: {here you put your fact}"
          }, {
              "role": "user",
              "content": completion_message
          }],
      )

      if chat_completion.choices and chat_completion.choices[0].message:
        new_fact = chat_completion.choices[0].message.content
        embed = discord.Embed(title="📜 Facts",
                              description="```Made with ❤️ by ConvoAI```",
                              color=discord.Color.blue())
        embed.add_field(name="❓ Random Fact",
                        value=f"```{new_fact}```",
                        inline=True)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")

        await interaction.followup.edit_original_message(embed=embed)
      else:
        await interaction.followup.send(
            "No response from the text generation model, might be caused because of model not being available for you."
        )
    except Exception as e:
      await interaction.followup.send(
          f"An error occurred while processing your request: {e}")


class Cog6(commands.Cog):

  def __init__(self, client: commands.Bot):
    self.client = client

  @command(name="fact", description="Get a random fact from AI.")
  async def ask(self, interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    completion_message = f"{interaction.user.display_name}: Tell me a fact"

    try:
      chat_completion = await openai_client.chat.completions.create(
          model="convoai-pro",
          messages=[{
              "role":
              "system",
              "content":
              "I want you to act as a random fact generator, your facts should be always safe for work, so no bad stuff, only positive random facts, your message should start as Hello! Did you knew that: {here you put your fact}"
          }, {
              "role": "user",
              "content": completion_message
          }],
      )

      if chat_completion.choices and chat_completion.choices[0].message:
        fact = chat_completion.choices[0].message.content
        embed = discord.Embed(title="📜 Facts",
                              description="```Made with ❤️ by ConvoAI```",
                              color=discord.Color.blue())
        embed.add_field(name="❓ Random Fact",
                        value=f"```{fact}```",
                        inline=True)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")

        await interaction.followup.send(embed=embed, view=FactButton())
      else:
        await interaction.followup.send(
            "No response from the text generation model, might be caused because of model not being available for you."
        )
    except Exception as e:
      await interaction.followup.send(
          f"An error occurred while processing your request: {e}")


async def setup(client: commands.Bot) -> None:
  await client.add_cog(Cog6(client))
