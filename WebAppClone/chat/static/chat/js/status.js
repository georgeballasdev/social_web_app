// Handle user online status
const statusUrl = 'ws://' + window.location.host + '/ws/status/';
const statusSocket = new WebSocket(statusUrl);

statusSocket.onmessage = (e) => {
    console.log('got status notification:')
    console.log(e.data);
    data = JSON.parse(e.data);
    let user = data['user'];
    let status = data['status'];
    console.log(status);
    if (status == true) {
        console.log('true');
        $('#'+user).find('span').addClass('online');
    }
    else {
        $('#'+user).find('span').removeClass('online');
    }
}
// CHECK IF JS IS THE PROBLEM, LOOK AT CONSOLE

// getFriendsStatus.onload = function() {
//     data = JSON.parse(this.responseText);
//     console.log(data);
//     friendsList.innerHTML = '';
//     for (var i=0; i < data.length; i++) {
//         let friend = Object.entries(data[i]);
//         let name = friend[0][0];
//         let status = friend[0][1];
//         console.log(status);
//         let newLi = document.createElement('li');
//         let newSpan = document.createElement('span');
//         if (status == true) {
//             newSpan.classList.toggle('online');
//         }
//         else {
//             newSpan.classList.toggle('offline');
//         }
//         let newFriend = document.createElement('a');
//         newFriend.textContent = name;
//         newFriend.href = '#';
//         newFriend.classList.toggle('friend');
//         newLi.appendChild(newSpan);
//         newLi.appendChild(newFriend);
//         friendsList.appendChild(newLi);
//     }
// }
