from flask_socketio import emit, join_room
from database import get_db

def register_events(socketio):

    @socketio.on("join")
    def on_join(data):
        join_room(data["room"])

    @socketio.on("send_message")
    def on_message(data):
        db = get_db()
        db.execute(
            "INSERT INTO messages(room,sender,message) VALUES (?,?,?)",
            (data["room"], data["sender"], data["message"])
        )
        db.commit()

        emit("receive_message", data, room=data["room"])
