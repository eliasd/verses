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
    // broswer uses ajax to send this data, from the unselected and selected lyrics, to the server
    data: JSON.stringify(
      {
        "lyric-selected": $('#lyric-left').text(),
        "song-name-selected": $('#song-name-left').text(),
        "artist-name-selected":$("#artist-name-left").text(),
        "lyric-unselected":$('#lyric-right').text(),
        "song-name-unselected":$('#song-name-right').text(),
        "artist-name-unselected":$('#artist-name-right').text()
      })
      // Code to run if the request succeeds (is done);
      // The response is passed to the function
      // This function updates BOTH the unselected and selected lyrics with new lyrics
  }).done(function( data ) {
    $('#lyric-span-left').text(data['lyric-selected']);
    $('#song-span-left').text(data['song-name-selected']);
    $('#artist-name-left').text(data['artist-name-selected']);
    $('#feat-artist-left').text(data['feat-artist-selected']);
    $('#lyric-span-right').text(data['lyric-unselected']);
    $('#song-span-right').text(data['song-name-unselected']);
    $('#artist-name-right').text(data['artist-name-unselected']);
    $('#feat-artist-right').text(data['feat-artist-unselected']);
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
  }).fail(function( xhr, status, errorThrown ) {
    alert( "Sorry, there was a problem!" );
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
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
    $('#feat-artist-right').text(data['feat-artist-selected']);
    console.log("RIGHT SIDE CLICKED")
    $('#lyric-span-left').text(data['lyric-unselected']);
    $('#song-span-left').text(data['song-name-unselected']);
    $('#artist-name-left').text(data['artist-name-unselected']);
    $('#feat-artist-left').text(data['feat-artist-unselected']);

  }).fail(function( xhr, status, errorThrown ) {
    alert( "Sorry, there was a problem!" );
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
  });
};


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  $('#section-left').click(handlerVoteLeft);
  $('#section-right').click(handlerVoteRight);
}



$(document).ready(setupHandlers);
