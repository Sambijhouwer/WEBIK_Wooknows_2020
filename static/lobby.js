document.addEventListener("DOMContentLoaded", ()=>{
    var app = new Vue({
        el: '#BODY',
        data: {
            socket: io.connect(
                location.protocol + "//" + document.domain + ":" + location.port
            ),
            username: localStorage.getItem("username"),
            game: {},
        },
    })
})