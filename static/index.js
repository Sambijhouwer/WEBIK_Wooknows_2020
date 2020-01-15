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
        socket.on("lobby", data =>{
            window.location = data.url;
        })
    })
    
}
const setup = socket =>{
    createGame(socket);
    user_id(socket);
    joinGame(socket);
    socket.emit('get rooms');
}
const createGame = socket =>{
    button = document.querySelector("#createGame")
    button.addEventListener("click", ()=>{
        name = document.querySelector("#createGame_name").value
        if (name == ""){
            return false
        }
        document.querySelector("#createGame_name").value = ""
        console.log("Creating game...");
        socket.emit('createGame', {name});
    }) 
}

const user_id = socket =>{
    socket.emit('username')
}

const joinGame = socket =>{
    button = document.querySelector("#joinGame")
    button.addEventListener('click', ()=>{
        let room_id = localStorage.getItem("room")
        if (!room_id){
            return
        }
        socket.emit("joinGame", {room_id} )
    })
}

const room_togle = (room) =>{
    document.querySelectorAll("#room_list > a").forEach(e =>{
        if (e.innerHTML == room){
            e.classList.add('is-active');
        } else{
            e.classList.remove("is-active")
        }
    })
} 

const make_channel = (data, socket) =>{
    rooms = document.querySelector("#room_list")
    room = document.createElement("a")
    room.classList.add('list-item', 'room_button')
    room.setAttribute('data-room_id', data['game_id'])
    room.innerHTML = data['game_name']
    rooms.appendChild(room)
    room.addEventListener('click', ()=>{
        localStorage.setItem("room", data['game_id'])
        room_togle(data['game_name'])
    })
}