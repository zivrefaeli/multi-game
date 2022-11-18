from .create import CreateServerUI
from .ui import ServerUI

def smain() -> None:
    create_server_ui = CreateServerUI()
    create_server_ui.mainloop()

    if create_server_ui.address:
        server_ui = ServerUI(create_server_ui.address)
        server_ui.mainloop()