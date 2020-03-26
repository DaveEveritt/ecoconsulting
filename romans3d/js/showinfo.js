$(document).ready(function(){
	$('#showhide').toggle(
		function() {
			$('#sidebar').animate({right:0}),
			$('#content').animate({right:130}),
			$('.info').css("color","rgba(240,100,100,1.0)")
		},
		function() {
			$('#sidebar').animate({right:-270}),
			$('#content').animate({right:0}),
			$('.info').css("color","#006")
		}
	),
	$('#sidebar').hover(
		function() { $(this).animate({opacity:0.9},{queue:false,duration:900}) },
		function() { $(this).animate({opacity:0.35},{queue:false,duration:900}) }
	)
});
