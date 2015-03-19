`import socket

def slaveOpenIosGateway (deviceid):
   print "  ---- entered function slaveOpenIosGateway with arg of " + deviceid
   bashCommand = "open -a iOSGateway --args -InitialDevice " + deviceid + " -InitialApp JeppFD-Pro"   
   runBashCommand (bashCommand)
   print "  **** exiting function slaveOpenIosGateway"   
   
def runBashCommand (command):
  print "  ---- entered function runBashCommand with input of " + command
  import subprocess
  process = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print "  just sent command : " + command
  rc = process.returncode
  return rc
  print "  **** exiting function runBashCommand"
   

def findCommandParamInsideBrackets (indata):
  print "  ----- entered function findCommandParamInsideBrackets with input of " + indata
  startBrkt = '<'
  endBrkt = '>'
  startIndex = indata.find(startBrkt)
  endIndex = indata.find(endBrkt)
  print "  start was at ",startIndex
  print "  end was at ", endIndex
  temp = indata
  param = indata[(startIndex+1):(endIndex)]
  print "  found parameter to be " , param
  print "  **** exiting function findCommandParamInsideBrackets"
  return param
  
def slaveDoResign ():
  print "  ---- entered function slaveDoResign, no parameters"
  cmd = "/Users/eggBox/Desktop/LatestIPA/Resign.sh"
  exitcode = runBashCommand (cmd)
  print "  **** exiting function slaveDoResign"
  return exitcode

def slaveDoDeploy (deviceid):
  print "  ---- entered function slaveDoDeploy with arg of " + deviceid
  cmd = "/Users/eggBox/Documents/iPadDeploy.sh"
  runBashCommand (cmd)
  print "  **** exiting function slaveDoDeploy with return code of "
  


TCP_IP = '10.1.119.176'
TCP_PORT = 13000
BUFFER_SIZE = 200  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    
    if "COMM STATUS" in data:
      response = "  S2M:COMM OK ^^"
      conn.send(response) 
      
    if "OPEN IOSGATEWAY" in data:
      deviceid = findCommandParamInsideBrackets (data) 
      slaveOpenIosGateway (deviceid) 
      response = "  S2M:OPEN IOSGATEWAY OK ^^"
      conn.send (response)  
      
    if "RESIGN" in data:
      retcode = slaveDoResign ()
      if retcode == 0:
        response = "  S2M:RESIGN OK ^^"
      else:
        response = "  S2M:RESIGN FAILED ^^"
      conn.send(response)

    if "DEPLOY" in data:
       deviceid = findCommandParamInsideBrackets (data)
       slaveDoDeploy (deviceid)
       response = " S2M:DEPLOY OK  ^^"
       conn.send(response)

conn.close()