#!/bin/bash

cat $1.glade |sed s/interface/glade-interface/ > $1Bug.glade
gtk-builder-convert $1Bug.glade $1.xml
rm $1Bug.glade
