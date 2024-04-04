import os
import socket
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog

# Function to start the HTTP server in a separate thread
def start_server(directory, status_label, start_button, stop_button, ip_label, port_label):
    global server_thread

    if not directory:
        status_label.config(text="No directory selected.")
        return

    try:
        # Start HTTP server in a separate thread
        server_thread = threading.Thread(target=run_server, args=(directory, status_label, start_button, stop_button, ip_label, port_label))
        server_thread.daemon = True
        server_thread.start()
    except Exception as e:
        print("Error starting server:", e)
        status_label.config(text="Error starting server")

# Function to run the HTTP server
def run_server(directory, status_label, start_button, stop_button, ip_label, port_label):
    global server, ip_address, port

    try:
        # Start HTTP server without displaying a console window
        server = subprocess.Popen(['python', '-m', 'http.server', '8000'], cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"Server started serving {directory}")
        status_label.config(text="Server running...")
        start_button.config(state="disabled")
        stop_button.config(state="normal")

        # Get server IP address
        ip_address = socket.gethostbyname(socket.gethostname())
        ip_label.config(text=f"Server IP: {ip_address}")

        # Set server port
        port = 8000
        port_label.config(text=f"Server Port: {port}")

    except Exception as e:
        print("Error starting server:", e)
        status_label.config(text="Error starting server")

# Function to stop the HTTP server
def stop_server(status_label, start_button, stop_button):
    global server
    if server:
        print("Stopping server...")
        server.terminate()
        server.wait()
        status_label.config(text="Server stopped.")
        start_button.config(state="normal")
        stop_button.config(state="disabled")

# Function to select directory
def select_directory(directory_label):
    directory = filedialog.askdirectory(title="Select Directory to Share")
    directory_label.config(text=directory)

# Main function to create the GUI
def main():
    root = tk.Tk()
    root.title("Python HTTP Server")

    # Directory selection
    directory_frame = tk.Frame(root)
    directory_frame.pack(pady=10)
    directory_label = tk.Label(directory_frame, text="")
    directory_label.pack(side=tk.LEFT, padx=5)
    select_button = tk.Button(directory_frame, text="Select Directory", command=lambda: select_directory(directory_label))
    select_button.pack(side=tk.LEFT, padx=5)

    # Server control buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)
    start_button = tk.Button(control_frame, text="Start Server", command=lambda: start_server(directory_label.cget("text"), status_label, start_button, stop_button, ip_label, port_label))
    start_button.pack(side=tk.LEFT, padx=5)
    stop_button = tk.Button(control_frame, text="Stop Server", command=lambda: stop_server(status_label, start_button, stop_button), state="disabled")
    stop_button.pack(side=tk.LEFT, padx=5)

    # Server status
    status_label = tk.Label(root, text="Server not running", pady=10)
    status_label.pack()

    # Server IP address
    ip_label = tk.Label(root, text="", pady=5)
    ip_label.pack()

    # Server port
    port_label = tk.Label(root, text="", pady=5)
    port_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
