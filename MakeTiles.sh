# We have already trained the AutoML neural network to identify coated, not coated, partial carbon and no carbon
# Now, we use this model to sort our large collection of tiles. This script will:
# 1) Rotate the original images to horizontal and crop them to 2560/2560
# 2) Split each image into 100 256x256 tiles
# 3) Ask AutoML what kind of image this is. 
# 4) Record the result for further use


# Rotate the vertical images to horizontal. Look for file size that matches 3024x4032
# and rotate those files 90 degrees

cd /Users/mikeevanoff/CarbonParts/JamalsPhotos
for file in `find . -name "*.jpg"`
do
   attr=`magick identify $file`
   if [[ $attr =~ .*3024x40.* ]]
   then
      convert -rotate "90" $file $file
   fi

   convert -crop 2560x2560+736+232 $file $file
done

cd /Users/mikeevanoff/CarbonParts
mkdir TilesWithFilm TilesNoFilm 

cd TilesWithFilm
for file in `find ../PART_W_FILM -name "*.jpg"`
do
	echo "Processing $file"
	slice-image $file 100
done

for base in `ls | grep png| sed 's/.png//'`
do 
   convert $base.png $base.jpg
   rm $base.png
done

python ../batch_predict.py
mv BatchOutput.txt ../InferenceWithFilm.txt

cd ../TilesNoFilm
for file in `find ../PART_WO_FILM -name "*.jpg"`
do
   echo "Processing $file"
   slice-image $file 100
done

for base in `ls | grep png| sed 's/.png//'`
do 
   convert $base.png $base.jpg
   rm $base.png
done

python ../batch_predict.py
mv BatchOutput.txt ../InferenceNoFilm.txt



