DATASETS_PATH = "./data/"
DB_TYPES = ["fill-mask", "semantic-similarity", "w2v"]
PROMPT_PROPOSITIONIZER = """
Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
context.
1. Split compound sentence into simple sentences. Maintain the original phrasing from the input
whenever possible.
2. For any named entity that is accompanied by additional descriptive information, separate this
information into its own distinct proposition.
3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that", "you", "your") with the full name of the
entities they refer to.
4. Present the results as a list of strings, formatted in JSON
You will only provide the result formatted in JSON and nothing else

Example:

Input: Title: ¯Eostre. Section: Theories and interpretations, Connection to Easter Hares. Content:
The earliest evidence for the Easter Hare (Osterhase) was recorded in south-west Germany in
1678 by the professor of medicine Georg Franck von Franckenau, but it remained unknown in
other parts of Germany until the 18th century. Scholar Richard Sermon writes that "hares were
frequently seen in gardens in spring, and thus may have served as a convenient explanation for the
origin of the colored eggs hidden there for children. Alternatively, there is a European tradition
that hares laid eggs, since a hare's scratch or form and a lapwing's nest look very similar, and
both occur on grassland and are first seen in the spring. In the nineteenth century the influence
of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular throughout Europe.
German immigrants then exported the custom to Britain and America where it evolved into the
Easter Bunny."
Output: ["The earliest evidence for the Easter Hare was recorded in south-west Germany in
1678 by Georg Franck von Franckenau.", "Georg Franck von Franckenau was a professor of
medicine.", "The evidence for the Easter Hare remained unknown in other parts of Germany until
the 18th century.", "Richard Sermon was a scholar.", "Richard Sermon writes a hypothesis about
the possible explanation for the connection between hares and the tradition during Easter", "Hares
were frequently seen in gardens in spring.", "Hares may have served as a convenient explanation
for the origin of the colored eggs hidden in gardens for children.", "There is a European tradition
that hares laid eggs.", "A hare's scratch or form and a lapwing's nest look very similar.", "Both
hares and lapwing's nests occur on grassland and are first seen in the spring.", "In the nineteenth
century the influence of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular
throughout Europe.", "German immigrants exported the custom of the Easter Hare/Rabbit to
Britain and America.", "The custom of the Easter Hare/Rabbit evolved into the Easter Bunny in
Britain and America."]
"""
PROMPT_PROPOSITIONIZER_V2 = """
Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
context.
1. Split compound sentence into simple sentences. Maintain the original phrasing from the input
whenever possible.
2. For any named entity that is accompanied by additional descriptive information, separate this
information into its own distinct proposition.
3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that", "you", "your") with the full name of the
entities they refer to.
4. Present the results as a list of strings, formatted in JSON
You will only provide the result formatted in JSON and nothing else

Example:

Input: Title: Udyr. Section: Udyr Guide. Content: Additionally, he can periodically empower 
one of his abilities. In addition, when changing stances he empowers his next two basic 
attacks to gain bonus attack speed and refund some of his passive. Udyr's Q isn't important 
as we don't level it. Udyr's W grants him a shield and makes his next two attacks gain lifesteal
and heal him. Of course making sure you use two attacks between each ability. For matchups, 
Udyr is amazing into tanky top lane bruisers who he can simply outvalue in extended fights. 
The longer the fight goes, the more you'll be rotating through your stances and getting your 
passive hits off, so the longer the fight, the more value you tend to get. 
However, at level 6 you don't get the big power spike so do care against champions that do. 
Output: ["Additionally, Udyr can periodically empower one of his abilities", "In addition, 
when changing stances Udyr empowers his next two basic attacks to gain bonus attack speed and 
refund some of his passive", "Udyr's Q isn't import as we don't level it", "Udyr's W grants him a 
shield and makes his next two attacks gain lifesteal and heal him", "Of course making sure Udyr is
using two attacks between each ability", "For matchups, Udyr is amazing into tanky top lane bruisers",
"Udyr can simply outvalue in extended fights", "The longer the fight goes, the more Udyr will be 
rotating through stances", "The longer the fight goes, the longer Udyr's passive hits off", "The 
longe the fight goes the more value Udyr tends to get", "However at level 6, Udyr doesn't get a 
big power spike", "Udyr needs to care against champions that have level 6 big power spike"]
"""