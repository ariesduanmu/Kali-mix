use strict;
use warnings;

#run like this `perl test.pl "echo test|"`

my $filehandle = "ARGV";

while (<$filehandle>) {
  print $_;
}
