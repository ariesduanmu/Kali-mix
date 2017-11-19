use strict;
use warnings;


my %letter_frequence = (
	"E" => 12.70, 
	"T" => 9.06, 
	"A" => 8.17, 
	"O" => 7.51, 
	"I" => 6.97, 
	"N" => 6.75, 
	"S" => 6.33, 
	"H" => 6.09, 
	"R" => 5.99, 
	"D" => 4.25, 
	"L" => 4.03, 
	"C" => 2.78, 
	"U" => 2.76, 
	"M" => 2.41, 
	"W" => 2.36, 
	"F" => 2.23, 
	"G" => 2.02, 
	"Y" => 1.97, 
	"P" => 1.93, 
	"B" => 1.29, 
	"V" => 0.98, 
	"K" => 0.77, 
	"J" => 0.15, 
	"X" => 0.15, 
	"Q" => 0.10, 
	"Z" => 0.07

	);

sub read_file{
	my ($filename) = @_;
	open CONFIG,$filename or die "Can't open file ".$filename;
	my $text = <CONFIG>;
	chomp $text;
	$text =~ s/\s//g;
	close CONFIG;

	return $text;

}

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

sub get_single_key{
	my $max_score = 0;
	my $best_k = 0;
	for (my $i = 0; $i < 26; $i++){
		my $score = 0;
		foreach my $string(@_){
			my $pt = plain_text($string, $i);
			$score += $letter_frequence{$pt};
		}

		if($score > $max_score){
			$max_score = $score;
			$best_k = $i;
		}

	}

	return $best_k;

}

sub plain_text{
	my ($cipter_text, $k) = @_;
	my $pt = chr(((ord($cipter_text) - ord('A') - $k) % 26) + ord('A'));

	return $pt;
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
