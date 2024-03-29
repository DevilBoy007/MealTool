## Meal Planning Tool ##

the purpose of this application was initally to practice utilitzing API response 
& implementing a GUI with Python
-- the application takes in user input & returns Spoonacular Recipe API response data

---

## HOW TO CONFIGURE ##
I've tried to make setup as streamlined as possible by providing a `Makefile`.
This should allow you to start the app up by 
1. clone this repo
2. in a terminal, navigate to the working directory (`~/Downloads/MealTool/v1` if you use the browser GUI)
3. run `make` command ;)

---

_v1_

* _DEPENDENCIES_

  * [PIL](https://pillow.readthedocs.io)
    * io 
  * [requests](https://requests.readthedocs.io)
  * [PySimpleGUI](https://pysimplegui.org)
  * [webbrowser](https://docs.python.org/3/library/webbrowser.html) - _built-in_
  * [json](https://docs.python.org/3/library/json.html) - _built-in_
  * [random](https://docs.python.org/3/library/random.html) - _built-in_
## WHAT WORKS ##

* random recipe button
* meal plan button
  * DAILY results only
* dynamic theme change button

## WHAT NEEDS WORK ##

* search button needs to be fully implemented
  * see [endpoint](https://rapidapi.com/spoonacular/api/recipe-food-nutrition)
* meal plan button
  * [WEEKLY](https://rapidapi.com/spoonacular/api/recipe-food-nutrition) results
* ADD button for uploading custom recipes
  * _no endpoint available! rely on sqlite database_
