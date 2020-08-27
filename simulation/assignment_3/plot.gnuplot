set datafile separator ','

set key autotitle columnhead
set key left top
set xlabel 'Current [A]' # label for the X axis

set ylabel 'Force [N]' # label for the Y axis
set ytics nomirror # dont show the tics on that side

set y2label 'Flux Density [T]' # label for second axis
set y2tics # enable second axis

plot 'result.csv' using 1:2 with lines, '' using 1:3 with lines axis x1y2
