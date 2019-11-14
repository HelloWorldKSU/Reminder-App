$(function()
{
});

$("#dbg_post").click(function()
{
	dbg_submit("POST");
});

$("#dbg_get").click(function()
{
	dbg_submit("GET");
});

function dbg_submit(reqType)
{
	console.log();
	return;
	$.ajax({
			type: reqType,
			url: $("#dbg_path").val(),
			data: form.serialize(),
			success: function(response)
			{
				if (!response.success)
				{
					alert('Login failed!');
				}
				else
				{
					auth_user_id = response.user_id;
					loadFrame("notes");
				}
			}
	});
}