## Integration with Searx
To integrate the PrivateRecsysFunctionality with search a plugin and an engine must be integrated within the plugins of search.

#integrating a plugin

A plugin called "Example plugin" was added to the 'settings.yaml' and the appropriate file 'examply.py' was added in searx/plugins with js code in /static/plugins/js. 


# Adding as engine and category of results
in engines in settings.yml add a new engine for the privaterecyss

 - name : privaterecsys
    engine : privaterecsys
    shortcut : prec

created a new file privaterecsys.py in engines folder and set as 
categories a new category called privaterecsys

we shall modify the base_url to the url of the recommender. and receive 
the results in the appropriate format and show them.

# search-url
base_url = 'https://www.bing.com/'
search_string = 'search?{query}&first={offset}'


### To start an instance of Searx:
'make run'

