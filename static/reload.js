function update_feed_status() {
    var xhr = new XMLHttpRequest();
    xhr.open('get', '/get_last_feed_string', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var json_data = JSON.parse(xhr.responseText)
            document.getElementById("feed_status").innerHTML = json_data["title"];
            document.getElementById("feed_time").innerHTML = json_data["subtitle"];
        }
    }
    xhr.send();
}