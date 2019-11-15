var notes;
var notesIndex;

$(function()
{
    loadNotes();
});

function showEditor(b, note)
{
    if (note)
    {
        var noteData = note.data("note");
        $("#editor").data("note_id", noteData.id),
        $(".editor_title input").val(noteData.title);
        $(".editor_content textarea").val(noteData.content);
        $("#editorbtn_post").css("display", "none");
        $("#editorbtn_save").css("display", "inline-block");
    }
    else
    {
        $(".editor_title input").val("");
        $(".editor_content textarea").val("");
        $("#editorbtn_post").css("display", "inline-block");
        $("#editorbtn_save").css("display", "none");
    }
    if (b)
        $("#editorbox").css("visibility", "visible");
    else
        $("#editorbox").css("visibility", "hidden");
}

$("#note_create").click(function()
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
                    $("#note_template").nextAll().remove();
                    notes = response.notes;
                    notesIndex = notes.length - 1;
                    showNextNote();
				}
			}
	});
}

// show next note and delay
function showNextNote()
{
    if (notes == null || notesIndex < 0)
        return;
    var noteData = notes[notesIndex];
    notesIndex--;
    createNotebox(noteData).appendTo("#notepanel");
    setTimeout(showNextNote, 50);
}
 
 // create a Notebox from template
function createNotebox(noteData)
{
	var note = $("#note_template").clone().removeAttr('id');
    // attach data object
    note.data("note", noteData);
    // initialize action bar
    note.find(".noteactionbar").hide();
    note.hover(function()
    {
        note.find(".noteactionbar").stop().slideDown(200);
    }, function()
    {
        note.find(".noteactionbar").stop().slideUp(200);
    });
    note.find(".note_edit").click(function()
    {
        editNote(note);
    });
    note.find(".note_delete").click(function()
    {
        deleteNote(note);
    });
    // fill text data
	note.find(".note_title").html(_.escape(noteData.title));
	note.find(".note_content").html(encodeNoteContent(noteData.content));
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
    return note;
}

function encodeNoteContent(content)
{
    var str = "";
    content.split("\n").forEach(function(s)
    {
        str += "<p>" + _.escape(s) + "</p>";
    });
    return str;
}

// post new note
$("#editorbtn_post").click(function()
{
	$.ajax({
			type: "POST",
			url: "/createNote",
			data: $.param({
                user_id : auth_user_id,
                title : $(".editor_title input").val(),
                content : $(".editor_content textarea").val()
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

// edit note
$("#editorbtn_save").click(function()
{
	$.ajax({
			type: "POST",
			url: "/updateNote",
			data: $.param({
                note_id : $("#editor").data("note_id"),
                user_id : auth_user_id,
                title : $(".editor_title input").val(),
                content : $(".editor_content textarea").val()
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

function editNote(note)
{
    showEditor(true, note);
}

function deleteNote(note)
{
    if (!confirm('Are you sure you want to delete this note?'))
        return;
	$.ajax({
			type: "POST",
			url: "/deleteNote",
			data: $.param({
                user_id : auth_user_id,
                note_id : note.data("note").id
            }),
			success: function(response)
			{
				if (!response.success)
				{
					alert('Post failed!');
				}
				else
				{
                    note.remove();
				}
			}
	});
}