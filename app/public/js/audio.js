function audioPlayer(){
    var currentSong = 0;
    $('#player')[0].src = $('#lib li a')[0];
    $('#player')[0].play();
    $('#lib li a').click(function(e){
        e.preventDefault();
        $('#player')[0].src = this;
        $('#player')[0].play();
        $('#lib li').removeClass("current-song");
        currentSong = $(this).parent().index();
        $(this).parent().addClass("current-song");
    });

    $("#player")[0].addEventListener("ended", function() {
        currentSong++;
        if(currentSong == $('#lib li a').length)
            currentSong = 0;
        $("#lib li").removeClass("current-song");
        $("#lib li:eq("+currentSong+")").addClass("current-song");
        $("#player")[0].src = $("#lib li a")[currentSong].href;
        $('#player')[0].play();

    });
}

function audioPlayer2(){
    var currentSong = 0;
    $('#player')[0].src = $('#res li a')[0];
    $('#player')[0].play();
    $('#res li a').click(function(e){
        e.preventDefault();
        $('#player')[0].src = this;
        $('#player')[0].play();
        $('#res li').removeClass("current-song");
        currentSong = $(this).parent().index();
        $(this).parent().addClass("current-song");
    });

    $("#player")[0].addEventListener("ended", function() {
        currentSong++;
        if(currentSong == $('#res li a').length)
            currentSong = 0;
        $("#res li").removeClass("current-song");
        $("#res li:eq("+currentSong+")").addClass("current-song");
        $("#player")[0].src = $("#res li a")[currentSong].href;
        $('#player')[0].play();

    });
}