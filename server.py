import socketserver
import image_classifier
import urllib

class MyServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, image_classifier, bind_and_activate=True):
        super.__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.classifier = image_classifier


class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        response = urllib.request.urlopen(self.data)
        with open('image.jpg', 'wb') as f:
            f.write(response.file.read())

        model = self.server.classifier
        result = model.classify('image.jpg')

        self.wfile.write(result)

if __name__ == "__main__":
    HOST, PORT = "localhost", 12345

    classifier_model = image_classifier.Classifier()
    # Create the server, binding to localhost on port 12345
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler, classifier_model) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()