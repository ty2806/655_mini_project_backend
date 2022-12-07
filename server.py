import socketserver
import image_classifier
import argparse
from base64 import b64decode
from io import BytesIO
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# a custom socketserver.TCPServer with a image classfication model as an attribute
class MyServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, image_classifier, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.classifier = image_classifier

# a custom TCP Handler
class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # use readline to delimit packets
        self.data = self.rfile.readline().strip()
        # receive a image's data uri and print it
        print("{} wrote:".format(self.client_address[0]))
        data_uri = self.data.decode()
        print(data_uri)
        
        # parse data uri to jpg image and write it to local file
        data_uri += "=="
        image = Image.open(BytesIO(b64decode(data_uri.split(',')[1])))
        image = image.convert('RGB')
        image.save("image.jpg")

        # load image to classification model and get result
        model = self.server.classifier
        result = model.classify('image.jpg')
        print("get result: " + result)
        
        # send result to socket client
        self.wfile.write(result.encode())
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    args = parser.parse_args()
    
    print("start server")
    # load image classification model
    classifier_model = image_classifier.Classifier()
    print("start image classification model")
    # Create the server, binding to args.host on port args.port
    with MyServer((args.host, int(args.port)), MyTCPHandler, classifier_model) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("start listening")
        server.serve_forever()
