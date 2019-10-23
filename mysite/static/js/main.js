$(function()
{
	load("..\\static\\_ajaxframes\\home.html");	// load home page
});

// load a page into #pagebox
function load(url)
{
	$.ajax({
			type: "GET",
			url: url,
			success: function(response)
			{
				
				// $("#pagebox").html($("body", "Hello world").html());
				$("#pagebox").html(response);
				//$("head").append($("head", response).html());
			},
			error: function (jqXHR, exception)
			{
				alert("[ajax error] " + jqXHR.status + " " + exception);
			},
	});
}