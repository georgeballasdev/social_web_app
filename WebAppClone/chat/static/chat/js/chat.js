// Variables
const chat_window = $('#chat-window');
const chats = $('#chats');
const max_chats = 3;
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
                    chatLog.append('<p>' + messages[i].sender + ': ' + 
                        messages[i].content +  messages[i].timestamp + '</p>');
                }
            }
            else {
                chatLog.append('<p>' + data.sender + ': ' + data.content +  data.timestamp + '</p>');
            }
    };

    socket.onclose = () => {
        console.error('WS closed');
    };
}

function getChatUrl(friend) {
    return 'ws://' + window.location.host + '/ws/chat/' +
                DATASET.username + '-' + friend + '/';
}

function newChat(friend) {
    let newChat = document.createElement('div');
    $(newChat).attr('class', 'chat');
    $(newChat).attr('id', friend + '-chat');
    $(newChat).append(('<div class="chat-head"><span>' + friend + '</span><i class="close-btn hoverable fa-solid fa-xmark"></i></div>\
        <div class="chat-log"></div>\
        <div class="chat-input">\
            <input class="msg-input" type="text">\
        <i class="send-btn hoverable fa-regular fa-paper-plane"></i>\
        </div>'));
    return newChat;
}

function openChat(friend) {
    // If max_chats, close last chat
    if (activeChats.length == max_chats) {
        closeChat(activeChats[activeChats.length-1]);
    }
    // Open websocket
    let chatSocket = new WebSocket(getChatUrl(friend));
    // Update activeChats and sockets
    activeChats.push(friend);
    sockets[friend] = chatSocket;
    // Get and append chat element
    let chat = newChat(friend);
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
chat_window.on('click', '.friend',(e) => {
    let friend = e.currentTarget.dataset.friendUsername;
    if (! activeChats.includes(friend)) {
        openChat(friend);
    }
})

chat_window.on('click', '.chat-head',(e) => {
    $(e.target).next().toggle();
    $(e.target).next().next().toggle();
})

chat_window.on('click', '.close-btn',(e) => {
    e.stopImmediatePropagation();
    let friend = $(e.target).prev().text();
    closeChat(friend);
})

chat_window.on('click', '.send-btn',(e) => {
    e.stopImmediatePropagation();
    let chat = $(e.target).closest('.chat').attr('id');
    let friend = (chat.slice(0, chat.length-5));
    let msg_input = $(e.target).prev();
    let msg = msg_input.val();
    sockets[friend].send(JSON.stringify({
        'command': 'new_message',
        'sender': DATASET.username,
        'receiver': friend,
        'content': msg,
    }));
    msg_input.val('');
})