import myLib, time, socket, sys, os


def send():
	fichier = b''
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nomFichier = input("Enter file name: ")

	with open(nomFichier, "rb") as file:
		myLib.log("{} Open on rb".format(nomFichier))
		fichier = file.read()
	port = int(input("OPEN PORT: "))
	server.bind(('', port))
	server.listen(1)
	myLib.log("Listening")
	client, infos = server.accept()
	myLib.log("Someone just connected himself\n{} :{}".format(infos[0], infos[1]))
	myLib.log("Length of opened file :{} bytes".format(sys.getsizeof(fichier)))
	length = sys.getsizeof(fichier)
	client.send((str(length) + ',' + nomFichier).encode())
	myLib.log("Sleeping 1s to be sure client is ready")
	time.sleep(1)
	myLib.log("Sending...")
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

	fileName = input("Save as: ")
	
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
		while(recv):
			for i in range(saveBufferSize):
				recu = client.recv(recvBufferSize)
				if recu == b'':
					fichier += recu
					recv = False
					break

				fichier += recu
				tailleRecu += sys.getsizeof(recu)
				print('\r{}/{}'.format(tailleRecu,taille),end = '')

			file.write(fichier)
			fichier = b""

	duree = time.time()-debut
	myLib.log('{}/{} in {}s'.format(tailleRecu,taille,duree))
	myLib.log("All received !")
	
	myLib.log('Average speed: {} MB/s'.format(os.path.getsize(fileName)/1000000/duree))
	if myLib.ask("Print received file?(may be unreadable): ", "Y", "N"):
		try:
			print(fichier.decode("utf-8"))
		except:
			print(fichier)
	else:
		myLib.log("Not printing")
	

	myLib.log("Bye !")
	client.close()