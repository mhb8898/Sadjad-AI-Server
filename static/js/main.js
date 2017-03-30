function listen(token){
  namespace = '/game';

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  socket.on('connect', function() {
      socket.emit('auth', {'token': token});
  });

  socket.on('result', function(msg) {
      data=$.parseJSON(msg.data)
      printBoard(data);

  });
}
function printBoard(map)
{
  $('#board').empty();
  table=$('<table/>')
  for(row in map){
    row=$.parseJSON(row);
    tr=$('<tr/>')
    for(var item in map[row]){
      tr.append('<td class="'+map[row][item].type+'"></td>');
    }
    table.append(tr);
    $('#board').append(table)

  }
}
