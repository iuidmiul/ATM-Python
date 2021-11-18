import cocos
from cocos.actions import *
import pyglet
from pyglet.window import key

ActiveCard = 0
BalanceCard1 = 1000
BalanceCard2 = 1500

#Pin Inteface
class PinInterface(cocos.layer.Layer):
	is_event_handler = True

	#Create All Objects
	def __init__(self):
		super(PinInterface,self).__init__()
		self.PinTries = 3
		self.PinHidden = ''
		self.PinPasswordNumbers = []

		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)

		#Retragere Sold BG
		RetragereBG = cocos.sprite.Sprite('Files/CodPinBG.png')
		RetragereBG.position = (525,110)
		RetragereBG.scale_y = 0.5
		self.add(RetragereBG)

		#Introducere Pin Text
		IntrodPin = cocos.text.Label('Introduceti Pin',(460,150),color = (255,255,255,255))
		IntrodPin.scale = 1.2
		self.add(IntrodPin)

		#Cod Pin Text
		self.PinPassword = cocos.text.Label(self.PinHidden,(505,100),color = (0,0,0,255))
		self.PinPassword.scale = 1.2
		self.add(self.PinPassword)

		#Incercari Ramase Text
		self.IncercRamase = cocos.text.Label('Incercari Ramase: ' + str(self.PinTries),(750,105),color = (255,255,255,255))
		self.IncercRamase.scale = 1.2
		self.add(self.IncercRamase)

		#Pin Gresit Text
		self.PinGresit = cocos.text.Label("Pin Gresit",(489,204),color = (0,0,0,255))
		self.PinGresit.opacity = 0
		self.add(self.PinGresit)

		#Card Blocat Text
		self.CardBlocat = cocos.text.Label("Card Blocat",(480,60),color = (255,255,255,255))
		self.CardBlocat.opacity = 0
		self.add(self.CardBlocat)

	#Pin Gresti Text Anim/Update Tries Text
	def PinGresitText(self):
		#Update
		self.PinTries -= 1
		if self.PinTries < 0:
			self.PinTries = 0
		self.IncercRamase.element.text = 'Incercari Ramase: ' + str(self.PinTries)
		#Anim
		PinGresitOptim = 0
		#Appear Anim
		self.PinGresit.opacity = 255
		self.PinGresit.do(Blink(1,2))
		#Disappear Anim
		if PinGresitOptim == 0:
			if self.PinGresit.opacity == 255:
				PinGresitOptim = 1
		if PinGresitOptim == 1:
			self.PinGresit.do(FadeOut(2))

	#Update Hidden Pin Text
	def UpdateHiddenPin(self):
		self.PinPassword.element.text = self.PinHidden

	#Update Self Pin Tries
	def UpdateSelfPinTries(self):
		self.IncercRamase.element.text = "Incercari Ramase: " + str(self.PinTries)

	#Reset All
	def ResetAll(self):
		#Reset Pin
		self.PinPasswordNumbers = []
		self.PinHidden = ''
		self.UpdateHiddenPin()
		#Reset Tries
		self.PinTries = 3
		

	#Keyboard Inputs
	def on_key_release(self,keys,modi):
		global ActiveCard
		#Check if there are tries left
		if self.PinTries > 0:
			#Verify Code Submit
			if keys == key.ENTER:
				if len(self.PinPasswordNumbers) == 4:
					KeepNumbers = ''
					for a in range(0,len(self.PinPasswordNumbers)):
						KeepNumbers += str(self.PinPasswordNumbers[a])
					#First Card
					if int(KeepNumbers) == 1234:
						#Reset Everything
						self.ResetAll()
						self.UpdateSelfPinTries()
						#Select 1st Card
						ActiveCard = 0
						#Change Scene
						cocos.director.director.replace(MainMenuScene)
						cocos.director.director.push(MainMenuScene)
					#Second Card
					elif int(KeepNumbers) == 4567:
						#Reset Everything
						self.ResetAll()
						self.UpdateSelfPinTries()
						#Select 2nd Card
						ActiveCard = 1
						#Change Scene
						cocos.director.director.replace(MainMenuScene)
						cocos.director.director.push(MainMenuScene)
					else:
						self.PinGresitText()
				else:
					self.PinGresitText()

			#Delete Wrong Code
			if keys == key.BACKSPACE:
				self.PinPasswordNumbers = []
				self.PinHidden = ''
				self.UpdateHiddenPin()

			#Check if it's a number
			ContinueCalc = False
			NumberConvert = pyglet.window.key.symbol_string(keys)[-1]
			for a in range(11):
				if NumberConvert == str(a):
					ContinueCalc = True
			if ContinueCalc == True:
				self.PinPasswordNumbers.append(int(NumberConvert))
				for a in range(0,len(self.PinPasswordNumbers) + 1):
					if self.PinHidden == "****":
						pass
					else:
						self.PinHidden = '*' * a
						self.UpdateHiddenPin()
			#Limit Pin Password
			if len(self.PinPasswordNumbers) > 4:
				self.PinPasswordNumbers.pop(0)

			#Clear The Text if there aren't any more tries
			if self.PinTries <= 0:
				self.PinHidden = ""
				self.UpdateHiddenPin()
				self.CardBlocat.opacity = 255

#Main Menu
class MainMenu(cocos.layer.Layer):
	is_event_handler = True

	#Button Template
	def ButtonTemplate(self,ButText,PosX,PosY):
		#Background
		self.BgName = cocos.sprite.Sprite("Files/ButtonBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.7
		self.BgName.scale_x = 0.9
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel

	def __init__(self):
		super(MainMenu,self).__init__()
		self.SelectOptionMain = 3
		self.SelectPosition = [(512,200),(512,300),(512,400),(512,500)]

		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)

		#Interogare Sold
		self.InterSold = self.ButtonTemplate("Interogare Sold",512,500)

		#Retragere Numerar
		self.RetNum = self.ButtonTemplate("Retragere Numerar",512,400)

		#Depozitare
		self.DepozitNum = self.ButtonTemplate("Depozitare Numerar",512,300)

		#Iesire
		self.Iesire = self.ButtonTemplate("Iesire",512,200)

		#Select
		self.Select = cocos.sprite.Sprite("Files/ButtonSelected.png")
		self.Select.scale_y = 0.7
		self.Select.scale_x = 0.9
		self.Select.scale = 1.2
		self.Select.opacity = 125
		self.add(self.Select)

		self.Number = 0
		self.NumberOptim = 0

	#Loop Functions
	def _step(self,dt):
		super(MainMenu,self)._step
		#Select Position
		for a in range(4):
			if a == self.SelectOptionMain:
				self.Select.position = self.SelectPosition[a]

		#Select Blink
		self.Number += 1 * dt
		if self.Number < 5 and self.NumberOptim == 0:
			self.Select.do(Blink(5,5))
			self.NumberOptim = 1
		if self.Number >= 4.5:
			self.Number = 0
			self.NumberOptim = 0

	#Keyboard Inputs
	def on_key_release(self,keys,modi):
		#Up Arrow
		if keys == key.UP:
			self.SelectOptionMain += 1
			if self.SelectOptionMain > 3:
				self.SelectOptionMain = 0
		#Down Arrow
		if keys == key.DOWN:
			self.SelectOptionMain -= 1
			if self.SelectOptionMain < 0:
				self.SelectOptionMain = 3
		#Enter
		if keys == key.ENTER:
			#Back to PinInterface Menu
			if self.SelectOptionMain == 0:
				cocos.director.director.replace(PinScene)
			elif self.SelectOptionMain == 1:
				cocos.director.director.replace(DepositScene)
			elif self.SelectOptionMain == 2:
				cocos.director.director.replace(WithdrawScene)
			elif self.SelectOptionMain == 3:
				cocos.director.director.replace(AccountBalanceScene)

#Withdraw Menu
class Withdraw(cocos.layer.Layer):
	is_event_handler = True

	#Button Template
	def ButtonTemplate(self,ButText,PosX,PosY):
		#Background
		self.BgName = cocos.sprite.Sprite("Files/ButtonBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.7
		self.BgName.scale_x = 0.9
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel

	def AboveTextTemplate(self):
		self.AboveSprite = cocos.sprite.Sprite('Files/AboveText.png',(510,500))
		self.AboveSprite.scale_x = 1.8
		self.add(self.AboveSprite)
		self.AboveText = cocos.text.Label("Introduceti Suma",anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.AboveText.scale_x = 0.7
		self.AboveSprite.add(self.AboveText)

	#Input Button Template
	def InputButtonTemplate(self,ButText,PosX,PosY):
		#Background
		self.BgName = cocos.sprite.Sprite("Files/CodPinBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.5
		self.BgName.scale_x = 1.5
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.NewLabel.scale_y = 1.6
		self.NewLabel.scale_x = 0.6
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel
	
	#Init
	def __init__(self):
		super(Withdraw,self).__init__()
		#Optim Vars
		self.SumaInsufBool = False
		self.SumaInsufOptim = 0
		self.SumaInsufTime = 0
		self.InvalidNumbBool = False
		self.InvalidNumbOptim = 0
		self.InvalidNumbTime = 0

		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)

		# Player input/Text
		self.WithdrawSum = []
		self.WithdrawText = self.InputButtonTemplate(str(0) + " RON",512,350)

		#Select Option Var/Position Array
		self.SelectOptionMain = 0
		self.SelectPosition = [(870,160),(870,60)]

		#Confirmare
		self.Anulare = self.ButtonTemplate("Confirmare",870,160)

		#Anulare
		self.DepozitNum = self.ButtonTemplate("Anulare",870,60)

		#Numar Invalid
		self.NumarInvalid = cocos.text.Label("Numar Invalid",(440,200),color = (0,0,0,255))
		self.NumarInvalid.scale = 1.2
		self.NumarInvalid.opacity = 0
		self.add(self.NumarInvalid)

		#Suma Insuficienta
		self.SumaInsuf = cocos.text.Label("Suma Insuficienta",(440,200),color = (0,0,0,255))
		self.SumaInsuf.scale = 1.2
		self.SumaInsuf.opacity = 0
		self.add(self.SumaInsuf)

		#Select
		self.Select = cocos.sprite.Sprite("Files/ButtonSelected.png")
		self.Select.scale_y = 0.7
		self.Select.scale_x = 0.9
		self.Select.scale = 1.2
		self.Select.opacity = 125
		self.add(self.Select)

		self.Number = 0
		self.NumberOptim = 0

		#Introduceti Suma
		self.SumInsert = self.AboveTextTemplate()

	#Loop Functions
	def _step(self,dt):
		super(Withdraw,self)._step
		#Select Position
		for a in range(2):
			if a == self.SelectOptionMain:
				self.Select.position = self.SelectPosition[a]
		#Select Blink
		self.Number += 1 * dt
		if self.Number < 5 and self.NumberOptim == 0:
			self.Select.do(Blink(5,5))
			self.NumberOptim = 1
		if self.Number >= 4.5:
			self.Number = 0
			self.NumberOptim = 0

		#Numar Invalid Anim
		if self.InvalidNumbBool == True:
			self.InvalidNumbTime += 1 * dt
			if self.InvalidNumbOptim == 0 and self.InvalidNumbTime < 1:
				self.NumarInvalid.opacity = 255
				self.InvalidNumbOptim = 1
			if self.InvalidNumbOptim == 1 and self.InvalidNumbTime > 1:
				self.NumarInvalid.opacity = 0
				self.InvalidNumbOptim = 0
				self.InvalidNumbTime = 0
				self.InvalidNumbBool = False
		
		#Suma Insuficienta Anim
		if self.SumaInsufBool == True:
			self.SumaInsufTime += 1 * dt
			if self.SumaInsufOptim == 0 and self.SumaInsufTime < 1:
				self.SumaInsuf.opacity = 255
				self.SumaInsufOptim = 1
			if self.SumaInsufOptim == 1 and self.SumaInsufTime > 1:
				self.SumaInsuf.opacity = 0
				self.SumaInsufOptim = 0
				self.SumaInsufTime = 0
				self.SumaInsufBool = False


	#Update Player Input
	def UpdatePlayerInput(self):
		if self.WithdrawSum[0] == 0:
			self.WithdrawSum.pop(0)
		self.StrConv = ""
		for a in range(len(self.WithdrawSum)):
			self.StrConv += str(self.WithdrawSum[a])
		self.WithdrawText[1].element.text = self.StrConv + " RON"
		
	#Keyboard Inputs
	def on_key_release(self,keys,modi):
		#Up Arrow
		if keys == key.UP:
			self.SelectOptionMain += 1
			if self.SelectOptionMain > 1:
				self.SelectOptionMain = 0
		#Down Arrow
		if keys == key.DOWN:
			self.SelectOptionMain -= 1
			if self.SelectOptionMain < 0:
				self.SelectOptionMain = 1

		#Delete
		if keys == key.BACKSPACE:
			self.WithdrawSum = [0]
			self.WithdrawText[1].element.text = str(0) + " RON"

		#Check if it's a number
		ContinueCalc = False
		NumberConvert = pyglet.window.key.symbol_string(keys)[-1]
		for a in range(11):
			if NumberConvert == str(a):
				ContinueCalc = True
		if ContinueCalc == True:
			if len(self.WithdrawSum) < 6:
				self.WithdrawSum.append(int(NumberConvert))
			self.UpdatePlayerInput()

		#Enter
		#Confirm/Cancel
		if keys == key.ENTER:
			#Confirm
			if self.SelectOptionMain == 0:
				self.StrConv = ""
				for a in range(len(self.WithdrawSum)):
					self.StrConv += str(self.WithdrawSum[a])
				#If there isn't any input
				if self.StrConv == "":
					self.StrConv = "0"
				#Card 1
				global BalanceCard1
				global BalanceCard2
				if ActiveCard == 0:
					if int(self.StrConv) == 0:
						if self.InvalidNumbBool == False:
							self.InvalidNumbBool = True
					elif int(self.StrConv) < BalanceCard1:
						BalanceCard1 -= int(self.StrConv)
						self.WithdrawSum = [0]
						self.WithdrawText[1].element.text = str(0) + " RON"
						cocos.director.director.replace(CompleteTransScene)
					else:
						if self.SumaInsufBool == False:
							self.SumaInsufBool = True
				#Card 2
				else:
					if int(self.StrConv) == 0:
						if self.InvalidNumbBool == False:
							self.InvalidNumbBool = True
					elif int(self.StrConv) < BalanceCard2:
						BalanceCard2 -= int(self.StrConv)
						self.WithdrawSum = [0]
						self.WithdrawText[1].element.text = str(0) + " RON"
						cocos.director.director.replace(CompleteTransScene)
					else:
						if self.SumaInsufBool == False:
							self.SumaInsufBool = True
			#Cancel
			elif self.SelectOptionMain == 1:
				cocos.director.director.replace(MainMenuScene)

#Compelete Transaction Menu
class CompleteTransMenu(cocos.layer.Layer):
	def __init__(self):
		super(CompleteTransMenu,self).__init__()
		self.Timer = 0
		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)

		#TransComplete Text
		self.TransCompleteText = cocos.text.Label("Tranzactie Completa",(400,360),color = (0,0,0,255))
		self.TransCompleteText.scale = 1.6
		self.add(self.TransCompleteText)
	def _step(self,dt):
		super(CompleteTransMenu,self)._step
		if self.Timer < 2:
			self.Timer += dt
		else:
			self.Timer = 0
			cocos.director.director.replace(MainMenuScene)

#Deposit Menu
class Deposit(cocos.layer.Layer):
	is_event_handler = True

	#Button Template
	def ButtonTemplate(self,ButText,PosX,PosY):
		#Background
		self.BgName = cocos.sprite.Sprite("Files/ButtonBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.7
		self.BgName.scale_x = 0.9
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel

	def AboveTextTemplate(self):
		self.AboveSprite = cocos.sprite.Sprite('Files/AboveText.png',(510,500))
		self.AboveSprite.scale_x = 1.8
		self.add(self.AboveSprite)
		self.AboveText = cocos.text.Label("Introduceti Suma",anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.AboveText.scale_x = 0.7
		self.AboveSprite.add(self.AboveText)

	#Input Button Template
	def InputButtonTemplate(self,ButText,PosX,PosY):
		#Background
		self.BgName = cocos.sprite.Sprite("Files/CodPinBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.5
		self.BgName.scale_x = 1.5
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.NewLabel.scale_y = 1.6
		self.NewLabel.scale_x = 0.6
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel
	
	#Init
	def __init__(self):
		super(Deposit,self).__init__()
		#Optim Vars
		self.InvalidNumbBool = False
		self.InvalidNumbOptim = 0
		self.InvalidNumbTime = 0

		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)

		# Player input/Text
		self.DepositSum = []
		self.WithdrawText = self.InputButtonTemplate(str(0) + " RON",512,350)

		#Select Option Var/Position Array
		self.SelectOptionMain = 0
		self.SelectPosition = [(870,160),(870,60)]

		#Confirmare
		self.Anulare = self.ButtonTemplate("Confirmare",870,160)

		#Anulare
		self.DepozitNum = self.ButtonTemplate("Anulare",870,60)

		#Numar Invalid
		self.NumarInvalid = cocos.text.Label("Numar Invalid",(440,200),color = (0,0,0,255))
		self.NumarInvalid.scale = 1.2
		self.NumarInvalid.opacity = 0
		self.add(self.NumarInvalid)

		#Select
		self.Select = cocos.sprite.Sprite("Files/ButtonSelected.png")
		self.Select.scale_y = 0.7
		self.Select.scale_x = 0.9
		self.Select.scale = 1.2
		self.Select.opacity = 125
		self.add(self.Select)

		self.Number = 0
		self.NumberOptim = 0

		#Introduceti Suma
		self.SumInsert = self.AboveTextTemplate()

	#Loop Functions
	def _step(self,dt):
		super(Deposit,self)._step
		#Select Position
		for a in range(2):
			if a == self.SelectOptionMain:
				self.Select.position = self.SelectPosition[a]
		#Select Blink
		self.Number += 1 * dt
		if self.Number < 5 and self.NumberOptim == 0:
			self.Select.do(Blink(5,5))
			self.NumberOptim = 1
		if self.Number >= 4.5:
			self.Number = 0
			self.NumberOptim = 0

		#Numar Invalid Anim
		if self.InvalidNumbBool == True:
			self.InvalidNumbTime += 1 * dt
			if self.InvalidNumbOptim == 0 and self.InvalidNumbTime < 1:
				self.NumarInvalid.opacity = 255
				self.InvalidNumbOptim = 1
			if self.InvalidNumbOptim == 1 and self.InvalidNumbTime > 1:
				self.NumarInvalid.opacity = 0
				self.InvalidNumbOptim = 0
				self.InvalidNumbTime = 0
				self.InvalidNumbBool = False


	#Update Player Input
	def UpdatePlayerInput(self):
		if self.DepositSum[0] == 0:
			self.DepositSum.pop(0)
		self.StrConv = ""
		for a in range(len(self.DepositSum)):
			self.StrConv += str(self.DepositSum[a])
		self.WithdrawText[1].element.text = self.StrConv + " RON"
		
	#Keyboard Inputs
	def on_key_release(self,keys,modi):
		#Up Arrow
		if keys == key.UP:
			self.SelectOptionMain += 1
			if self.SelectOptionMain > 1:
				self.SelectOptionMain = 0
		#Down Arrow
		if keys == key.DOWN:
			self.SelectOptionMain -= 1
			if self.SelectOptionMain < 0:
				self.SelectOptionMain = 1

		#Delete
		if keys == key.BACKSPACE:
			self.DepositSum = [0]
			self.WithdrawText[1].element.text = str(0) + " RON"

		#Check if it's a number
		ContinueCalc = False
		NumberConvert = pyglet.window.key.symbol_string(keys)[-1]
		for a in range(11):
			if NumberConvert == str(a):
				ContinueCalc = True
		if ContinueCalc == True:
			if len(self.DepositSum) < 6:
				self.DepositSum.append(int(NumberConvert))
			self.UpdatePlayerInput()

		#Enter
		#Confirm/Cancel
		if keys == key.ENTER:
			#Confirm
			if self.SelectOptionMain == 0:
				self.StrConv = ""
				for a in range(len(self.DepositSum)):
					self.StrConv += str(self.DepositSum[a])
				#If there isn't any input
				if self.StrConv == "":
					self.StrConv = "0"
				#Card 1
				global ActiveCard
				global BalanceCard1
				global BalanceCard2
				if ActiveCard == 0:
					if int(self.StrConv) == 0:
						if self.InvalidNumbBool == False:
							self.InvalidNumbBool = True
					else:
						BalanceCard1 += int(self.StrConv)
						self.DepositSum = [0]
						self.WithdrawText[1].element.text = str(0) + " RON"
						cocos.director.director.replace(CompleteTransScene)
				#Card 2
				elif ActiveCard == 1:
					if int(self.StrConv) == 0:
						if self.InvalidNumbBool == False:
							self.InvalidNumbBool = True
					else:
						BalanceCard2 += int(self.StrConv)
						self.DepositSum = [0]
						self.WithdrawText[1].element.text = str(0) + " RON"
						cocos.director.director.replace(CompleteTransScene)
			#Cancel
			elif self.SelectOptionMain == 1:
				cocos.director.director.replace(MainMenuScene)

#Account Balance Menu
class AccountBalance(cocos.layer.Layer):
	is_event_handler = True

	def ButtonTemplate(self,ButText,PosX,PosY):
		#Time
		self.Time = 0

		#Background
		self.BgName = cocos.sprite.Sprite("Files/ButtonBG.png",(PosX,PosY))
		self.BgName.scale_y = 0.7
		self.BgName.scale_x = 0.9
		self.BgName.scale = 1.2
		self.add(self.BgName)
		#Text
		self.NewLabel = cocos.text.Label(ButText,anchor_x = "center",anchor_y = "center",color = (0,0,0,255))
		self.BgName.add(self.NewLabel)
		return self.BgName,self.NewLabel
	
	#Init
	def __init__(self):
		super(AccountBalance,self).__init__()
		#Optim Vars
		self.Time = False

		#Background
		SpriteBackground = cocos.sprite.Sprite('Files/Background.png')
		SpriteBackground.scale = 4
		self.add(SpriteBackground)
		global BalanceCard1
		global BalanceCard2
		#Suma Totala
		#Card 1
		self.SumaTotalaCard1 = cocos.text.Label("Suma Totala : " + str(BalanceCard1),(400,360))
		self.SumaTotalaCard1.scale = 1.5
		self.add(self.SumaTotalaCard1)
		#Card 2
		self.SumaTotalaCard2 = cocos.text.Label("Suma Totala : " + str(BalanceCard2),(400,360))
		self.SumaTotalaCard2.scale = 1.5
		self.add(self.SumaTotalaCard2)

	#Update Balance
	def UpdateBalance(self):
		if ActiveCard == 0:
			self.SumaTotalaCard1.element.text = "Suma Totala : " + str(BalanceCard1)
			self.SumaTotalaCard1.opacity = 255
			self.SumaTotalaCard2.opacity = 0
		else:
			self.SumaTotalaCard2.element.text = "Suma Totala : " + str(BalanceCard2)
			self.SumaTotalaCard1.opacity = 0
			self.SumaTotalaCard2.opacity = 255

	#Loop Functions
	def _step(self,dt):
		super(AccountBalance,self)._step
		#Update Balance
		self.UpdateBalance()

		#Back to main menu
		if self.Time < 1.5:
			self.Time += 1 * dt
		else:
			self.Time = 0
			cocos.director.director.replace(MainMenuScene)

#Screen/Scenes Load
cocos.director.director.init(1024,720,caption = "Bancomat")
PinScene = cocos.scene.Scene(PinInterface())
MainMenuScene = cocos.scene.Scene(MainMenu())
WithdrawScene = cocos.scene.Scene(Withdraw())
DepositScene = cocos.scene.Scene(Deposit())
AccountBalanceScene = cocos.scene.Scene(AccountBalance())
CompleteTransScene = cocos.scene.Scene(CompleteTransMenu())
cocos.director.director.run(PinScene)
