#!/usr/bin/perl
use strict;
use CGI;

my $q = new CGI;
my %vals;																		# Form / Replacement values
my @pfields = (qw(name email comment));								# Form Fields
my @allfields = (qw(page approved date),@pfields);					# Other fields
my @compulsory = (qw(name comment));									# Compulsory Fields
my $template = join("",(<DATA>));										# HTML Template
my @comments = get_page_comments($ENV{DOCUMENT_URI});				# Comments for this page
my ($chunk) =($template =~/\[COMMENTS\](.*)\[ENDCOMMENTS\]/s);	# Looped Comment Chunk
my $replace="";																# Replace chunk with...
foreach my $comment (grep {$_->{approved} eq "Approved"} @comments) {	# ...all approved comments
	my $c = $chunk;															# Make a copy...
	foreach(@allfields) {$c =~ s/\[\U$_\E\]/$comment->{$_}/;}	# replace [THIS] with $_->{this}
	$replace .= $c;															# and add it to the rest
}
$template =~s/\[COMMENTS\](.*)\[ENDCOMMENTS\]/$replace/s;		# replace chunk with list

if ($q->param("submit")) {													# Comment submitted?
	foreach (@pfields) {														# sanitise fields
		$vals{$_} = $q->param($_);
		$vals{$_} =~ s/[^A-Za-z0-9\s,.;\(\)\[\]]\-//g;
		$vals{$_} = substr($vals{$_}, 0, 2000)."..." if (length($vals{$_}) > 2000);
	}
	foreach(@compulsory) {													# Missing Compulsory?
		unless ($q->param($_)) {$vals{message} .= "Please give a $_<br />";}
	}
	if (grep {$_->{name} eq $vals{name} && $_->{comment} eq $vals{comment}} @comments) {
		$vals{message} .= "You have already posted this comment";	# Trap duplicates
	}
	unless ($vals{message}) {												# No errors?
		write_comment();														# Write it
		%vals=('message'=>"Thank you for your comment");			# And say thanks (whilst blanking rest of vals)
	}
}

foreach(@pfields,'message') {$template =~ s/\[\U$_\E\]/$vals{$_}/;}	# Do the rest of the template, and...
print $template;	# Wham, Bam,
exit;					# Thank-you Mam

sub get_page_comments {	# a sub, 'cos we *know* it'll change in the future )
	return unless -e "./comments.tab";
	my $page = shift;
	my @c;
	open FILE, "<./comments.tab";
	while (<FILE>) {
		next unless /^$page\t/;		
		my @vals = split(/\t/);
		push @c, {map {$allfields[$_]=>$vals[$_]} (0..$#allfields)};
	}
	close FILE;
	@c;
}

sub write_comment {
	my $d = localtime();	# Dow Mon DD HH:MM:SS YYYY
	$d =~ s/:\d\d\s/ /;
	%vals=(%vals,'date'=>$d,'approved'=>"Unapproved",'page'=>$ENV{DOCUMENT_URI});
	$vals{comment} =~s/[\r\n]+/<br \/>/g;	# newlines to br tags
	open FILE, ">>./comments.tab";
	print FILE join("\t",map {$vals{$_}} @allfields),"\n";
	close FILE;
}

# The template
__DATA__

[COMMENTS]
		<h2 class="notes commenthead">Comments:</h2>
		
		<p class="comment">
			<strong>From: [NAME], [DATE]</strong><br />
			[COMMENT]
		</p>
[ENDCOMMENTS]

		<h2 class="notes">Add a comment&hellip;</h2>
		<p>Comments (limited to 2000 characters or 300 words) will appear after approval. Your email will <em>not</em> be published.</p>
		<p class="thanks">[MESSAGE]</p>
		<form method="get" action="" class="comments">
			<table>
				<tr><td>Name: </td><td><input type="text" name="name" size="30" value="[NAME]"/></td></tr>
				<tr><td>Email (optional): </td><td><input type="text" name="email" size="30" value="[EMAIL]"/></td></tr>
				<tr><td>Comment: </td><td><textarea name="comment" rows="5" cols="50">[COMMENT]</textarea></td></tr>
			</table>
			<p><input type="submit" value="Submit your comment" name="submit" title="send" /></p>
		</form>
