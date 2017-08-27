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
    // NOTICE: Modify 'data' so that it also sends the data from the unselected lyric
    data: JSON.stringify(
      {
        "lyric": $('#lyric-left').text(),
        "song-name": $('#song-name-left').text(),
        "artist-name":$("#artist-name-left").text()
      })
      // NOTICE: Modify data so that it updates BOTH the unselected and selected lyric with a new lyric
  }).done(function( data ) {
    $('#lyric-span-left').text(data['lyric']);
    $('#song-span-left').text(data['song-name']);
    $('#artist-name-left').text(data['artist-name']);
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
