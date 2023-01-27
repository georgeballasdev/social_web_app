var mouseX;
var mouseY;
const profilePopUp = $('#profile-popup');

const profile = $('#profile');
const profileMenu = profile.find('#profile-menu');
const profileCaret = profile.find('i');

const notifications = $('#notifications');
const notificationsCount = notifications.find('#notifications-count');
const notificationsList = notifications.find('#notifications-list');

// Handle notifications
notificationsUrl = 'ws://' + window.location.host + '/ws/notifications/';
let notificationsSocket = new WebSocket(notificationsUrl);

notificationsSocket.onopen = (e) => {
  $.ajax({
    type: 'GET',
    url: notifications_url,
    data:
    {
        username: username,
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
    console.log('new notify ' + data);
    let list = notificationsList.find('ul');
    list.append('<li><a href="'+ data.link +'">'+ data.text +'</a></li>');
}

// Events
$(document).mousemove( (e) => {
   mouseX = e.pageX; 
   mouseY = e.pageY;
});  

$(".pop-up").mouseenter( () => {
  profilePopUp.css({'top':mouseY-10,'left':mouseX-10});
  profilePopUp.toggle();
});

profilePopUp.mouseout( () => {
    profilePopUp.toggle();
});

profile.click( () => {
    profileCaret.toggleClass('fa-caret-up');
    profileCaret.toggleClass('fa-caret-down');
    profileMenu.toggleClass('hidden');
})

notifications.click( () => {
  console.log('notd');
  notificationsList.toggleClass('hidden');
})