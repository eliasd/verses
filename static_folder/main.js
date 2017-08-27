// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
};
function handlerOut(){
 $(this).css("background-color","blue");
};

// Handlers used for transforming lyric elements into clickable button elements
function handlerVoteLeft(){
  $.ajax({
    type: "POST",
    url: "/vote/",
    dataType: 'json',
    data: JSON.stringify(
      {
        "lyric": $('#lyric-left').text(),
        "song-name": $('#song-name-left').text(),
        "artist-name":$("#artist-name-left").text()
      })
  }).done(function( data ) {
    $('#lyric-span-left').text(data['lyric']);
    $('#song-span-left').text(data['song-name']);
    $('#artist-name-left').text(data['artist-name']);
  });

};
function handlerVoteRight(){
  console.log("Right side was clicked")
  console.log($('#lyric-right').text());
  console.log($('#song-name-right').text());
  console.log($('#artist-name-left').text());
};


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  // GET THIS to actually retreive the text for the lyric, song, and artist name so that it can be passed onto the funct()
  $('#section-left').click(handlerVoteLeft);
  $('#section-right').click(handlerVoteRight);
}



$(document).ready(setupHandlers);
