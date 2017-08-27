// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
}
function handlerOut(){
 $(this).css("background-color","blue");
}

// Handlers used for transforming lyric elements into clickable button elements
function handlerVoteLeft(lyric_left,song_name_left,artist_name_left){
  console.log("Left side was clicked")
  console.log()

}
function handlerVoteRight(){
  console.log("Right side was clicked")
}


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  // GET THIS to actually retreive the text for the lyric, song, and artist name so that it can be passed onto the funct()
  $('#section-left').click(
      handlerVoteLeft(
        $('#section-left').filter("#lyric-left")
      )
    )
  $('#section-right').click(handlerVoteRight)
}



$(document).ready(setupHandlers);
