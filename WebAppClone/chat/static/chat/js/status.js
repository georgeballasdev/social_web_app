// Handle user online status
const statusUrl = 'ws://' + window.location.host + '/ws/status/';
const statusSocket = new WebSocket(statusUrl);

statusSocket.onopen = () => {
    statusSocket.send(JSON.stringify({
        status: true
    }));
}

statusSocket.onmessage = (e) => {
    data = JSON.parse(e.data);
    let user = chatWindow.find('.friend[data-friend-username=' + data['user'] + ']');
    let status = data['status'];
    if (status === true) {
        user.find('.status').addClass('online');
    }
    else {
        user.find('.status').removeClass('online');
    }
}

window.addEventListener('beforeunload', () => {
    statusSocket.send(JSON.stringify({
        user: DATASET.username,
        status: false
    }));
})