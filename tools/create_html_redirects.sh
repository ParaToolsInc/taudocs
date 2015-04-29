#for file in *.html 
#	do mv $file `echo $file | sed 's/\(.*\.\)html/\1php/'`
#done
#
#for file in *.php
#do
#	echo "<html></head><META HTTP-EQUIV=\"Refresh\" CONTENT=\"0; 
#URL=$file\"></head></html>" > `echo $file | sed 's/\(.*\.\)php/\1html/g'`
#
#done

#copy images into 'chunked' directory.

cp ../*.gif . ;
cp ../*.jpg . ;
cp ../*.tiff . ;
cp ../*.png . ;

#change img source to immediate directory.

for file in *.html
	do sed s_"\.\.\/tools\/docbook-xsl-1.69.1\/images\/"_''_ > $file".tmp" < $file;
        mv $file".tmp" $file
done

for file in *.html
	do sed s_"Transitional//EN"_"Strict//EN"_ > $file".tmp" < $file;
        mv $file".tmp" $file
done

