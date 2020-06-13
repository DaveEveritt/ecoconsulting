#!/usr/bin/perl
use strict;
use CGI;
use Mail::Send;

my $q = new CGI;
my %vals;																              # Form / Replacement values
my @pfields = (qw(name email comment));								# Form Fields
my @allfields = (qw(page approved date),@pfields);		# Other fields
my @compulsory = (qw(name comment));									# Compulsory Fields
my @comments = get_page_comments($ENV{DOCUMENT_URI}); # Comments for this page
my $template = join("",(<DATA>));	# HTML Template
my ($chunk) =($template =~/\[COMMENTS\](.*)\[ENDCOMMENTS\]/s);        # Looped Comment Chunk
my $replace="";															                          # Replace chunk with...
foreach my $comment (grep {$_->{approved} eq "Approved"} @comments) {	# ...all approved comments
	my $c = $chunk;														                # Make a copy...
	foreach(@allfields) {$c =~ s/\[\U$_\E\]/$comment->{$_}/;}	# replace [THIS] with $_->{this}
	$replace .= $c;												                    # and add it to the rest
}
$template =~s/\[COMMENTS\](.*)\[ENDCOMMENTS\]/$replace/s;		# replace chunk with list
my @spamwords = (
  qw( accutane acyclovir adderall albendazole albertine albuterol allaceon alomid amaryl ambien amitriptyline amoxicillin amoxil ampicillin anastrozole antabuse antibiotic antibiotics antiperspirant aricept arimidex aripiprazole atarax atenolol ativan bimatoprost buspar celebrex celexa cialis cipralex cipro clomid clomipramine clopidogrel codeine cymbalta cytotec deltasone diflucan dosage doxycycline dugis duloxetine effexor eriacta erythromycin flagyl fluconazole fluoxetine gabapentin garcinia hemorrhoids hydroxyzine icomelmer imitrex inderal indocin kamagra lasix levitra lexapro louboutin methocarbamol minoxidil mirtazapine moncler naprosyn nexium nolvadex orlistat paroxetine paxil pernicka pharmacy phentemine prescription priligy propecia propranolol proscar prosolution remeron renova robaxin rogaine seroquel sildenafil strattera suhagra sumatriptan synthroid tadacip tamoxifen tenormin tetracycline topamax tramadol trazodone valium vaporizer ventolin viagra vibramycin wellbutrin xanax xenical zithromax zoloft zovirax zygor adultgroups airlines amerihealth babywearing backlinks basketball betting carpet casino chanel cheap cigarettes closeupmagazine dating defense dental dissertation dkny essay federal flooring football footwear foxyjackyexposed funerals gaymovies givenchy googlesearchworld googleus goose handbag hermes horny hollister httpgoogle httpmsn jewelry lending longchamp medicare megagames nakedwoman nfl nike onlinegambling outlet payday pizza poker pokies porn prada rankings resume tiffany traffic vacuum vuitton webcam webcams yahooadult yahoous xrumortest xrumertest),
  '∫–∞–∑','∏–≥','[url=','[link=','barny','hotmail.com','first page of google','google ranking','increase traffic','ing.com','search engine marketing','am loving it','been on the lookout','this blog','my web','my homepage','my webpage','my home page','my page','my weblog','my blog','my web-site','my website','my site','blog platform','off topic','your blog','your weblog','your contact details','rss feed','this topic','blog loading','nice site look this','this site before','university together','school together','full movies','news papers','opposite experts','realize your dreams','aspiring writers','honest with their spam','pirate bay','super bowl','baby carrier','baby clothes','ralph lauren','replica watches','oakleys','michael kor','red sox','sandy birkin','kate moss','heel lifts','shoe lifts','toms shoes','mont blanc','cash advance','personal loans','business loans','credit loans','goodfinance','slot machines','hello. and bye.','yourmail@gmail.com','.ru'
);



# ============================
# If comment submitted:
#   checks for required fields,
#   sanitizes,
#   traps duplicate submits,
#   checks for errors,
#   checks for spam,
#   writes to comments file,
#   says thanks even for spam,
#   empties fields. Phew.
# ============================
if ($q->param("submit")) {
	foreach (@pfields) { # sanitise
		$vals{$_} = $q->param($_);
		$vals{$_} =~ s/[^A-Za-z0-9\s,.;\(\)\[\]]\-//g;
		$vals{$_} = substr($vals{$_}, 0, 2000)."..." if (length($vals{$_}) > 2000);
	}
	foreach(@compulsory) {
		unless ($q->param($_)) {$vals{message} .= "Please give a $_<br>";}
	}
	if (grep {$_->{name} eq $vals{name} && $_->{comment} eq $vals{comment}} @comments) { # duplicates
		$vals{message} .= "You have already posted this comment and it is awaiting approval";
	}
	unless ($vals{message}) { # No errors?
		unless (spamcheck()) { write_comment(); send_email(); }
		%vals=('message'=>"Thanks - comment awaiting approval.");
	}
}

# ============================
# does/prints template, ends
# ============================
foreach(@pfields,'message') {$template =~ s/\[\U$_\E\]/$vals{$_}/;}
print $template;
exit;

# ============================
# reads comments from file
# ============================
sub get_page_comments {
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

# ============================
# writes new comments to file
# ============================
sub write_comment {
	my $d = localtime();  # Dow Mon DD HH:MM:SS YYYY
	$d =~ s/:\d\d\s/ /;
	%vals=(%vals,'date'=>$d,'approved'=>"Unapproved",'page'=>$ENV{DOCUMENT_URI});
	$vals{comment} =~s/[\r\n]+/<br \/>/g;	# newlines to br tags (remove self-closing for HTML4/5)
	open FILE, ">>./comments.tab";
	print FILE join("\t",map {$vals{$_}} @allfields),"\n";
	close FILE;
}

sub spamcheck { # does what it says
	my $msgcheck = lc($q->param("comment"));
	foreach (@spamwords) { return 1 if (index($msgcheck,$_) > -1) }
}

# ============================
# sends email notification
# ============================
sub send_email {
	my $to = "deveritt\@innotts.co.uk";
	my $subject = "Eco Consulting, page: " . $vals{"page"};
	my $mailtext = $vals{"comment"} . " - " . $vals{"name"} . ", " . $vals{"email"} . "\n\n - page: " . $vals{"page"};
	my $msg = new Mail::Send(Subject=>$subject, To=>$to);
	my $fh = $msg->open; print $fh $mailtext; $fh->close;
}


# ============================
# Comment template HTML+vars
# ============================
__DATA__

		<h2 id="commenthead" class="notes">Comments:</h2>

[COMMENTS]		
		<p class="comment">
			<strong>From: [NAME], [DATE]</strong><br />
			[COMMENT]
		</p>
[ENDCOMMENTS]

		<h2 class="notes">Add a comment&hellip;</h2>
		<p>Comments (2000 characters/300 word limit) appear after approval. Add your email if you'd like a reply <em>(it can be entered safely and won't be published, stored or spammed)</em>.</p>
		<p class="thanks">[MESSAGE]</p>
		<form method="get" action="" class="comments">
			<table>
				<tr><td>Name: </td><td><input type="text" name="name" size="30" value="[NAME]"/></td></tr>
				<tr><td>Email (optional): </td><td><input type="text" name="email" size="30" value="[EMAIL]"/></td></tr>
				<tr><td>Comment: </td><td><textarea name="comment" rows="5" cols="50">[COMMENT]</textarea></td></tr>
			</table>
			<p><input type="submit" value="Submit your comment" name="submit" title="send" /></p>
		</form>
