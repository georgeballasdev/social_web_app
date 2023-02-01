// Handle user online status
const statusUrl = 'ws://' + window.location.host + '/ws/status/';
const statusSocket = new WebSocket(statusUrl);

statusSocket.onmessage = (e) => {
    data = JSON.parse(e.data);
    let user = chat_window.find('.friend[data-friend-username=' + data['user'] + ']');
    let status = data['status'];
    if (status === true) {
        user.find('.status').addClass('online');
    }
    else {
        user.find('.status').removeClass('online');
    }
}