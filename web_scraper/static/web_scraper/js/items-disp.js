$(function(){
    $(".col:hidden").slice(0, 15).show();
    $(".my-3:hidden").slice(0, 5).show();
    $("#loadMore").on("click", function(e){
        e.preventDefault();

        $(".col:hidden").slice(0, 15).show();
        $(".my-3:hidden").slice(0, 5).show();
        if($(".col:hidden").length == 0) {
            $("#loadBtn").prop('disabled', true);
        }
    });

    $('.col').hover(
        //when hovering
        function(){
            $(this).animate({
                marginTop:"-=0.5%",
            }, 100);
        },
        //putting mouse away
        function(){
            $(this).animate({
                marginTop:"0%",
            }, 100);
        }
    );
});