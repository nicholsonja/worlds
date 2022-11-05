#!/bin/sh

for f in *.png
do
	tex=`echo $f | awk -F_ '{print $1}' | sed 's/\\..*//'`

	echo cp $f ../models/${tex}_box/materials/textures
done
