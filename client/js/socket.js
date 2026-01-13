const socket = io()
const room = "pratham_adhya"
const sender = localStorage.getItem("username")

socket.emit("join",{room})

const messages = document.getElementById("messages")
const input = document.getElementById("msg")

fetch(`/messages/${room}`)
.then(r=>r.json())
.then(data=>{
  data.forEach(m=>{
    addMsg(m.message, m.sender)
  })
})

input.addEventListener("keydown",e=>{
  if(e.key==="Enter" && input.value){
    socket.emit("send_message",{
      room,
      sender,
      message:input.value
    })
    input.value=""
  }
})

socket.on("receive_message",data=>{
  addMsg(data.message, data.sender)
})

function addMsg(msg, senderName){
  const d=document.createElement("div")
  d.className = senderName===sender ? "right" : "left"
  d.innerText = msg
  messages.appendChild(d)
}
