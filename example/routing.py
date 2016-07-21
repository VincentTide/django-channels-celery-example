from channels import route
from jobs import consumers

channel_routing = [
    # Wire up websocket channels to our consumers:
    route("websocket.receive", consumers.ws_receive),
]