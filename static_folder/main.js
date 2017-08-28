// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
};
function handlerOut(){
 $(this).css("background-color","blue");
};

// Left side Handler uses AJAX to send the data on the page to the server
function handlerVoteLeft(){
  $.ajax({
    type: "POST",
    url: "/vote/",
    dataType: 'json',
    // EVEN BIGGER NOTICE: YOU CAN SIMPLIFY THIS FURTHER BY: creating a function that alternates between left/right selection
    // broswer uses ajax to send the data from the unselected and selected lyric
    data: JSON.stringify(
      {
        "lyric-selected": $('#lyric-left').text(),
        "song-name-selected": $('#song-name-left').text(),
        "artist-name-selected":$("#artist-name-left").text(),
        "lyric-unselected":$('#lyric-right').text(),
        "song-name-unselected":$('#song-name-right').text(),
        "artist-name-unselected":$('#artist-name-right').text()
      })
      // This section updates BOTH the unselected and selected lyrics with new lyrics
  }).done(function( data ) {
    $('#lyric-span-left').text(data['lyric-selected']);
    $('#song-span-left').text(data['song-name-selected']);
    $('#artist-name-left').text(data['artist-name-selected']);
    $('#lyric-span-right').text(data['lyric-unselected']);
    $('#song-span-right').text(data['song-name-unselected']);
    $('#artist-name-right').text(data['artist-name-unselected']);
  });

};

//AJAX Functionality for the right side handler
function handlerVoteRight(){
  $.ajax({
    type: "POST",
    url: "/vote/",
    dataType: 'json',
    // EVEN BIGGER NOTICE: YOU CAN SIMPLIFY THIS FURTHER BY: creating a function that alternates between left/right selection
    // Data sends the data from the unselected and selected lyric
    data: JSON.stringify(
      {
        "lyric-selected": $('#lyric-right').text(),
        "song-name-selected": $('#song-name-right').text(),
        "artist-name-selected":$("#artist-name-right").text(),
        "lyric-unselected":$('#lyric-left').text(),
        "song-name-unselected":$('#song-name-left').text(),
        "artist-name-unselected":$('#artist-name-left').text()
      })
      // This section updates BOTH the unselected and selected lyrics with new lyrics
  }).done(function( data ) {
    $('#lyric-span-right').text(data['lyric-selected']);
    $('#song-span-right').text(data['song-name-selected']);
    $('#artist-name-right').text(data['artist-name-selected']);
    $('#lyric-span-left').text(data['lyric-unselected']);
    $('#song-span-left').text(data['song-name-unselected']);
    $('#artist-name-left').text(data['artist-name-unselected']);
  });
};


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  $('#section-left').click(handlerVoteLeft);
  $('#section-right').click(handlerVoteRight);
}



$(document).ready(setupHandlers);
