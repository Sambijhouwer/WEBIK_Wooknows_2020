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
            make_channel(data)
        })
        socket.on('all_rooms', data =>{
            for (room of data){
                make_channel(room)
            }
        })
        socket.on("lobby", data =>{
            document.open();
            document.write(data.url);
            document.close();
        })
        socket.on("lobby_update", data =>{
            let id = data['game_id']
            socket.emit('lobbyupdate', {id})
        })
        socket.on("error", data =>{
            return
        })
    })
    
}
const setup = socket =>{
    createGame(socket);
    joinGame(socket);
    username(socket);
    socket.emit('get rooms');
}
const createGame = socket =>{
    button = document.querySelector("#createGame")
    if (!button){
        return true
    }
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

const username = socket =>{
    let username = localStorage.getItem('username')
    if (username){
        socket.emit('username', {username})
        return true
    }
    let button = document.querySelector("#userbutton")
    if (!button){
        return true
    }
    button.addEventListener("click", ()=>{
        username = document.querySelector("#usertext").value.trim()
        if (username != ""){
            localStorage.setItem("username", username)
            socket.emit('username', {username})
        }
    })    
}

const joinGame = socket =>{
    button = document.querySelector("#joinGame")
    if (!button){
        return true
    }
    button.addEventListener('click', ()=>{
        let room_id = localStorage.getItem("room")
        if (!room_id){
            return
        }
        socket.emit("joinGame", {room_id} )
    })
}

const room_toggle = (room) =>{
    document.querySelectorAll("#room_list > a").forEach(e =>{
        if (e.innerHTML == room){
            e.classList.add('is-active');
        } else{
            e.classList.remove("is-active")
        }
    })
} 

const make_channel = (data) =>{
    rooms = document.querySelector("#room_list")
    if (!rooms){
        return true
    }
    room = document.createElement("a")
    room.classList.add('list-item', 'room_button')
    room.setAttribute('data-room_id', data['game_id'])
    room.innerHTML = data['game_name']
    rooms.appendChild(room)
    room.addEventListener('click', ()=>{
        localStorage.setItem("room", data['game_id'])
        room_toggle(data['game_name'])
    })
}