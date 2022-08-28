#from mobilenet import mobilenet_v2

#from pickle import TRUE
#from mobbilenet2.mobilenet import is_available
from mobilenet import mobilenet_v2

from mobilenet import is_available


global model

def handle(req):
    #model = mobilenet_v2(pretrained=True)
    '''
    model = mobilenet_v2(pretrained=True)
    input_size=(1, 3, 224, 224)
    x = torch.randn(input_size)
    out = model(x)
    response = flask.jsonify({"message": "success"})
    response.status_code = 200
    '''
    if is_available():
        #response = flask.jsonify({"message": "success"})
        #response.status_code = 200
        return "true"
    else:
        return "false"
    
    #return response

