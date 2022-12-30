const chat_window = document.querySelector('#chat-window');
const chat1 = document.querySelector('#chat1');
const chat2 = document.querySelector('#chat2');
const chat3 = document.querySelector('#chat3');
const friends = document.querySelectorAll(".friend");
const username = document.querySelector('#username').textContent;
let active_chats = {};
let sockets = {}

// Functions
function handleSocket(url, friend, chat) {
    chat.querySelector('.msg-input').focus();
    let chatSocket = new WebSocket(url);
    active_chats[friend] = chatSocket;
    
    chatSocket.onopen = function(e) {
        console.error('WS opened');
        chatSocket.send(JSON.stringify({
            'command': 'get_messages',
        }));
    };

    chatSocket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            let chat_log = chat.querySelector('.chat-log');
            if (data['command'] == 'get_messages') {
                let messages = data['messages'];
                for (var i = 0; i < messages.length; i++) {
                    chat_log.innerText += (messages[i].sender + ': ' + messages[i].content +  messages[i].timestamp + '\n');
                }
            }
            else {
                console.log('GOT new message');
                chat_log.innerText += (data.sender + ': ' + data.content +  data.timestamp + '\n');
            }
    };

    chatSocket.onclose = function(e) {
        console.error('WS closed');
    };

    chat.querySelector('.msg-input').onkeyup = function(e) {
        if (e.keyCode === 13) {
            chat.querySelector('.send-btn').click();
        }
    };

    chat.querySelector('.send-btn').onclick = function(e) {
        let msg_input = chat.querySelector('.msg-input');
        let msg = msg_input.value;
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'sender': username,
            'receiver': friend,
            'content': msg,
        }));
        msg_input.value = '';
    };
}

function getChatUrl(friend) {
    return 'ws://' + window.location.host + '/ws/chat/' +
                username + '-' + friend + '/';
}

function openChat(chat, friend){
    chat.querySelector('.chat-log').innerText = '';
    chat.querySelector('.msg-input').value = '';
    chat.querySelector('.chat-head span').innerText = friend;
    chat.style.display = 'flex';
    handleSocket(getChatUrl(friend), friend, chat);
}

function moveChat(chat, prev_chat) {
    if (chat.style.display != 'flex') {
        prev_chat.style.display = 'none';
        return;
    }
    prev_chat.innerHTML = chat.innerHTML;
    chat.style.display = 'none';
    prev_chat.style.display = 'flex';
}

function closeChat(chat, friend) {
    if (chat == chat3) {
        chat.style.display = 'none';
    }
    else if (chat == chat2) {
        moveChat(chat3, chat2);
    }
    else {
        moveChat(chat2, chat1);
        moveChat(chat3, chat2);
    }
    active_chats[friend].close();
    delete active_chats[friend];
}

function newChat(friend) {
    if (friend in active_chats) {
        return;
    }
    let chat_count = Object.keys(active_chats).length;
    if (chat_count == 0) {
        openChat(chat1, friend);
    }
    else if (chat_count == 1) {
        openChat(chat2, friend);
    }
    else {
        if (chat_count == 3) {
            closeChat(chat3, friend);
        };
        openChat(chat3, friend);
    }
}

// Event listeners
chat_window.addEventListener('click', function(e) {
    let target = e.target;
    if (target.classList.contains('friend')) {
        newChat(target.innerText);
    }
    else if (target.classList.contains('close-btn')) {
        let friend = target.previousElementSibling.innerText;
        let chat = target.parentElement.parentElement;
        closeChat(chat, friend);
    }
    else if (target.classList.contains('chat-head')) {
        s1 = target.nextElementSibling;
        s2 = s1.nextElementSibling;
        s1.classList.toggle('collapsed');
        s2.classList.toggle('collapsed');
    }
})