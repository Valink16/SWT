import myLib, time, socket, sys, os


def send():
	fichier = b''
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nomFichier = input("Enter file name: ")
	ext = '.' + nomFichier.split(".")[1]
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
	client.send((str(length) + ',' + ext).encode())
	myLib.log("Sleeping for 0.5 second to be sure client is ready")
	time.sleep(1)
	myLib.log("Sending...")
	temps = time.time()
	client.send(fichier)
	temps = time.time() - temps
	myLib.log('Sended in {} seconds'.format(str(temps)[:5]))
	server.close()
	client.close()

def receive():

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = input("Enter sender's IP: ")
	port = int(input("Enter sender's open PORT: "))
	client.connect((ip,port))
	myLib.log('Connected')
	fichier = bytes()# Where received data will be stored
	recu = client.recv(1024).decode("utf-8") # Sender immediately sends a message when connected
	taille,ext = recu.split(',')#recu contains the length of file and file extension, separated by a comma
	taille = int(taille)
	tailleRecu = 0

	myLib.log("The length of {} is {} bytes".format(ext,taille))
	myLib.log("Receiving...")

	debut = time.time()
	recCount = 0
	while(True):
		recu = client.recv(1000000)
		tailleRecu = sys.getsizeof(fichier)
		recCount += 1
		if(recu  == b'stop' or recu  == b''):
			fichier += recu
			break
		fichier += recu
		print('\r{}/{}'.format(tailleRecu,taille),end = '')
	myLib.log('{}/{} in {} tries'.format(tailleRecu,taille,recCount))
	myLib.log("All received !")
	duree = time.time()-debut
	myLib.log('Speed: {} B/s'.format(float(taille)/duree))
	if myLib.ask("Print received file?(may be unreadable): ", "Y", "N"):
		try:
			print(fichier.decode("utf-8"))
		except:
			print(fichier)
	else:
		myLib.log("Not printing")
	
	if myLib.ask("Save received file?: ", "Y", "N"):
		chemin = input("Enter path for saving(#  =  {}): ".format(os.getcwd()))
		if not chemin  == "#":
			os.chdir(chemin)

		with open(input("Enter file name(without extension): ") + ext,"wb") as file:
			file.write(fichier)
		myLib.log("Saving done")
	myLib.log("Bye !")
	client.close()
