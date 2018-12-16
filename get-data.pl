#!/usr/bin/perl

open(SYMBOLS, "SP500.txt");

$a = "00";
$b = "19";
$c = "2000";
$d = "01";
$e = "6";
$f = "2007";
$g = "d";

while(<SYMBOLS>)
{
  $check=0;
  chomp($_);
  $SYM = $_;
  while($check==0)
  {
    $URL = "http://ichart.finance.yahoo.com/table.csv?";
    $QSTR = "s=".$SYM;
    $URL .= $QSTR."&ignore=.csv";
    print("\nNow retrieving...$SYM\n");
    $cmd = "wget -O $SYM.dat -q $URL";
    print("$cmd");
    `$cmd`;

    open(CHKFILE, "<$SYM.dat");
    print("Checking file integrity...\n");

     $_ = <CHKFILE>;

     split(/,/, $_);
     ($day, $mo, $yr) = split(/-/, $_[0]);
     $firstyear = $yr;

    $numlines = 0;

    while(<CHKFILE>) 
    { 
      $numlines++;
    }

    
   # if($numlines > 1500)
   # {
      $check = 1;
      print("File looks good! (", $numlines, " lines)\n");
   
   # } else {
   #   print("File contains no data, re-acquiring...\n");
   # }
    close(CHKFILE);
  }
}
