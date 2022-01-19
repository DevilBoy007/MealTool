import requests
import PySimpleGUI as sg
import webbrowser
import json

def daily_plan_results(resultsList):
    breakfast = resultsList[0]
    lunch = resultsList[1]
    dinner = resultsList[2]
    sg.theme('DarkAmber')
    frame_layout = [ [sg.T('Breakfast',font=('Courier New',18,'bold'))],
               [sg.T('{}'.format(breakfast['title']), text_color='gainsboro')],
               [sg.T('Lunch',font=('Courier New',18,'bold'))],
               [sg.T('{}'.format(lunch['title']), text_color='gainsboro')],
               [sg.T('Dinner',font=('Courier New',18,'bold'))],
               [sg.T('{}'.format(dinner['title']), text_color='gainsboro')],
               [sg.VPush()]
             ]
    layout = [
             [sg.Frame('',frame_layout)],
             [sg.VPush()],
             [sg.HorizontalSeparator()],
             [sg.CButton('Close')]
             ]
    window = sg.Window('Daily Meal Plan',layout, font=('Courier New',12))
    window.read()
    window.close()

def generate_meal_plan():
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
             [sg.Submit(),sg.Exit(), sg.B('Return')]]

    window = sg.Window('Meal Planner', layout, element_justification='c',font=('Courier New',15))

    # MAIN EVENT LOOP
    event, values = window.read()   # caputure screen input
    print(event, values) # FOR DEBUGGING
    if event in (sg.WIN_CLOSED, 'Exit'):  # user has exited
        window.close()
        quit()
    if event == 'Return':
        window.close()
        return
    # if they didn't quit, they submitted #if event == 'Submit'
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
        daily_plan_results(response['meals'])
        '''
        for meal in response['meals']:
            print('id: {} | {}'.format(meal['id'],meal['title']))
        '''
''' MAIN SCREEN'''
#setup GUI
sg.theme('DarkAmber')
layout = [ [sg.B('Search',pad=(10,20), s = (30,3), k='search')],
           [sg.B('Random', pad=(10,20), s = (30,3), k='random')],
           [sg.B('Meal Plan', pad=(10,20), s = (30,3), k='mealplan')],
           [sg.Exit()]
         ]
window = sg.Window('this will have a clever name eventually', layout, element_justification='c', font=('Courier New', 15, 'bold'))
# MAIN EVENT LOOP
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break
    print(event, values)
    if event == 'search':
        quit()
    if event == 'mealplan':
        generate_meal_plan()
window.close()
''' ------------------------------------------------------ '''
