$(function()
{
	for(var i = 0; i <=15; i++)
		setTimeout(function() {appendNote();}, i * 50);
});
 
 // append a note
function appendNote()
{
	var note = $("#notebox_template").clone().appendTo("#notepanel");
	note.find(".note_content").html("<p>something to do</p>".repeat(Math.ceil(Math.random() * 7)));
	note.css("display", "block");
	// move-in animation
	note.find(".notebox").css(
	{
		top : "10px",
		opacity : "0.3",
	}).animate({
		top : "0px",
		opacity : "1",
  }, 300);
}