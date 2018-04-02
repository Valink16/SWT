import myLib, time, socket, sys, os
from threading import Thread

MB100 = 1024 * 1024 * 100

def send():
	fichier = b''
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nomFichier = input("Enter file name: ")
	with open(nomFichier, "rb") as file:
		fichier = file.read()
	port = int(input("OPEN PORT: "))
	server.bind(('', port))
	server.listen(1)
	myLib.log("Listening")
	client, infos = server.accept()
	myLib.log("Someone just connected himself: IP: {}, PORT: {}".format(infos[0], infos[1]))
	length = os.path.getsize(nomFichier)


	client.send((str(length) + ',' + nomFichier).encode())
	myLib.log("Sleeping 1s to be sure client is ready")
	time.sleep(1)

	myLib.log("Sending...")
	myLib.log("{} Open on rb".format(nomFichier))
	temps = time.time()
	client.send(fichier)
	temps = time.time() - temps

	myLib.log('Sended in {} seconds'.format(str(temps)[:5]))
	server.close()
	client.close()

def receive(recvBufferSize = 1000000, saveBufferSize = 150):

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = input("Enter sender's IP: ")
	port = int(input("Enter sender's open PORT: "))

	client.connect((ip,port))
	myLib.log('Connected')

	recu = client.recv(1024).decode("utf-8") # Sender immediately sends a message when connected
	taille, fileName = recu.split(',')#recu contains the length of file and file extension, separated by a comma
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
					break

			tailleRecu += sys.getsizeof(fichier)
			file.write(fichier)
			fichier = b""

	duree = time.time()-debut
	progress.kill()
	progress.join()

	myLib.log('{}/{} in {}s'.format(tailleRecu,taille,duree))
	myLib.log("All received !")

	myLib.log('Average speed: {} MB/s'.format(os.path.getsize(fileName)/1000000/duree))

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
		self.running = False
