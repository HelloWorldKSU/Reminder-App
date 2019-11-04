var notes;
var notesIndex;

$(function()
{
    loadNotes();
});

function showEditor(b)
{
    if (b)
        $("#editorbox").css("visibility", "visible");
    else
        $("#editorbox").css("visibility", "hidden");
}

$(".notebox_create").click(function()
{
    showEditor(true);
});

$("#editorbox").click(function(e)
{
    if (e.target !== this)
        return;
    showEditor(false);
});

// load notes
function loadNotes()
{
    if (auth_user_id == null)
        return;
	$.ajax({
			type: "GET",
			url: "\\note",
			data: {
                "user_id" : auth_user_id
            },
            cache: false,
			success: function(response)
			{
				if (!response.success)
				{
					//alert('failed!');
				}
				else
				{
                    $("#notebox_template").nextAll().remove();
                    notes = response.notes;
                    notesIndex = 0;
                    showNextNote();
				}
			}
	});
}

// show next note and delay
function showNextNote()
{
    if (notes == null || notesIndex >= notes.length)
        return;
    var note = notes[notesIndex];
    notesIndex++;
    appendNote(note.title, note.content);
    setTimeout(showNextNote, 50);
}
 
 // append a note
function appendNote(title, content)
{
	var note = $("#notebox_template").clone().appendTo("#notepanel");
	note.find(".note_title").html(title);
	note.find(".note_content").html(encodeNoteContent(content));
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

function encodeNoteContent(content)
{
    var str = "";
    content.split("\n").forEach(function(s)
    {
        str += "<p>" + s + "</p>";
    });
    return str;
}

// ajax submission
$("#form_createnote").submit(function(e)
{
	e.preventDefault(); // prevent the default submission
	var form = $(this);
	var url = form.attr('action');
	$.ajax({
			type: "POST",
			url: url,
			data: form.serialize() + "&" + $.param({
                user_id : auth_user_id
            }),
			success: function(response)
			{
				if (!response.success)
				{
					alert('Post failed!');
				}
				else
				{
                    showEditor(false);
                    loadNotes();
				}
			}
	});
});