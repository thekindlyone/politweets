$(document).ready(function(){
    $('#searchform').submit(function(event){
        event.preventDefault();
        searchterm=$("#termbox").val();
        if ($('input').val() != '') {
            $('input:first').blur();
            $('input:first').focus();
            $.get("/show",{term : searchterm}, function(data, status){
                chart=data;
                $(".chart_container").html(chart);
            });
        }
    });
});