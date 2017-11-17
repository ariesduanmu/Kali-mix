#!/usr/bin/perl

use strict;
use warnings;
use feature 'say';


use File::Slurp;


my @FILENAMES = ("found1", "found2", "found3");
my @LETTERS = ("A" .. "Z");
my @ENGLISH_FREQ = ("E", "T", "A", "O", "I", "N", "S", 
                    "H", "R", "D", "L", "C", "U", "M", 
                    "W", "F", "G", "Y", "P", "B", "V", 
                    "K", "J", "X", "Q", "Z");

my $ENCRYPTED_STRING = read_file("krypton4");
$ENCRYPTED_STRING =~ s/\s+//g;


sub count_frequency {
    my ($string) = @_;
    my %occurences = count_occurence($string);
    return map { $_ => $occurences{$_} / length($string) } keys %occurences;
}

sub count_occurence {
    my ($string) = @_;
    my %frequency = map { $_ => 0 } @LETTERS;
    foreach (split //, $string) {
        $frequency{$_}++;
    }
    return %frequency;
}

sub decrypt {
    my (%text_freq) = @_;
    my @text = ();

    foreach my $name ( sort { $text_freq{$b} <=> $text_freq{$a} } keys %text_freq ) {
        push @text, $name;
    }

    # This line is wrong... ?
    # Getting 52 key length ugh, tired now... Maybe fix tomorrow.
    my %key = map { $text[$_] => $ENGLISH_FREQ[$_] } (0 .. $#text);    

    foreach (split //, $ENCRYPTED_STRING) {
        print "$key{$_}";
    }
    say "";
}

foreach (@FILENAMES) {
    my $text = read_file($_);
    $text =~ s/\s+//g;
    decrypt(count_frequency($text));
}


