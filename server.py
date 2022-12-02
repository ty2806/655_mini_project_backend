import socketserver
import image_classifier
import argparse
from base64 import b64decode
from io import BytesIO
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class MyServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, image_classifier, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
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
        data_uri = self.data.decode()
        print(data_uri)
        
        data_uri += "=="
        image = Image.open(BytesIO(b64decode(data_uri.split(',')[1])))
        image = image.convert('RGB')
        image.save("image.jpg")

        model = self.server.classifier
        result = model.classify('image.jpg')
        print("get result: " + result)
        
        self.wfile.write(result.encode())
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    args = parser.parse_args()
    
    print("start server")
    classifier_model = image_classifier.Classifier()
    print("start image classification model")
    # Create the server, binding to localhost on port 12345
    with MyServer((args.host, int(args.port)), MyTCPHandler, classifier_model) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("start listening")
        server.serve_forever()
