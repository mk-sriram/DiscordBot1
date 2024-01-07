import discord 
import os 
import asyncio
from discord.ext import commands 
from dotenv import load_dotenv 
#######
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1PXo41iQE6BpjX6SWSkmTjz_2SKowuyLTIm6OpjcL4t4"
SAMPLE_RANGE_NAME = "A:F"

load_dotenv()
DISCORD_API_SECRET = os.getenv("DISCORD_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
GOOGLE_AUTH_PROVIDER_CERT_URL = os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL")
GOOGLE_REDIRECT_URIS = os.getenv("GOOGLE_REDIRECT_URIS")

        
class SimpleView(discord.ui.View):
        choice : int = None 
        
        async def on_timeout(self) -> None:
            self.choice = None
            self.stop()  
            
        def __init__(self, timerTime:int ):
            super().__init__(timeout=timerTime)
            
        @discord.ui.button(label="1",style=discord.ButtonStyle.green)
        async def green(self, interaction:discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.choice = 1
            self.stop()
            
        @discord.ui.button(label="2",style=discord.ButtonStyle.blurple)
        async def blurple(self, interaction:discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.choice = 2
            self.stop()
 
        @discord.ui.button(label="3",style=discord.ButtonStyle.red)
        async def red(self, interaction:discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.choice = 3
            self.stop()
             
        @discord.ui.button(label="4",style=discord.ButtonStyle.grey)
        async def gray(self, interaction:discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.choice = 4
            self.stop()
        
"""class clearButton(discord.ui.View):
    def __init__(self,  ctx: commands.Context, lines_to_clear: int):
        super().__init__()
        self.lines_to_clear = lines_to_clear
        self.ctx = ctx 

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.red)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Retrieve the channel where you want to clear messages
        await self.ctx.purge(limit=self.lines_to_clear + 1)"""
    
def run(): 
    intents = discord.Intents.default() 
    intents.message_content = True 
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        print(bot.user)
        print("----------------")
    
    # Study command to display a question with options
    @bot.command()
    async def study(ctx,questionNums = 1, time = 60):
        #Database variables
        values = []
        questions = []
        options = []
        correctOption = []
        #number of correct responses
        correctCount = 0 
        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": GOOGLE_CLIENT_ID,
                            "project_id": GOOGLE_PROJECT_ID,
                            "auth_uri": GOOGLE_AUTH_URI,
                            "token_uri": GOOGLE_TOKEN_URI,
                            "auth_provider_x509_cert_url": GOOGLE_AUTH_PROVIDER_CERT_URL,
                            "client_secret": GOOGLE_CLIENT_SECRET,
                            "redirect_uris": GOOGLE_REDIRECT_URIS
                        }
                    },
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                .execute()
            )
            #print("it got the values")
            values = result.get("values", [])
            #print(values)
            if not values:
                await ctx.send("No data found.")
                return

        except HttpError as err:
            print(err)
            
       
        #getting values from google sheets on request 
        values1 = values[1:questionNums+1]
        #print(values1)
        #print("forloop to extract")
        for mitem_index in range(len(values1)):
                #print(values1[mitem_index])
                #print('question1')
                     # Check if index + 5 is within the range
                questions.append(values1[mitem_index][0])
                temp_list = [
                    values1[mitem_index][1],
                    values1[mitem_index][2],
                    values1[mitem_index][3],
                    values1[mitem_index][4]
                ]
                options.append(temp_list)
                correctOption.append(values1[mitem_index][5])
                    
        if not (len(options) == len(questions) or len(options) == len(correctOption)):
            await ctx.send("Cells in the database are not full")
            return
        if len(questions) < questionNums:
            await ctx.send("Number of questions is higher than avaiable in database")
            #error check for more request
            return
        
        print("after getting values ")
        # Create an instance of SimpleView
        #view = SimpleView()
        index = 0 
       
        while index < questionNums: #change to range(0,questionNums)
            # Create and send the embed with buttons
             # simple view for each button
            view = SimpleView(time)
            embed = discord.Embed(
                colour=discord.Colour.orange(),
                title=f"{questions[index]} ?"
            )
            # Setting up the options in the description
            description = ""
            for idx, option in enumerate(options[index], start=1):
                description += f"{idx}. {option}\n"
            embed.description = description
            embed.set_footer(text="Select the option below")
            embed.set_author(name=f"Question {index+1}")
        
            message = await ctx.send(embed=embed, view=view)
            
            try:
                # Wait for the user to interact with the buttons
                 # Acknowledge the interaction
                # Retrieve the choice made by the user
                await view.wait() 
                selected_option = view.choice

                print(type(selected_option))
                print(correctCount)
                if selected_option == int(correctOption[index]):
                    await ctx.send("Correct option was chosen!")
                    correctCount += 1
                elif selected_option == None:
                    await ctx.send("you ran out of time!")
                else:
                    await ctx.send("Incorrect option was chosen")
                index += 1
            
            except asyncio.TimeoutError:
                await ctx.send("You didn't select an option in time.")
                break

            # Optionally, you can send the total score or any final message after all questions are answered.
        await ctx.send(f"Quiz ended! You got {correctCount} out of {questionNums} questions correct.")
        
            
    bot.run(DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run() 
    
