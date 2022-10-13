from PIL import Image
from io import BytesIO
import requests
import PySimpleGUI as sg
import webbrowser
import json
#import os, sys
import random


def popup_image():
    im = Image.open('test.jpg')
    im_resize = im.resize((300, 200))
    buf = BytesIO()
    im_resize.save(buf, format='PNG')
    byte_im = buf.getvalue()

    layout = [
             [sg.T('text above the image')],
             [sg.Image(data=byte_im)],
             [sg.Exit()]
             ]
    window = sg.Window('window title',layout, element_justification='c')
    window.read()
    window.close()
    return
# takes generic byte data and returns a sanitized png image stream
def sanitize_image(generic_bytes, x=300, y=200):
    stream = BytesIO(generic_bytes)
    good_bytes = Image.open(stream)
    good_bytes = good_bytes.resize((x, y))
    buf = BytesIO()
    image = good_bytes.save(buf, format='PNG')
    return buf.getvalue()

def get_image_from_id(id):
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(id)
    headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com', 'x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
    response = requests.request('GET', url, headers=headers).json()
    image = requests.get(response['image']).content
    return image

def get_instructions(id):
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(id)
    headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com', 'x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
    response = requests.request('GET', url, headers=headers).json()
    return response['instructions']

def daily_plan_results(resultsList):
    breakfast = resultsList[0]
    lunch = resultsList[1]
    dinner = resultsList[2]
    
    breakfast_image = sanitize_image(get_image_from_id(breakfast['id']), 60,40)
    lunch_image = sanitize_image(get_image_from_id(lunch['id']), 60,40)
    dinner_image = sanitize_image(get_image_from_id(dinner['id']), 60,40)

    frame_layout = [ 
                   [sg.T('Breakfast',font=('Courier New',18,'bold'))],
                   [sg.T('{}'.format(breakfast['title']), background_color='grey', text_color='white')],
                   [sg.Image(data=breakfast_image)],                   
                   [sg.T('Lunch',font=('Courier New',18,'bold'))],
                   [sg.T('{}'.format(lunch['title']), background_color='grey', text_color='white')],
                   [sg.Image(data=lunch_image)],                   
                   [sg.T('Dinner',font=('Courier New',18,'bold'))],
                   [sg.T('{}'.format(dinner['title']), background_color='grey', text_color='white')],
                   [sg.Image(data=dinner_image)],                   
                   [sg.VPush()]
                   ]

    column_button_layout = [
                            [sg.B('View',k='vRecipe1', font=('Courier New', 12, 'bold')), sg.B('See steps!',k='pRecipe1')],
                            [sg.HorizontalSeparator(pad=12)],
                            [sg.B('View',k='vRecipe2', font=('Courier New', 12, 'bold')),sg.B('See steps!',k='pRecipe2')],
                            [sg.HorizontalSeparator(pad=12)],
                            [sg.B('View',k='vRecipe3', font=('Courier New', 12, 'bold')),sg.B('See steps!',k='pRecipe3')]
                           ]

    layout = [
             [sg.Frame('',frame_layout,border_width=2, relief='flat'), sg.Column(column_button_layout)],
             [sg.HorizontalSeparator()],
             [sg.Push(),sg.CButton('Close', font=('Courier New',18, 'bold')),sg.Push()]
             ]
    window = sg.Window('Daily Meal Plan',layout, font=('Courier New',12))
# WINDOW EVENT LOOP
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            window.close()
            break
        if(event == 'vRecipe1'):
            id = breakfast['id']
            url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(id)
            headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com','x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
            response = requests.request('GET', url, headers=headers).json()
            webbrowser.open(response['sourceUrl'])
        if(event == 'vRecipe2'):
            id = lunch['id']
            url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(id)
            headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com','x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
            response = requests.request('GET', url, headers=headers).json()
            webbrowser.open(response['sourceUrl'])
        if(event == 'vRecipe3'):
            id = dinner['id']
            url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'.format(id)
            headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com','x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
            response = requests.request('GET', url, headers=headers).json()
            webbrowser.open(response['sourceUrl'])
        if(event=='pRecipe1'):
            sg.popup('instructions',get_instructions(breakfast['id']))
        if(event=='pRecipe2'):
            sg.popup('instructions',get_instructions(lunch['id']))
        if(event=='pRecipe3'):
            sg.popup('instructions',get_instructions(dinner['id']))

def generate_meal_plan():
    layout = [
             [sg.Text('Select timeframe')],
             [ sg.Radio('Daily', 'timeframe', default=True, k='daily', background_color='grey', text_color='white'),sg.Radio('Weekly', 'timeframe',k='weekly',background_color='grey', text_color='white') ],
             [sg.Text('What is your ideal daily caloric intake?')],
             [sg.Spin([i for i in range(1,10000)], initial_value=2000, k='calories',background_color='grey', text_color='white'), sg.Text('calories',background_color='grey', text_color='white')],
             [sg.Text('Select your diet type. (optional)')],
             [sg.Listbox(['','vegan', 'vegetarian', 'pescatarian', 'gluten free', 'grain free', 'dairy free', 'high protein', 'low sodium', 'low carb', 'Paleo', 'Primal', 'ketogenic', 'FODMAP','Whole 30'],[''],auto_size_text=True,text_color='black',select_mode='LISTBOX_SELECT_MODE_MULTIPLE',s=(None,4),k='diet')],
             [sg.Text('Any items you\'d like to avoid? (separate with commas)')],
             [sg.In(background_color='red', text_color='white',k='exclude')],
             [sg.Submit(),sg.Exit(), sg.B('Return')]]

    window = sg.Window('Meal Planner', layout, element_justification='c',font=('Courier New',15))

# WINDOW EVENT LOOP
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
#    print(f'INPUT DATA:\n{timeframe} | {calories} | {diet} | {exclude}')
    response = requests.request('GET', url, headers=headers, params=querystring).json()
    print('\n'*24)
#    print(response)
    print('-'*90)
    if timeframe == 'week':
        for item in response['items']:
            item = json.loads(item['value']) # convert item['value']->str to item['value']->dict
            print('id: {} | {}'.format(item['id'], item['title']))

    else:
        daily_plan_results(response['meals'])
        window.close()
        '''
        for meal in response['meals']:
            print('id: {} | {}'.format(meal['id'],meal['title']))
        '''

def random_recipe_results(responseData):
    try:
        image = sanitize_image(requests.get(responseData['image']).content)
    except Exception as e:
        print(e)
    ingrCol = (item['name'] for item in responseData['extendedIngredients'])
    layout = [
             [sg.Text('Recipe: ',font=('Courier New',15, 'bold')),sg.Text('{}'.format(responseData['title']))],
             [sg.Text('Ingredients',font=('Courier New',15,'bold'))],
             [sg.Text('{}'.format('\n'.join(ingrCol)),auto_size_text=True), sg.Image(data=image)],
             [sg.Push(),sg.B('Visit',k='visit'),sg.B('See steps!',k='print'),sg.Push()],
             [sg.Save(bind_return_key=False),sg.Button('Close'),sg.Push()]
             ]
    window = sg.Window('Random Recipe Results', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            window.close()
            return
        if event == 'visit':
            webbrowser.open(responseData['sourceUrl'])
        if event == 'print':
            sg.popup('instructions',responseData['instructions'])
        if event == 'Save':
            save_recipe(responseData)

def random_recipe():
    querystring = {'number':'1'}

    layout = [
             [sg.Sizer(h_pixels=0,v_pixels=10)],
             [sg.T('Enter any constraint tags separated by commas')],
             [sg.In(k='constraints')],
             [sg.Sizer(h_pixels=0,v_pixels=10)],
             [sg.HorizontalSeparator()],
             [sg.Submit(), sg.Exit()]
             ]

    window = sg.Window('Random Meal', layout, element_justification='c')
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        window.close()
        return
    if values['constraints']:
        querystring.update({'tags':values['constraints']})
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random'
    headers = {'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com','x-rapidapi-key': '8d36fc9dacmsh905d9e293400d5bp1c6bedjsnb29677382b1b'}
#    sg.popup(querystring, 'query params')
    # get the response
    response = requests.request('GET', url, headers=headers, params=querystring).json()
    # print(response)
    try:
        window.close()
        random_recipe_results(response['recipes'][0])
    except Exception as e:
        print(e)
        sg.popup('no data found with matching parameters!\n\ttry some different keywords.')
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    ''' MAIN SCREEN'''
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# setup GUI
sg.theme('BrightColors')
selected_theme = sg.theme()
layout = [
         [sg.Push(),sg.B('change theme!',k='theme')],
         [sg.B('Search',pad=(10,20), s = (30,3), k='search')],
         [sg.B('Random', pad=(10,20), s = (30,3), k='random')],
         [sg.B('Meal Plan', pad=(10,20), s = (30,3), k='mealplan')],
         [sg.Exit()]
         ]
window = sg.Window('this will have a clever name eventually', layout, element_justification='c', font=('Courier New', 15, 'bold'))
# MAIN EVENT LOOP
path = './thing.png'
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break
    print(event, values)
    if event == 'theme':
        window.close()
        sg.theme(random.choice(sg.theme_list()))
        selected_theme = sg.theme()
        layout = [
                 [sg.Push(),sg.B('change theme!',k='theme')],
                 [sg.B('Search',pad=(10,20), s = (30,3), k='search')],
                 [sg.B('Random', pad=(10,20), s = (30,3), k='random')],
                 [sg.B('Meal Plan', pad=(10,20), s = (30,3), k='mealplan')],
                 [sg.Exit()]
                 ]
        window = sg.Window('this will have a clever name eventually', layout, element_justification='c', font=('Courier New', 15, 'bold'))
    if event == 'search':
        quit()
    if event == 'random':
        random_recipe()
    if event == 'mealplan':
        generate_meal_plan()
window.close()
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
