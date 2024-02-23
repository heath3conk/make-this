# Recipe matcher

## Problem statement
How can I decide what to cook in the evening when my executive function is low? I have ingredients and I know how 
to cook but I need someone to give me some ideas about what to make. 

I also want to be able to customize recipes to my preferences and make subsitutions while retaining the flavor profile of 
my favorite food. Examples
- Suppose I really don't like olives so any recipe that features olives is unlikely to make my list unless I can understand what they
    add to the flavor so I can substitute something else for their salty/briny-ness.
- Maybe I'm lactose intolerant but love pasta dishes and pizza. What can I do to give my lasange some creamy goodness without ricotta 
    or mozzarella.



## Methodology
1. Build an app that takes user input:
    - 2 or more ingredients (probably need an upper limit)
    - how much time to spend
2. Backend hits an API that returns (hopefully) several recipes that meet the criteria
3. App returns a flavor profile of the recipes, based on data from [FooDB](https://foodb.ca/foods)
4. User can select any of the ingredients in the list to either avoid altogether or to reduce, whether due to preferences, allergies or dietary restrictions
5. App returns suggested substitutions for those ingredients or different recipes

## Data
- API with recipe search by ingredient:
    - [recipe search API](https://developer.edamam.com/edamam-recipe-api)
- data with info about ingredients: 
    - [USDA API](https://fdc.nal.usda.gov/api-guide.html#bkmk-2): nutrients, etc. about branded foods as well as what they call "foundational" foods
    - they also have data for download, will try the api first & then see if I need to download data instead
    - FooDB: food groups, nutrients, chemical compounds
    - they too have data for download, massive CSV
- data with flavor profile of ingredients
    - this has a lot of great data I'm not sure if they have an API 
    - especially as a "nice to have," I'd love to use this: https://cosylab.iiitd.edu.in/flavordb/search for pairings and substitutions for flavor

### maybe nice to have
Could have users input this info on specific ingredients or make suggestions to users:
- typical foods people avoid for dietary reasons and substitutions for them, eg. low sodium, low fat
- typical foods people are allergic to and substitutions for them, eg. shellfish, nuts, dairy
- types/combinations of foods people avoid for religious reasons, eg. kosher

## Technical notes
### Installing requirements
- From the root of this repo, run `conda deactivate` to get out of any of your existing conda environments
- Hopefully, you're running zsh with a theme that shows your active conda environment - yes?
- Run `conda env create -f env.yml`

## References
1. Neelansh Garg, Apuroop Sethupathy, Rudraksh Tuwani, Rakhi NK, Shubham Dokania, Arvind Iyer, Ayushi Gupta, Shubhra Agrawal, Navjot Singh, Shubham Shukla, Kriti Kathuria, Rahul Badhwar, Rakesh Kanji, Anupam Jain, Avneet Kaur, Rashmi Nagpal, Ganesh Bagler. (2018, 4 January) FlavorDB: a database of flavor molecules. Nucleic Acids Research [link](https://academic.oup.com/nar/article/46/D1/D1210/4559748#107188690)
