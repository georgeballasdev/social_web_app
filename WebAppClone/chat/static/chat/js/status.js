// Handle user online status
const statusUrl = 'ws://' + window.location.host + '/ws/status/';
const statusSocket = new WebSocket(statusUrl);

statusSocket.onmessage = (e) => {
    console.log('got status notification:')
    console.log(e.data);
    data = JSON.parse(e.data);
    let user = data['user'];
    let status = data['status'];
    if (status == true) {
        $('#'+user).find('span').addClass('online');
    }
    else {
        $('#'+user).find('span').removeClass('online');
    }
}