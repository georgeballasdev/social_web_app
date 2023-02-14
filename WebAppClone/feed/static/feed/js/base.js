// Handle loading icon
$(document).ready( () => {
    $('#loading').animate({opacity: '0'}, 100, () => {
        $('#loading').hide();
    });
})


// Handle notifications
const notifications = $('#notifications');
const notificationsCount = $('#notifications-count');
const notificationsDropdown = $('#notifications-list');
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
        notificationsCount.text(response.count);
        let data = response.list;
        let list = notificationsDropdown.find('ul');
        for (var i = 0; i < data.length; i++) {
            list.append(
                '<li data-notification-id="' + data[i].id + '">\
                    <a href="' + data[i].link + '">' + data[i].text +
                    '<span> - ' + data[i].timestamp + '</span></a>\
                </li>'
            );
        }
    }
  });
}

notificationsSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    // New chat notification
    if (data.user){
        console.log('You have a new message from ' + data.user);
    }
    // New notification
    else {
        notificationsCount.text(data.count);
        notificationsCount.animate({fontSize: '2.25rem'}, 'fast', 'swing', () => {
            notificationsCount.animate({fontSize: '2rem'}, 'fast', 'swing');
        });
        if (data.notification) {
            let notification = data.notification;
            let list = notificationsDropdown.find('ul');
            list.prepend(
                '<li data-notification-id="' + notification.id + '">\
                <a href="' + notification.link + '">' + notification.text +
                '<span> - ' + notification.timestamp + '</span></a>\
                </li>'
                );
                // Remove oldest notification from dropdown
                if (notificationsDropdown.find('li').length > 5) {
                    list.find('li').last().remove();
                }
        }
    }
}

notifications.on('mouseenter', () => {
    // If visible, mark dropdown notifications as seen
    if(notificationsDropdown.is(':visible')){
        let markSeen = [];
        let notifications = notificationsDropdown.find('li');
        for (var i = 0; i < notifications.length; i++) {
            markSeen.push(notifications[i].dataset.notificationId);
        }
        notificationsSocket.send(JSON.stringify({
            'seen': markSeen
        }));
    }
})

// Handle search
const searchBar = $('#search-bar');
const searchInput = searchBar.find('input');
const searchList = $('#search-list');
const searchUsers = $('#search-users');
const searchGroups = $('#search-groups');

searchInput.on('focus', () => {
    if (searchUsers.find('li').length + searchGroups.find('li').length > 0){
        searchList.css({opacity: '1', top: '120%', pointerEvents: 'auto'});
    }
})

searchInput.on('blur', () => {
    searchList.css({opacity: '0', top: '100%'});
})

searchInput.on('input', () => {
    searchList.css({opacity: '1', top: '120%', pointerEvents: 'auto'});
    let query = searchInput.val();
    let isValidQuery = /^[a-zA-Z0-9!? ]+$/.test(query);
    if (isValidQuery) {
        $.ajax({
            type: 'GET',
            url: DATASET.searchUrl,
            data:
            {
                query: query,
            },
            success: (response) => {
                searchUsers.empty();
                searchGroups.empty();
                response.users.forEach(user => {
                    searchUsers.append(
                        '<li><a href="' + user.link + '">' +
                        '<img alt="pic" src="' + user.pic + '">' +
                        user.username + '</a></li>'
                    );
                })
                response.groups.forEach(group => {
                    searchGroups.append(
                        '<li><a href="' + group.link + '"> Group: ' + group.title + '</a></li>'
                    );
                })
            }
        })
    }
})