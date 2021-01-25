$(document).ready(function(){

    $("#run-demo").click(function(event) {
        console.log("clicked");
        $.get('/api/function1', function(data) {
            console.log(data);
            $('#output1').html(data);
        });
    });

    $("#button2").click(function(event) {
        $.get('/api/function2', function(data) {
            console.log(data);
            $('#output2').html(data);
        });
    });

});