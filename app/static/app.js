var data = {
  'memories': null,
  'user_memories': null
}

var memoryData = {
  'memory': {'title': '',
             'time': '',
             'id': ''}
}

function memories_callback(response) {
  data.memories = JSON.parse(response).memories;
}


function get_user_callback(response) {
  data.user_memories = JSON.parse(response).memory_ids;
}

function memory_callback(response) {
  memoryData.memory = JSON.parse(response).memory;
}

Vue.component('memory-item', {
    'props': ['title', 'time', 'id'],
    'template': '<li class="memory-item" v-on:click="memoryOnclick(id)">\
                 <span class="memory-item-title">{{ title }}</span>&nbsp;<span class="memory-item-date">({{ time }})</span>\
                 </li>',
    'methods': {
      'memoryOnclick': function(id) {
        token = sessionStorage.getItem('token');
        request('GET', '/api/memory?id=' + id + '&lat=26&long=36',
                {'Authorization': token}, null, memory_callback);

      },
    'local_time': local_time
    }
});

Vue.component('memory', {
  'props': ['title', 'text', 'time', 'id', 'user'],
  'template': '<div class=""><span>{{ title }} {{ time }} {{ user }} </span><span>{{ text }}</span>'
})

var app = new Vue({
  'el': '#app',
  'data': data,
  'methods': {
    'fetch_memories_nearby': function () {
      token = sessionStorage.getItem('token');
      request('GET', '/api/memory?lat=26&long=36',
              {'Authorization': token}, null, memories_callback);
    },
    'fetch_user_memories': function () {
      token = sessionStorage.getItem('token');
      request('GET', '/api/user',
              {'Authorization': token}, null, get_user_callback);
    },
    'local_time': local_time
  }
});

var memoryApp = new Vue({
  'el': '#memory-app',
  'data': memoryData,
  'methods': {
    'local_time': local_time
  }
});

app.fetch_user_memories();
app.fetch_memories_nearby();
