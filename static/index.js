document.addEventListener("DOMContentLoaded", ()=>{
    init();
})

const init = ()=>{   
    let socket = io.connect(
        location.protocol + "//" + document.domain + ":" + location.port
      );
    socket.on("connect", () =>{
        setup(socket);

        socket.on('join_room', data =>{
            room_id = data.room['game_id']
            socket.emit('joinGame', {room_id})
        })
        socket.on('new_room', data =>{
            make_channel(data.room, socket)
        })
    })
    
}
const setup = socket =>{
    createGame(socket);
    user_id(socket);
}
const createGame = socket =>{
    button = document.querySelector("#createGame")
    button.addEventListener("click", ()=>{
        console.log("Creating game...");
        let name = 'Kamer 1'
        socket.emit('createGame', {name});
    }) 
}

const user_id = socket =>{
    socket.emit('username')
}

const make_channel = (channel, socket) =>{
    console.log("In de maak..." + channel)
}