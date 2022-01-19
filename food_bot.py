import requests
import PySimpleGUI as sg
import webbrowser
import json

# setup GUI
sg.theme('DarkAmber')
layout = [[sg.Text('Select timeframe')],
         [ sg.Radio('Daily', 'timeframe', default=True, k='daily', text_color='gainsboro'),sg.Radio('Weekly', 'timeframe',k='weekly',text_color='gainsboro') ],
         [sg.Text('What is your ideal daily caloric intake?')],
         [sg.Spin([i for i in range(1,10000)], initial_value=2000, k='calories',text_color='gainsboro'), sg.Text('calories',text_color='gainsboro')],
         [sg.Text('Select your diet type. (optional)')],
         [sg.Listbox(['','vegan', 'vegetarian', 'pescatarian', 'gluten free', 'grain free', 'dairy free', 'high protein', 'low sodium', 'low carb', 'Paleo', 'Primal', 'ketogenic', 'FODMAP','Whole 30'],[''],auto_size_text=True,text_color='gainsboro',select_mode='LISTBOX_SELECT_MODE_MULTIPLE',s=(None,4),k='diet')],
         [sg.Text('Any items you\'d like to avoid? (separate with commas)')],
         [sg.In(text_color='gainsboro',k='exclude')],
         [sg.Submit(),sg.Exit()]]

window = sg.Window('this will have a clever name eventually', layout, element_justification='c',font=('Courier New',15))

# MAIN EVENT LOOP
while True:
    event, values = window.read()   # caputure screen input
    print(event, values) # FOR DEBUGGING
    if event in (sg.WIN_CLOSED, 'Exit'):  # user has exited or submitted form data
        quit()
    if event == 'Submit':
        break
window.close()
timeframe = 'day' if values['daily'] else 'week'
calories = values['calories']
diet = values['diet'][0]
exclude = values['exclude']
url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate'
querystring = {'timeFrame': timeframe,'targetCalories': calories,'diet': diet,'exclude': exclude}
headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com', 'x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
print(f'INPUT DATA:\n{timeframe} | {calories} | {diet} | {exclude}')
response = requests.request('GET', url, headers=headers, params=querystring).json()
print('\n'*24)
print(response)
print('-'*90)
if timeframe == 'week':
    for item in response['items']:
        item = json.loads(item['value']) # convert item['value']->str to item['value']->dict
        print('id: {} | {}'.format(item['id'], item['title']))

else:
    for meal in response['meals']:
        print('id: {} | {}'.format(meal['id'],meal['title']))
