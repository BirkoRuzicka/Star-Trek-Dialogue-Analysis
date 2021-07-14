# Gender in „Star Trek“ dialogue and characters 

**A statistical analysis of episode transcripts, by Dr. Birko-Katarina Ruzicka**

<br>

## Motivation

It is no secret that dialogue in movies and series has been unevenly distributed between genders this far ([Source 1](#bibliography)), although surprisingly few studies have been conducted on the matter so far, and even fewer were published in peer-reviewed journals. Rare and beautiful examples for what could be done include 
* the outstanding work by Anderson and Daniels titled "Film Dialogue from 2,000 screenplays, Broken Down by Gender and Age" ([Source 1](#bibliography)), and 
* T. Bowe's "Stargate SG1 Dialogue Text Analysis" ([Source 2](#bibliography)), in which he thoroughly analyses dialogue by character, speech content, and positive vs. negative sentiment across five seasons of a sci-fi show. 

(both of which, by the way, are filled to the brim with beautiful Data Vizualisation graphics!)

As a lifelong "trekkie", I was curious as to how this was handled within the **Star Trek** franchise, a notoriously socially progressive format whose plotlines are frequently driven by themes of morality and tolerance. Star Trek's numerous shows and movies, covering roughly 60 years of social development, also make it an ideal target for studies across time. 

I analysed the transcripts of most Star Trek series for the ratio of male, female, and gender-neutral characters with speaking roles, as well as how many lines of dialogue are spoken by each gender. In particular, I focused on how this distribution changed over time. 

These are the series I included in the study:

|title                               | abbreviation |&emsp; originally aired|
:------------------------------------| ------------ | ---------------------:|
|Star Trek: The Original Series      |TOS           |              1966-1969|
|Star Trek: The Animated Series&emsp;|TAS           |              1973-1974|
|Star Trek: The Next Generation      |TNG           |              1987-1994|
|Star Trek: Deep Space Nine          |DS9           |              1993-1999|
|Star Trek: Voyager                  |VOY           |              1995-2001|
|Star Trek: Enterprise               |ENT           |              2001-2005|
|Star Trek: Discovery                |DIS           |              2017-2021|
|Star Trek: Picard                   |PIC           |              2020-2020|

<br>

The main steps in this analysis were:

1. collecting and preparing the data ([go there](#part1))
2. bringing in additional, manually prepared metadata
3. analysis of gender in individual series
4. analysis of gender across all series with time

<br>

## 1. Collecting and preparing the data 
<a id="part1"></a>

I initially was inspired by, and worked from, a dataset of "Star Trek Scripts" from Kaggle ([Source 3](#Bibliography)). While working with this data, however, I noticed some issues that required extensive cleaning, and some issues that I was unable to correct at all. Furthermore, having been created several years ago, the dataset did not include the most recent Star Trek series "Discovery" and "Picard" (which, spoiler!, have turned out to be pivotal to my analysis).

So, in a fit of perfectionism, I wrote my own Python webscraping algorithm to fetch the transcripts to transform the text into a clean, ready-to-use dataset in JSON format. The JSON file and the algorithm are available [in this GitHub repository](https://github.com/BirkoRuzicka/Star-Trek-Transcripts).

(***A note on code in this notebook:***
*the examples of code I show here are not intended to represent a fully working model of my analysis, but rather to illustrate concepts. The full code is available on GitHub, please use this if you intend to recreate any of my work!*)


To begin the analysis, the contents of the JSON file are read into a Pandas dataframe. To prevent the code from being unnecessarily complex, I did this series-by-series. I will now show the code for creating the "TOS" segment of the dataframe:

```python
import json
import pandas as pd

# open the JSON and read each series' entry into a variable
with open('StarTrekDialogue.json', 'r') as read_file:
    all_series = json.load(read_file)
del(read_file)
    
tos = all_series['TOS']  # ...and so on, for tas, tng, ds9, ...

# transform dict -> series -> dataframe
tos_series = pd.concat({k: pd.Series(v) for k, v in tos.items()})
tos_df = pd.Series.to_frame(tos_series).reset_index()
tos_df.columns = ['Episode', 'Character', 'Lines']
```

This dataframe now contains every line ever spoken on "TOS", so in the next step I removed all entries for 'minor characters' who have less than 10 lines of dialogue per episode. This reduces noise and lowers the overall workload in the next step.

```python
# create additional column in the dataframe to show a character's linecount per episode
tos_df['Linecount'] = tos_df['Lines'].str.len()

# drop entries where Linecount is less than 10
for index in tos_df.index:
    if tos_df.at[index, 'Linecount'] < 10:
        tos_df.drop(index, axis=0, inplace=True)
```
<br>

## 2. Additional metadata

In addition to the information on episode number, character name, and lines spoken by the character, I needed the following additional metadata for the episodes and characters:

* **season** of the episode within the series
* **year** when the episode was first aired on U.S. tv (and for DIS and PIC, on streaming services)
* **episode title** for personal orientation within the series
* **character gender**

The first three items were easily extracted from Wikipedia (and saved in a CSV file for later use), but the characters' gender had to be assessed manually. Working from a list of unique character names of the series 

```python
tos_df['Character'].unique()
```

I cross-referenced the fandom encyclopedia [Memory Alpha](https://memory-alpha.fandom.com/), my memory, and in some inconclusive cases even the episode's video itself, to compile a CSV file of the gender for each character with at least 10 lines in the respective episode. 

To illustrate the scale of this endeavour:

|series          |TOS|TAS|TNG|DS9|VOY|ENT|DIS|PIC|
|---             |---|---|---|---|---|---|---|---|
|character count |229| 49|419|362|385|211| 74| 33|

<br><br>

***A note on "gender" in this study***

*Rarely in Star Trek is a character's gender explicitly stated on screen, except for episodes that expressly deal with gender. Notable examples of such episodes include "The Outcast" (TNG, season 5, episode 17) and "Cogenitor" (ENT, season 2, episode 22). Much could and should be said about gender expression in Star Trek, but that is not the scope of this project. If anyone reading this feels the calling to expand on this further, I fiercely encourage you to get in touch with me!*

*For the purpose of this study, I assigned characters the gender which they were expressing to the viewer. In almost every case, I found the characters' gender expression to be stereotypical, sometimes to an amusing degree. However, in the few ambiguous cases I relied on how the character referred to themselves or was referred to by another in dialogue, as well as background knowledge on the character. For example:*

*- the ship's computer generally speaks in a female-coded voice (fellow trekkies will know that it was indeed the voice of Majel Barret, the wife of Gene Roddenberry himself). However, the computer never expresses gender, nor is it ever addressed as anything other than "it", so I classified it as genderneutral*

*- the Voyager's "Emergency Medical Hologram" is a non-corporeal computer program, so it is not "alive" and does not have a gender in the conventional sense. But it is generally referred to as "he", the crew members treat it as a person, and we come to understand throughout the plot that it is evolving self-awareness as a male person. I therefore classified this character as male*

*- Next Generation's "Data" is an android, whose outward gender expression is distinctly male. Furthermore, Data is consistently portrayed as self-aware and is shown to understand himself as male, so I classified him as male*

<br>

Once I had compiled both files of additional data, I added them to the dataframe and re-ordered the columns:

```python
# open csv files
tos_data = pd.read_csv('additional_data/tos_data.csv', index_col=0, delimiter=';')
tos_gender = pd.read_csv('additional_data/tos_gender.csv',
                                 header=None, index_col=0, squeeze=True, delimiter=';').to_dict()

# the season-year-episodetitle data can simply be merged to the df,
# as it's in the same format (one entry per episode)
tos_df = tos_df.merge(tos_data, left_on='Episode', right_index=True)
        
# the gender data has to be mapped to the dataframe, as characters appear in multiple episodes  
tos_df['Gender'] = tos_df['Character'].map(tos_gender)
        
# re-order columns
tos_df = tos_df[['Episode', 'Season', 'Year', 'Title', 'Character', 'Gender', 'Lines', 'Linecount']]
```

<br>














## Bibliography
<a id="bibliography"></a>

[1] 	H. Anderson und M. Daniels, „Film Dialogue from 2,000 screenplays, Broken Down by Gender and Age,“ 2016, https://pudding.cool/2017/03/film-dialogue/.
<br><br>
[2] 	T. Bowe, „Stargate SG1 Dialogue Text Analysis,“ 2021, https://www.kaggle.com/tombowe/stargate-sg1-dialogue-text-analysis.
<br><br>
[3] 	G. Broughton, „Kaggle - Star Trek Scripts,“ 2018, https://www.kaggle.com/gjbroughton/start-trek-scripts.
