import myLib, time, socket, sys, os
from threading import Thread

BUFFERSIZE = 1024 * 1024 * 50 # Change this to change buffer size (The highter it is, higher will be the memory usage)

def send():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nomFichier = input("Enter file name: ")
	length = os.path.getsize(nomFichier)
	myLib.log("Size of file: {} KBs".format(int(length / 1024)))
	port = int(input("OPEN PORT: "))

	server.bind(('', port))
	server.listen(1)
	myLib.log("Listening")
	client, infos = server.accept()
	myLib.log("Someone just connected himself: IP: {}, PORT: {}".format(infos[0], infos[1]))

	client.send((str(length) + ',' + nomFichier.split("/")[-1]).encode())
	myLib.log("Sleeping 1s to be sure client is ready")
	time.sleep(1)

	myLib.log("Sending...")
	temps = time.time()
	with open(nomFichier, "rb") as file:
		myLib.log("{} Open on rb".format(nomFichier))
		loadingAndSending = True
		while loadingAndSending:
			fichier = file.read(BUFFERSIZE)
			myLib.log("Length of buffer: {}".format(sys.getsizeof(fichier)))
			client.send(fichier)
			loadingAndSending = not fichier == b""
	temps = time.time() - temps

	myLib.log('Sended in {} seconds'.format(str(temps)[:5]))
	server.close()
	client.close()


def receive(recvBufferSize = BUFFERSIZE, saveBufferSize = 1):

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = input("Enter sender's IP: ")
	port = int(input("Enter sender's open PORT: "))

	client.connect((ip,port))
	myLib.log('Connected')

	recu = client.recv(1024).decode("utf-8") # Sender immediately sends a message when connected
	taille = recu.split(',')[0] #recu contains the length of file and file extension, separated by a comma
	fileName = input("Save as: ")
	taille = int(taille)
	tailleRecu = 0
	fichier = bytes()# Where received data will be stored
	myLib.log("The length of {} is {} bytes".format(fileName,taille))

	with open(fileName, "wb+") as file:
		recv = True
		myLib.log("Receiving...")
		debut = time.time()
		progress = loadThread(fileName, taille, 1)
		progress.start()
		while(recv):
			for i in range(saveBufferSize):
				recu = client.recv(recvBufferSize)
				fichier += recu
				if recu == b'':
					recv = False
					myLib.log("recu is empty, size: {}".format(sys.getsizeof(recu)))
					break
			tailleRecu += sys.getsizeof(fichier)
			file.write(fichier)
			fichier = b""

	duree = time.time()-debut
	progress.kill()
	progress.join()

	myLib.log('{}/{} in {}s'.format(tailleRecu,taille,duree))
	myLib.log("All received !")
	try:
		myLib.log('Average speed: {} MB/s'.format(os.path.getsize(fileName)/1000000/duree))
	except ZeroDivisionError:
		myLib.log('Average speed: Fast AF !')

	myLib.log("Bye !")
	client.close()

class loadThread(Thread):
	def __init__(self, fileName, maxSize, interval = 5):
		Thread.__init__(self)
		self.fileName = fileName
		self.maxSize = maxSize
		self.interval = interval
		self.running = True

	def run(self):
		while self.running:
			print("\r{}b / {}b".format(os.path.getsize(self.fileName), self.maxSize), end="")
			time.sleep(self.interval)

		print("")

	def kill(self):
		print("\n", end = "")
		self.running = False
