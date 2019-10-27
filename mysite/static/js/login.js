$(function()
{
});
 
// ajax submission
$("#form_login").submit(function(e)
{
	e.preventDefault(); // prevent the default submission
	var form = $(this);
	var url = form.attr('action');
	$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(),
			success: function(response)
			{
				// not implemented
				alert("post success!");
			}
	});
	loadFrame("notes");	// debug
});