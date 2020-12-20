def checkBase(userid):
	uid = str(userid)
	opener = open("base.txt","r").read().split("\n")
	if uid in opener:
		return True
	else:
		return False

def newUser(userid,time_now,log,admin):
	try:
		uid = str(userid)
		opener = open("base.txt","a")
		opener.write("\n"+uid)
		opener.close()
		opener = open("profiles/"+uid+".txt","w")
		opener.write(str(time_now))
		if log == "y" or log == "Y":
			print("|Добавлен новый айди: "+uid)
	except Exception as E:
		bot.send_message(admin,"*Капитан! Произошел пиздец! Вам необходимо связаться с кодером.\n\nОшибка:*\n"+str(E))
		


