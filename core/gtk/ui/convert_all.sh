#!/bin/bash
for i in $(ls *.glade|sed 's/.glade//g');do 
	sh convert_gui.sh $i;
done
