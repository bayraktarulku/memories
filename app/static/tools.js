function request(method, endpoint, headers, data, callback) {
  var r = new XMLHttpRequest();
  r.open(method, endpoint);
  header_keys = Object.keys(headers);
  for (var i = header_keys.length - 1; i >= 0; i--) {
    r.setRequestHeader(header_keys[i], headers[header_keys[i]]);
  }
  r.onreadystatechange = function() {
    if (r.readyState == 4){
        callback(r.responseText);
    }
  };
  r.send(data);
}

function local_time(timestamp){
  var a = new Date(timestamp * 1000);
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + (hour > 9 ? hour : '0'+hour) + ':' + (min > 9 ? min : '0'+min);
  return time;
}
