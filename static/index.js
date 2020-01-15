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
            make_channel(data, socket)
        })
        socket.on('all_rooms', data =>{
            for (room of data){
                make_channel(room, socket)
            }
        })
    })
    
}
const setup = socket =>{
    createGame(socket);
    user_id(socket);
    socket.emit('get rooms');
    console.log('hier12')
}
const createGame = socket =>{
    button = document.querySelector("#createGame")
    button.addEventListener("click", ()=>{
        name = document.querySelector("#createGame_name").value
        document.querySelector("#createGame_name").value = ""
        console.log("Creating game...");
        socket.emit('createGame', {name});
    }) 
}

const user_id = socket =>{
    socket.emit('username')
}

const make_channel = (data, socket) =>{
    rooms = document.querySelector("#room_list")
    room = document.createElement("a")
    room.innerHTML = `<a class="list-item" data-room_id="{${data['game_id']}}">${data['game_name']}</a>`
    rooms.appendChild(room)
}