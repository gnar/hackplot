#!/usr/bin/gnuplot
set term postscript size 30cm, 10cm color
set output "hackdiet_db.ps"

set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m"

set xlabel "date"
set ylabel "weight"
# set xrange ["2005-01-01" : "2013-12-31"]
# set yrange [80 : 100]

plot "hackdiet_db.txt" using 1:2 with lines ls 1 lc 2 notitle, \
     "hackdiet_db.txt" using 1:3 with lines ls 1 lc 1 notitle
