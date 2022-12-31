// Handle user online status
status_url = 'ws://' + window.location.host + '/ws/status/';
let statusSocket = new WebSocket(status_url);

// Update friends list and statuses with AJAX
const friendsList = document.querySelector('#friends-list');
const getFriendsStatus = new XMLHttpRequest();
getFriendsStatus.getResponseHeader("Content-type", "application/json");

setInterval(function() {
    getFriendsStatus.open("GET", friends_url, true);
    getFriendsStatus.send();
}, 10000)

getFriendsStatus.onload = function() {
    data = JSON.parse(this.responseText);
    friendsList.innerHTML = '';
    for (var i=0; i < data.length; i++) {
        let friend = Object.entries(data[i]);
        let name = friend[0][0];
        let status = friend[0][1];
        console.log(status);
        let newLi = document.createElement('li');
        let newSpan = document.createElement('span');
        if (status == true) {
            newSpan.classList.toggle('online');
        }
        else {
            newSpan.classList.toggle('offline');
        }
        let newFriend = document.createElement('a');
        newFriend.textContent = name;
        newFriend.href = '#';
        newFriend.classList.toggle('friend');
        newLi.appendChild(newSpan);
        newLi.appendChild(newFriend);
        friendsList.appendChild(newLi);
    }
}
