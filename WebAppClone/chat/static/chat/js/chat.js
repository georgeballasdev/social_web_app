// Variables
const chatWindow = $('#chat-window');
const chats = $('#chats');
const maxChats = 3;
let activeChats = []; // stack of friendnames
let sockets = {} // {'friendname': socket}

// Functions
function handleChatScroll(chat){
    let chatLog = chat.querySelector('.chat-log');
    chatLog.addEventListener('scroll', (e) => {
        if (e.target.scrollTop == 0) {
            $.ajax({
                type: 'POST',
                url: DATASET.nextMessages,
                data:
                {
                    id: chatLog.firstChild.dataset.messageId,
                    csrfmiddlewaretoken: DATASET.token
                },
                success: (response) => {
                    messages = response['messages'];
                    var divClass;
                    for (var i = 0; i < messages.length; i++) {
                        if (messages[i].sender == DATASET.username) {
                            divClass = 'user-msg';
                        }
                        else {
                            divClass = 'friend-msg';
                        }
                        $(chatLog).prepend(
                            '<div data-message-id="' + messages[i].id + '" class="' + divClass + '">\
                            <span class="msg-text">' + messages[i].content + '</span>\
                            <span class="msg-timestamp">' + messages[i].timestamp + '</span>\
                            </div>'
                        );
                    }
                }
            });
            $(e.target).scrollTop(1);
        }
    })
}

function handleSocket(socket, friend) {    
    socket.onopen = () => {
        socket.send(JSON.stringify({
            'command': 'get_messages',
        }));
    };

    socket.onmessage = (e) => {
            let data = JSON.parse(e.data);
            let chat = $('.chat[id=' + friend + '-chat]');
            let chatLog = chat.find('.chat-log');
            if (data['command'] == 'get_messages') {
                let messages = data['messages'];
                for (var i = 0; i < messages.length; i++) {
                    var divClass;
                    if (messages[i].sender == DATASET.username) {
                        divClass = 'user-msg';
                    }
                    else {
                        divClass = 'friend-msg';
                    }
                    chatLog.append(
                        '<div data-message-id="' + messages[i].id + '" class="' + divClass + '">\
                            <span class="msg-text">' + messages[i].content + '</span>\
                            <span class="msg-timestamp">' + messages[i].timestamp + '</span>\
                         </div>'
                    );
                }
            }
            else {
                var divClass;
                if (data.sender == DATASET.username) {
                    divClass = 'user-msg';
                }
                else {
                    divClass = 'friend-msg';
                }
                chatLog.append(
                    '<div data-message-id="' + data.id + '" class="' + divClass + '">\
                        <span class="msg-text">' + data.content + '</span>\
                        <span class="msg-timestamp">' + data.timestamp + '</span>\
                     </div>'
                );
            }
            chatLog.scrollTop(9999);
    };
}

function getChatUrl(friend) {
    return 'ws://' + window.location.host + '/ws/chat/' +
                DATASET.username + '-' + friend + '/';
}

function newChat(friend, picUrl, profileUrl) {
    let newChat = document.createElement('div');
    $(newChat).attr('class', 'chat');
    $(newChat).attr('id', friend + '-chat');
    $(newChat).append(
        '<div class="chat-head">\
            <img src="' + picUrl + '" alt="pic">\
            <a href="' + profileUrl + '">' + friend + '</a>\
            <i class="close-btn hoverable fa-solid fa-xmark"></i></div>\
         <div class="chat-log"></div>\
         <div class="chat-input">\
             <input class="msg-input" type="text">\
         <i class="send-btn hoverable fa-regular fa-paper-plane"></i>\
         </div>'
    );
    return newChat;
}

function openChat(friend, picUrl, profileUrl) {
    // If maxChats, close last chat
    if (activeChats.length == maxChats) {
        closeChat(activeChats[activeChats.length-1]);
    }
    // Open websocket
    let chatSocket = new WebSocket(getChatUrl(friend));
    // Update activeChats and sockets
    activeChats.push(friend);
    sockets[friend] = chatSocket;
    // Get and append chat element
    let chat = newChat(friend, picUrl, profileUrl);
    chats.append(chat);
    $(chat).find('.msg-input').focus();
    // Handle websocket
    handleSocket(chatSocket, friend);
    // Handle loading next messages on scroll
    handleChatScroll(chat);
}

function closeChat(friend) {
    // Close websocket
    sockets[friend].close();
    // Update activeChats and sockets
    let index = activeChats.indexOf(friend);
    activeChats.splice(index, 1);
    delete sockets[friend];
    // Remove chat element
    $('.chat[id=' + friend + '-chat]').remove();
}

// Event listeners
chatWindow.on('click', '.friend',(e) => {
    let friend = e.currentTarget.dataset.friendUsername;
    let picUrl = e.currentTarget.dataset.picUrl;
    let profileUrl = e.currentTarget.dataset.profileUrl;
    if (! activeChats.includes(friend)) {
        openChat(friend, picUrl, profileUrl);
    }
    let newMsgIcon = $(e.currentTarget).find('i');
    console.log(newMsgIcon.css('opacity'));
    newMsgIcon.animate({opacity: '0'}, 300);
})

chatWindow.on('click', '.close-btn',(e) => {
    e.stopImmediatePropagation();
    let friend = $(e.target).prev().text();
    closeChat(friend);
})

chatWindow.on('click', '.send-btn',(e) => {
    e.stopImmediatePropagation();
    let chat = $(e.target).closest('.chat').attr('id');
    let friend = (chat.slice(0, chat.length-5));
    let msgInput = $(e.target).prev();
    let msg = msgInput.val();
    if (msg != '') {
        sockets[friend].send(JSON.stringify({
            'command': 'new_message',
            'sender': DATASET.username,
            'receiver': friend,
            'content': msg,
        }));
        msgInput.val('');
    }
    msgInput.focus();
})

chatWindow.on('keypress', '.msg-input', (e) => {
    // Enter key corresponds to number 13
    if (e.which === 13) {
        $(e.target).next().click();
    }
})

 chatWindow.on('scroll', '.chat-log',(e) => {
    console.log('scrolling chat log');
})

$('#test').on('click', () => {
    let chatLog = $('.chat-log');
    let first = chatLog[0].firstChild;
    let id= $(first).attr('data-message-id');
    $.ajax({
        type: 'POST',
        url: DATASET.nextMessages,
        data:
        {
            id: id,
            csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            messages = response['messages'];
            var divClass;
            for (var i = 0; i < messages.length; i++) {
                if (messages[i].sender == DATASET.username) {
                    divClass = 'user-msg';
                }
                else {
                    divClass = 'friend-msg';
                }
                chatLog.prepend(
                    '<div data-message-id="' + messages[i].id + '" class="' + divClass + '">\
                        <span class="msg-text">' + messages[i].content + '</span>\
                        <span class="msg-timestamp">' + messages[i].timestamp + '</span>\
                     </div>'
                );
            }
        }
    });
})