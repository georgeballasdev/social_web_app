// Variables
const chatWindow = $('#chat-window');
const chats = $('#chats');
const maxChats = 3;
let activeChats = []; // stack of friendnames
let sockets = {} // {'friendname': socket}

// Functions
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
                        '<div class="' + divClass + '">\
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
                    '<div class="' + divClass + '">\
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

function newChat(friend, picUrl) {
    let newChat = document.createElement('div');
    $(newChat).attr('class', 'chat');
    $(newChat).attr('id', friend + '-chat');
    $(newChat).append(
        '<div class="chat-head">\
            <img src="' + picUrl + '" alt="pic">\
            <span>' + friend + '</span>\
            <i class="close-btn hoverable fa-solid fa-xmark"></i></div>\
         <div class="chat-log"></div>\
         <div class="chat-input">\
             <input class="msg-input" type="text">\
         <i class="send-btn hoverable fa-regular fa-paper-plane"></i>\
         </div>'
    );
    return newChat;
}

function openChat(friend, picUrl) {
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
    let chat = newChat(friend, picUrl);
    chats.append(chat);
    $(chat).find('.msg-input').focus();
    // Handle websocket
    handleSocket(chatSocket, friend);
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
    if (! activeChats.includes(friend)) {
        openChat(friend, picUrl);
    }
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