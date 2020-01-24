from flask import Flask, render_template, Response
from iBlink_Webcam import Webcam
from iBlink_DetectEyes import DetectEyes
import time
import pdb


app = Flask(__name__)     
Eyes = DetectEyes()

@app.route('/')
def index():
    """Video"""
    return render_template('index.html')


def gen(webcam):
    while True:
        frame = webcam.get_frame()
        png, L = Eyes.calculate(frame)
        streambyte()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + png.tobytes() + b'\r\n')




@app.route('/camVideo')
def camVideo():
    return Response(gen(Webcam()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/code')
def streambyte():
    L = Eyes.codeArr

    #Shortcut
    final = Eyes.final
    if final.__contains__("om"):
        final = final.replace("om","_On_My_Way_")
        print("replaced")
        #pdb.set_trace()
    Eyes.final = final
    b = (''.join(L)).encode('utf-8')
    c = (final).encode('utf-8')
    #.................................................................

    final = Eyes.final
   

    b = (''.join(L)).encode('utf-8')
    c = (final).encode('utf-8')
    
    
    def events():
        yield "data: %s %s\n\n" % (b,c)
        time.sleep(1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
