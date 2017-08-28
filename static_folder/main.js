// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
};
function handlerOut(){
 $(this).css("background-color","blue");
};

// Handlers used for using AJAX to send the data on the page to the server
function handlerVoteLeft(){
  $.ajax({
    type: "POST",
    url: "/vote/",
    dataType: 'json',
    // EVEN BIGGER NOTICE: YOU CAN SIMPLIFY THIS FURTHER BY: creating a function that alternates between left/right selection
    // NOTICE: Modify 'data' so that it also sends the data from the unselected lyric
    data: JSON.stringify(
      {
        "lyric-selected": $('#lyric-left').text(),
        "song-name-selected": $('#song-name-left').text(),
        "artist-name-selected":$("#artist-name-left").text(),
        "lyric-unselected":$('#lyric-right').text(),
        "song-name-unselected":$('#song-name-right').text(),
        "artist-name-unselected":$('#artist-name-right').text()
      })
      // NOTICE: Modify data so that it updates BOTH the unselected and selected lyric with a new lyric
  }).done(function( data ) {
    $('#lyric-span-left').text(data['lyric-selected']);
    $('#song-span-left').text(data['song-name-selected']);
    $('#artist-name-left').text(data['artist-name-selected']);
    $('#lyric-span-right').text(data['lyric-unselected']);
    $('#song-span-right').text(data['song-name-unselected']);
    $('#artist-name-right').text(data['artist-name-unselected']);
  });

};

// NOTICE: AJAX Functionality has to be added to the Right-side section
function handlerVoteRight(){

};


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  $('#section-left').click(handlerVoteLeft);
  $('#section-right').click(handlerVoteRight);
}



$(document).ready(setupHandlers);
