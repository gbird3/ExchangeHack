var config = {
    apiKey: "AIzaSyCYaZJlTQjeI-SsWTzW6xplKc7Ja7I-s8Q",
    authDomain: "exchangehack-143922.firebaseapp.com",
    databaseURL: "https://exchangehack-143922.firebaseio.com/",
    storageBucket: "exchangehack-143922.appspot.com"
};
firebase.initializeApp(config);
var db = firebase.database();
var tweetCount = $('#tweetCount');
db.ref('counter').on('value', function(snapshot) {
    tweetCount.html(snapshot.val().toLocaleString());
})
