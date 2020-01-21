document.addEventListener("DOMContentLoaded", ()=>{
    var app = new Vue({
        el: '#BODY',
        data: {
            socket: io.connect(
                location.protocol + "//" + document.domain + ":" + location.port
            ),
            username: '',
            rooms: [],
            game: {},
            picked: true,
            game_name: '',
            errors: [],
            Active_Room: undefined,
        },
        delimiters: ['[[',']]'],
        methods: {
            get_user: function (){
                if (this.username != ''){
                    this.errors = []
                    this.picked = false
                }
                else{
                    this.errors.push('Fill in a valid name')
                }
            },
            make_room: function (){
                if (this.game_name != ''){
                    this.errors = []
                    this.socket.emit('createGame', {'name':this.game_name})
                }
                else{
                   this.errors.push("Fill in a valid name")
                }
            },
            join_room: function (){
                if (this.Active_Room != undefined){
                    this.socket.emit('joinGame', {'name': this.username, 'room_id': this.Active_Room})
                }
                else{
                    this.errors.push("Please pick a room")
                }
            }
        }
    })

    // Connection made, get already made rooms
    app.socket.on("connect", () =>{
        app.socket.emit('get_rooms')
        return true
    })

    // On connection, import rooms from data
    app.socket.on('all_rooms', data =>{
        app.rooms = data
    })

    // Autojoin room after creating one 
    app.socket.on('join_room', data =>{
        room_id = data.room['game_id']
        app.socket.emit('joinGame', {'room_id':room_id, 'name': app.username})
    })

    // Update rooms @ new room
    app.socket.on('new_room', data =>{
        app.rooms.push(data['room'])
    })

    // First Lobby join
    app.socket.on("lobby", data =>{
        app.game = data.game
        document.querySelector('#BODY').innerHTML = data.url
        let name = data.game['game_name']
        document.title = name
    })
    app.socket.on("lobby_update", data =>{
        let id = localStorage.getItem('room')
        app.socket.emit('lobbyupdate', {id})
    })
})

const init = ()=>{   

    
    socket.on("connect", () =>{
        setup(socket);
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

const readyGame = socket =>{
    button = document.querySelector("#Ready")
    if (!button){
        return true
    }
    user = 'Player 1'
    room_id = localStorage.getItem('room')
    button.addEventListener("click", () =>{
        socket.emit("ready", {user, room_id})
    })
}
