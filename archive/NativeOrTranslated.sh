# Look at this site http://opus.nlpl.eu/Books.php  
# Download http://opus.nlpl.eu/download.php?f=Books/v1/raw/en.zip
# Unzip the file. It creates Books/raw/en

rm native.csv translated.csv

# These are the basic processing steps for taking the book files downloaded from opus.nlpl.eu and 
# getting them ready for the ML process
#
# awk 'NR>15' $book -- skip the first 15 header lines. 
# sed 's/.*\">//'   -- Every line starts with something like <s id="s11.0"> 
# sed 's/....$//'   -- Every line ends with </s> so get rid of it
# sed 's/[_,]//g'   -- Get rid of underscores and commas. Especially the commas because the output is a csv file
# awk 'BEGIN{OFS=",";}; NF>10 && NF<25 {print $0,"native"}'    -- Find sentences with more than 10 and less than 25 words. 
# sed 's/\"//g'  -- Get rid of quotation marks. 

# Directory with all books in English, both native and translated
cd ./Books/raw/en

# Native English Language sentences
for book in Austen_Jane-Pride_and_Prejudice.xml Twain_Mark-Tom_Sawyer.xml Doyle_Arthur_Conan-Adventures_of_Sherlock_Holmes.xml
do
	awk 'NR>15' $book | sed 's/.*\">//' | sed 's/....$//' | sed 's/[_,]//g' | \
        awk 'BEGIN{OFS=",";}; NF>10 && NF<25 {print $0,"native"}'    | sed 's/\"//g' >> ~/opus/native.csv
done

# Professionally translated sentences from Spanish and French into English
for book in Cervantes_Miguel-Don_Quijote.xml Hugo_Victor-Notre_Dame_de_Paris.xml  Flaubert_Gustave-Madame_Bovary.xml
do
	awk 'NR>15' $book | sed 's/.*\">//' | sed 's/....$//' | sed 's/[_,]//g' | \
        awk 'BEGIN{OFS=",";}; NF>10 && NF<25 {print $0,"translated"}' | sed 's/\"//g' >> ~/opus/translated.csv
done


# Take one native Spanish language book and one French book. Pull out the sentences and prep the text. 
cd ~/opus/Books/raw/

awk 'NR>15' ./es/Cervantes_Miguel-Don_Quijote.xml | sed 's/.*\"\>//' |\
 sed 's/....$//' | sed 's/-/ /g' | sed 's/^[[:space:]]//' | sed 's/»//' | sed 's/[_,]//g' |\
 awk 'BEGIN{OFS=",";}; NF>10 && NF<25' | sed 's/\"//g' > ~/opus/cervantes.txt

awk 'NR>15' ./fr/Hugo_Victor-Notre_Dame_de_Paris.xml | sed 's/....$//' | sed 's/.*>//' |\
  sed 's/[-]/ /g' | sed 's/^[[:space:]]//' | sed 's/»//' | sed 's/[_,]//g' |\
 awk 'BEGIN{OFS=",";}; NF>10 && NF<25' | sed 's/\"//g' > ~/opus/victorhugo.txt

# Google Translate will only process 5000 characters at a time. Split the files into smaller
# text files that only have 300 lines each
cd ~/opus
split -l 300 cervantes.txt spanish
split -l 300 victorhugo.txt french
for file in `ls french* spanish*`; do mv $file $file.txt; done

# The commands below need to be run by hand after the manual translation is done. 
exit

# Now, you must go to translate.google.com and translate each of the spanish and 
# french documents one at a time. Paste the results into a text editor and save
# the final results as cervantes_machine_translated.txt and hugo_machine_translated.txt
# Alternatively, use the Translate API with key ml-sandbox-1-191918-b473cb40490b.json

cat hugo_machine_translated.txt cervantes_machine_translated.txt |\
  awk 'BEGIN{OFS="=";} {print $0",machine"}' > machine_translated.csv

# Shuffle the results. Not sure if Google does this automatically or not.
cat native.csv translated.csv machine_translated.csv | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > native_translated_machine.csv
 

