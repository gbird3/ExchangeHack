$('#trackStocks').on('click', function(event){
    event.preventDefault();
    //console.log('button was clicked to start tracking stocks');
    $.get('startTrack/');
});
