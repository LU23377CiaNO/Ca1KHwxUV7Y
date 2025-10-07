# 代码生成时间: 2025-10-07 20:45:40
import cherrypy
def check_digit_identity(number):
    """
    Validates a number to determine if it has a valid digit identity.
    
    For demonstration purposes, we'll assume a valid digit identity means
    the number ends with an even digit.
    
    :param number: The number to validate.
    :raises ValueError: If the number is not valid.
    """
    try:
        num = int(number)
        if num % 10 % 2 != 0:
            raise ValueError("The number does not end with an even digit.")
    except ValueError:
        raise ValueError("Invalid input: the number must be an integer.")

def expose_check_digit_identity():
    """
    CherryPy exposed function to check digit identity via HTTP GET request.
    
    It expects a query parameter 'number' and returns the result of the check.
    """
    number = cherrypy.request.params.get("number")
    if number is None:
        return "Missing 'number' parameter."
    try:
        result = check_digit_identity(number)
        return f"The number {number} is valid."
    except ValueError as e:
        return f"Error: {e}"
def main():
    """
    Configures and starts the CherryPy server.
    """
    cherrypy.quickstart(
        expose_check_digit_identity,
        config={"global": {"server.socket_host": "0.0.0.0", "server.socket_port": 8080}}
    )
def run_server():
    """
    Starts the server in a separate thread to allow for graceful shutdowns.
    """
    import threading
    server_thread = threading.Thread(target=main)
    server_thread.daemon = True  # allow server to terminate when main thread stops
    server_thread.start()if __name__ == "__main__":
    run_server()