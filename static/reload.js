function feed_status_error(response) {
    var error = "Unable to get last feed time."
    document.getElementById("feed_status").innerHTML = error;
    document.getElementById("feed_time").innerHTML = "Sorry";
    console.log(error + " " + response);
}

function update_feed_status() {
    fetch('/get_last_feed_string').then(
        function(response) {
            if (response.status !== 200) {
                feed_status_error(response.status)
                return;
            }
            response.json().then(
                function(data) {
                    document.getElementById("feed_status").innerHTML = data["title"];
                    document.getElementById("feed_time").innerHTML = data["subtitle"];
                }
            );
        }
    ).catch(function(err) {feed_status_error(err)});
}

// Update once per minute
setInterval(update_feed_status, 1000 * 60);