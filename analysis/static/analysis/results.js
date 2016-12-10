$(document).ready(function() {
    var impact = document.getElementById('impact').innerHTML;

    document.getElementById('impact').style.color = "green";

    if(impact == 'negative') {
      document.getElementById('impact').style.color = "red";
    }
    console.log(impact);


});
