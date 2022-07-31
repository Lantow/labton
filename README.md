# labton

## What's this then?
**Labton** (**LAB**eling **TO**ol **N**ow!) is an OpenSource annotation tool for **creating text data sets for machine learning models**. The length of the paragraphs to annotate is defined by you. Labton also allows for extraction of words in the given pargraph - thus the labels of the paragraph can be a word from the paragraph. You can also use Labton to help control Inter-Annotator Agreement (ie. securing that your annotaters agree on the defined classes).

## But why?

This tool is thus used in order to create a labeled data set of text.
As such this library is for you if you:

0. Are aiming to build a text-classifiaction or -extraction algorithm, and are putting together a dataset.
1. Need high quality of the labels (secure Inter-Annotator Agreement)
2. Want a webpage that can be used to annotate your text both on PC and smartphone. 
3. Prioritize getting up and running fast and efficiently (can be done in seconds if the data is ready)
4. Actually wanted to use [prodigy](https://prodi.gy/buy) but need to do a proof a concept before spending the money;)

## How does it work?

The **Python library** includes an easily deployable Flask web app that allows one to annotate the text in self defined classes. The app can be deployed directly from a [Terminal](#How-do-I-get-started-with-running-application-on-server-(access-from-internet)) or through a [Jupyter Notebook](#How-do-I-get-started-in-a-jupyter-notebook-(access-localy)) for lighter annotation tasks. The classes, and many other aspects of the app, are easily configurable either via python or through YAML configguration files. 

The data can be easily uploaded to the app. This can be done by directly pointing to a .cvs file (and specifying the delimiter) or by simply feeding in a Pandas Dataframe (and specifying the text column). The app will then structure the data and present one segment at a time for human classification in the UI.

## How do I get started in a jupyter notebook (access localy)

Firstly `pip install labton` in your virtual environment of choice
From there simply open jupyter notebook and run the following from a cell.

In order to test the interface, with sample data from the package, simply instantiate and run the App object without any data source or classes 

**`from labton.annotation_app import App`**<br/>
**`App().run()`**

The app should now be running at [localhost:8080](localhost:8080) <br/>
Type any name to login (no password needed for now)

When you've verified that Labton is useable for your usecase you can go ahead and boot up the app with your own data like so:

**`from labton.annotation_app import App`**<br/>
**`app = App(data_source='`\<your data source>`, classes=`\<your list of classes>`)`**

\<your list of classes> is a list contatining the classes you want to classify the text into. For a tweet sentiment classifier this could look like: `classes=["positive", "Negative", "Neutral"]`<br/>
\<your data source> can either be a path to the .csv file or alternatively a pandas.DataFrame. <br/>
If a it is a Datafame the `column_name` of the column contatining the text needs to be defined. If a .csv file only contating the text, then the delimiter of the files need to be fed to the App object as `csv_sep`.
You can also set the `project_name` (used when running many projects from the same environment), the `port`, the directory you want the config- and data files created in, along with many other setings. 

In order to boot up the server and start annotating simply run:

**`app.run()`**

The jupyter notebook will be occupied as long as the server is running.
You can start the server again and it will continue where you left from.

At any point in the process you can extract a copy of the data as a pandas.DataFrame like so:

**`from labton.labton_backend.helper_funcs import get_labton_data`**<br/>
**`df_labeled_data = get_labton_data()`**

If you have given a your project a custom `project_name` hand this to the `get_labton_data` function in order to load the data from the correct database file.

## How do I get started with running application on server (access from internet)

If you don't already have an intenet facing server I can recomend starting a free account on [pythonanywhere](https://eu.pythonanywhere.com/registration/register/beginner/)) and booting up a server.

From here simply:
1. Go to the terminal
2. Create and activate a virtual environment (optional)
3. `pip install labton` or `python3 -m pip install labton`

In order to test the interface, with sample data from the package, simply go to the folder where you want to initialise the project and run the library as so:

`python -m labton`

This will create a folder for the config files and a folder for data base files and start the server with a few test sentances.<br/> The server can now be accessed locally for a testrun at [localhost:8080](localhost:8080)

You can now configure the YAML file found in the projects_config_files with the port, host, etc. that mathces your firewall configurations.

TODO: Add easy functionality and walkthrough for how to setup a python anywhere app
