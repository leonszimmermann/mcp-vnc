import os
from tempfile import NamedTemporaryFile
from io import BytesIO

from vncdotool import api
import PIL
import mcp.server.fastmcp as fastmcp
import time

INSTRUCTIONS = """
This MCP server connects to a VNC server using the vncdotool library.
It provides tools for interacting with the VNC server, such as:
- Taking screenshots
- Clicking and dragging the mouse
- Typing text
- Pressing keyboard shortcuts
- Waiting for a period of time
- Dragging the mouse from one coordinate to another

Make sure to set the VNC_HOST and VNC_PASS environment variables to the correct values.
"""


mcp = fastmcp.FastMCP(name="VNC Computer Controller", instructions=INSTRUCTIONS)


WIDTH, HEIGHT = 1024, 768
REMOTE_WIDTH, REMOTE_HEIGHT = 1024, 768

        
def connect_vnc():
    # raises if environment variables are not set
    return api.connect(server=os.environ["VNC_HOST"], password=os.environ["VNC_PASS"])


@mcp.tool()
def screenshot() -> fastmcp.Image:
    """Take a screenshot of the current screen and return it as an image"""

    # vncdotool needs a filename, so use a temp file, but avoid a second open()
    with connect_vnc() as vnc, NamedTemporaryFile(suffix=".png") as tmp:
        vnc.captureScreen(tmp)
        img = PIL.Image.open(tmp)
        img = img.resize((WIDTH, HEIGHT), PIL.Image.LANCZOS)

        with BytesIO() as buf: # build the image in memory
            img.save(buf, format="JPEG")
            return fastmcp.Image(data=buf.getvalue())
        


@mcp.tool()
def left_mouse_click(x: int, y: int, repeat: int = 1) -> None:
    """Left mouse click at the given [x],[y] coordinates (for [repeat] times, e.g. 2 for double click)"""
    with connect_vnc() as vnc:
        remote_x = int(round(x * REMOTE_WIDTH / WIDTH))
        remote_y = int(round(y * REMOTE_HEIGHT / HEIGHT))
        vnc.mouseMove(remote_x, remote_y)
        for i in range(repeat):
            # explicitly press and release to improve compatibility with some servers
            vnc.mouseDown(button=1)
            vnc.pause(0.05)
            vnc.mouseUp(button=1)
            vnc.pause(0.05)


@mcp.tool()
def right_mouse_click(x: int, y: int, repeat: int = 1) -> None:
    """Right mouse click at the given [x],[y] coordinates (for [repeat] times, e.g. 2 for double click)"""
    with connect_vnc() as vnc:
        remote_x = int(round(x * REMOTE_WIDTH / WIDTH))
        remote_y = int(round(y * REMOTE_HEIGHT / HEIGHT))
        vnc.mouseMove(remote_x, remote_y)
        for i in range(repeat):
            vnc.mouseDown(button=3)
            vnc.pause(0.05)
            vnc.mouseUp(button=3)
            vnc.pause(0.05)

@mcp.tool()
def type_text(text: str) -> None:
    """Enter the given text on the keyboard"""
    with connect_vnc() as vnc:
        for key in text:
            vnc.keyPress(('shift-' if key.isupper() else '') + key.lower())
            vnc.pause(0.05)


@mcp.tool()
def keyboard_shortcut(keys: list[str]) -> None:
    """Press the given keys simultaneously; e.g. ["shift", "e"] or ["enter"]. Use the keymap resource to see the valid key names."""
    with connect_vnc() as vnc:
        vnc.keyPress('-'.join([key.lower() for key in keys]))
        vnc.pause(0.05)


@mcp.tool()
def sleep(seconds: float) -> None:
    """Sleep (time.sleep) for the given number of seconds. Use this when you need to wait to be able to continue a task."""
    time.sleep(seconds)

@mcp.tool()
def mouse_drag(x_start: int, y_start: int, x_end: int, y_end: int) -> None:
    """Drag the mouse from the given [x_start],[y_start] coordinates to the given [x_end],[y_end] coordinates. Does NOT work like a touchscreen drag."""
    with connect_vnc() as vnc:
        remote_x_start = int(round(x_start * REMOTE_WIDTH / WIDTH))
        remote_y_start = int(round(y_start * REMOTE_HEIGHT / HEIGHT))

        remote_x_end = int(round(x_end * REMOTE_WIDTH / WIDTH))
        remote_y_end = int(round(y_end * REMOTE_HEIGHT / HEIGHT))

        vnc.mouseMove(remote_x_start, remote_y_start)
        vnc.pause(0.05)
        vnc.mouseDown(1)
        vnc.pause(0.05)
        vnc.mouseMove(remote_x_end, remote_y_end)
        vnc.pause(0.05)
        vnc.mouseUp(1)
        vnc.pause(0.05)


@mcp.resource("resource://keymap")
def get_keymap() -> list[str]:
    """ Provides valid key names for e.g. keyboard shortcuts"""
    return [
        "bsp", "tab", "return", "enter", "esc", "ins", "delete", "del", "home", "end",
        "pgup", "pgdn", "left", "up", "right", "down", "slash", "bslash", "fslash",
        "spacebar", "space", "sb", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
        "f9", "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20",
        "lshift", "shift", "rshift", "lctrl", "ctrl", "rctrl", "lmeta", "meta", "rmeta",
        "lalt", "alt", "ralt", "scrlk", "sysrq", "numlk", "caplk", "pause", "lsuper",
        "super", "rsuper", "lhyper", "hyper", "rhyper", "kp0", "kp1", "kp2", "kp3",
        "kp4", "kp5", "kp6", "kp7", "kp8", "kp9", "kpenter"
    ]

        
if __name__ == "__main__":
    mcp.run()
