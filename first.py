import discord 
import os 
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
SAMPLE_RANGE_NAME = "general!A:F"
####

load_dotenv()
DISCORD_API_SECRET = os.getenv("DISCORD_API_KEY")

class SimpleView(discord.ui.View):
        choice : int = None 
        @discord.ui.button(label="1",style=discord.ButtonStyle.green)
        async def green(self, interaction:discord.Interaction, button: discord.ui.Button):
            #await interaction.response.send_message("first option was chosen")
            self.choice = 1
            self.stop()
            
            
        @discord.ui.button(label="2",style=discord.ButtonStyle.blurple)
        async def blurple(self, interaction:discord.Interaction, button: discord.ui.Button):
            #await interaction.response.send_message("second option was chosen")
            self.choice = 2
            self.stop()
            
            
            
        @discord.ui.button(label="3",style=discord.ButtonStyle.red)
        async def red(self, interaction:discord.Interaction, button: discord.ui.Button):
           #await interaction.response.send_message("third option was chosen")
            self.choice = 3
            self.stop()
             
            
        @discord.ui.button(label="4",style=discord.ButtonStyle.grey)
        async def gray(self, interaction:discord.Interaction, button: discord.ui.Button):
            #await interaction.response.send_message("fourth option was chosen")
            self.choice = 4
            self.stop()
        
def run(): 
    intents = discord.Intents.default() 
    intents.message_content = True 
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    #variables for the questions
    
    
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        print("----------------")
        
       
    #use the number of questions to extac tthe values from google sheets to quetsion and optiosn list, and then for loop through the rest to create the embeds 
    # Study command to display a question with options
    @bot.command()
    async def study(ctx,questionNums = 1):
        #num of correct answers 
        values = []
        questions = []
        options = []
        correctOption = []
        
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
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
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
            print("it got the values")
            values = result.get("values", [])
            print(values)
            if not values:
                print("No data found.")
                return

            ##putting into variables 
            #print(values)
            ###for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print(f"{row[0]}, {row[4]}")###
        except HttpError as err:
            print(err)
            
      
        print("started command")
        
        correctCount = 0 
        #getting values from google sheets on request 
        values1 = values[1:questionNums+1]
        print(values1)
        print("forloop to extract")
        for mitem_index in range(len(values1)):
                print(values1[mitem_index])
                for item_index in range(0,len(values[mitem_index]),5):
                    print('question1')
                    print(values[mitem_index][item_index])
                    questions.append(values[mitem_index][item_index])
                    temp_list = [values[mitem_index][item_index + 1],values[mitem_index][item_index + 2],
                                 values[mitem_index ][item_index + 3],values[mitem_index][item_index + 4]]
                    options.append(temp_list)
                    #the correctOption now has char
                    correctOption.append(values[mitem_index][item_index + 5])
        # Input validation for google sheets values 
            #number of values need to be equal 
        print("past the for loop")
        print(questions)
        
        if not len(options) == len(questions) or len(options) == len(correctOption):
            return
        
        if len(questions) < questionNums:
            await ctx.send("Number of questions is higher than avaiable in database")
            #error check for more request
            return
        
        # Create an instance of SimpleView
        view = SimpleView()
        for index in range(questionNums): #change to range(0,questionNums)
            # Create and send the embed with buttons
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

            
            print(view.choice) #works till here 
            await view.wait() 
            print(view.choice)
            if view.choice == correctOption[index]: 
                await ctx.send("correct option was chosen")
                correctCount+=1
                continue
            else:
                await ctx.send("incorrect option was chosen, try again")
                continue
                
        
       #await send_question(ctx, question, options)
    
            
    bot.run(DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run() 