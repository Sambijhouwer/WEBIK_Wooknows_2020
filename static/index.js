document.addEventListener("DOMContentLoaded", ()=>{
    init();
})

const init = ()=>{
    let socket = io();
    socket.on('connect', ()=>{
        username = 'Sam'
        socket.emit('username', { username });
    })
}