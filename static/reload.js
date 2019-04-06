function update_feed_status() {
    var xhr = new XMLHttpRequest();
    xhr.open('get', '/get_last_feed_string', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) { 
            document.getElementById("feed_status").innerHTML = xhr.responseText;
        }
    }
    xhr.send();
}