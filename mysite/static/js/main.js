var auth_user_id = null;

$(function()
{
	loadFrame("home");	// load home page
    // DEBUG : skip login
    //auth_user_id = 1;
    //loadFrame("notes");
});

// load a page into #pagebox
function load(urlPage, urlCSS, urlJS)
{
	$.ajax({
			type: "GET",
			url: urlPage,
			success: function(response)
			{
				$("#frame_css").attr("href", urlCSS);
				$("#pagebox").html($(response));
				$.getScript(urlJS);
			},
			error: function (jqXHR, exception)
			{
				alert("[ajax error] " + jqXHR.status + " " + exception);
			},
	});
}

// load a frame with name
function loadFrame(name)
{
	load("..\\static\\_ajaxframes\\" + name + ".html", "..\\static\\css\\" + name + ".css", "..\\static\\js\\" + name + ".js");
}