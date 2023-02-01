// Handle notifications
const notifications = $('#notifications');
const notificationsCount = $('#notifications-count');
const notificationsList = $('#notifications-list');
const notificationsUrl = 'ws://' + window.location.host + '/ws/notifications/';
let notificationsSocket = new WebSocket(notificationsUrl);

notificationsSocket.onopen = () => {
  $.ajax({
    type: 'GET',
    url: DATASET.notificationsUrl,
    data:
    {
        username: DATASET.username,
    },
    success: (response) => {
        notificationsCount.text(response['count']);
        let n = response['list'];
        let list = notificationsList.find('ul');
        for (var i = 0; i < n.length; i++) {
          list.append(
            '<li><a href="'+ n[i][0] +'">'+
            n[i][1] + ' - ' + n[i][2] +'</a></li>'
          );
        }
    }
  });
}

notificationsSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    let list = notificationsList.find('ul');
    list.append('<li><a href="'+ data.link +'">'+ data.text +'</a></li>');
}

notifications.click( () => {
  notificationsList.toggle();
})

// Handle profile menu
const profile = $('#profile');
const profileCaret = profile.find('i');
const profileMenu = $('#profile-menu');

profile.click( () => {
    profileCaret.toggleClass('fa-caret-up');
    profileCaret.toggleClass('fa-caret-down');
    profileMenu.toggle();
})