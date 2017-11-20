use strict;
use warnings;

BEGIN {
	require '../utility.pl';
}

our(%letter_frequence);

sub get_key{
	my $found1_text = read_file "found1";
	my $found2_text = read_file "found2";

	my @key = ();
	for (my $i = 0; $i < 6; $i++){
		my @strings = ();
		for (my $j = $i; $j < length($found1_text); $j+=6){
			push(@strings, substr($found1_text,$j,1))
		}
		for (my $j = $i; $j < length($found2_text); $j+=6){
			push(@strings, substr($found2_text,$j,1))
		}

		push(@key, get_single_key(@strings))
	}

	return @key;
}


sub decrypt{
	my $k5_text = read_file "krypton5";
	my @key = get_key;
	my $plaintext = "";
	for(my $i = 0; $i < length($k5_text); $i++){
		$plaintext .= plain_text(substr($k5_text,$i,1), @key[$i % 6]);
	}
	return $plaintext;
}

print(decrypt);
print("\n");
