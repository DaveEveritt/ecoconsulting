#!/usr/bin/perl -w

use strict;
use CGI;
use Mail::Send;

#########################################
# User Params / Templates
#########################################

my $to = "deveritt\@innotts.co.uk";
my $subject = "From Eco Consulting";
my $mailtext = << "ENDMAIL";
Reply to: <var name>, <var email>\n
<var message>\n\n
ENDMAIL

#########################################
# End of user params
#########################################

my @spamwords = (qw(spybot rankings megagames webcam webcams cheapticket vogue.com valium cigarettes airlines viagra porn httpgoogle httpmsn adultgroups gaymovies googlesearchworld googleus yahoous onlinegambling nakedwoman yahooadult atacand ashwagandha arimidex aricept antabuse amaryl allaceon cheapticketscom),'nice site look this','first page of google','google ranking','increase traffic','search engine marketing');

my $q = new CGI;

# if required fields aren't empty, check for spam and say thanks, else say the fields are blank
if ($q->param('email') && $q->param('message')) {
	foreach($q->param) {$q->param_fetch($_)->[0] =~ s/[^A-Za-z0-9\:\/\@\'\n\r\.\,\-\!~ ]//g;}
	$q->param("name","") unless $q->param("name");

	if (spamcheck()) { # don't tell them they failed
		print $q->redirect("/errors/servererror.shtml");
	}
	else {
		my $msg = new Mail::Send(Subject=>$subject, To=>$to);
		$mailtext =~ s/<var (.*?)>/$q->param($1)/ge;
		my $fh = $msg->open; print $fh $mailtext; $fh->close;
		print $q->redirect("/contact/contact-thanks.shtml");
	}
}
else {
	print $q->redirect("/contact/contact-blank.shtml");
}

sub spamcheck {
	return 1 if ($q->param("sum") =~ /\D+/ || $q->param("sum") != "5" || $q->param("about") || $q->param("comment"));
	return 1 if ($q->param("link") ne "http://");
	my $msgcheck = lc($q->param("message"));
	foreach (@spamwords) { return 1 if (index($msgcheck,$_) > -1) }
}

exit;
